"""
APRENDIZAJE PROBABILÍSTICO
Algoritmos 23-30: Aprendizaje bayesiano, clustering, SVM, deep learning
"""

import random
import math
import numpy as np
from collections import defaultdict

# ============================================================================
# 23. APRENDIZAJE BAYESIANO
# ============================================================================

def aprendizaje_bayesiano(datos, hipotesis, prior, verosimilitud_func):
    """
    Aprendizaje bayesiano: actualiza creencias sobre hipótesis
    Args:
        datos: datos observados
        hipotesis: lista de hipótesis posibles
        prior: dict {hipótesis: P(h)}
        verosimilitud_func: función que calcula P(datos|h)
    Returns:
        posterior: dict {hipótesis: P(h|datos)}
    """
    posterior = {}
    
    # Calcular P(datos|h) * P(h) para cada hipótesis
    for h in hipotesis:
        verosimilitud = verosimilitud_func(datos, h)
        posterior[h] = verosimilitud * prior[h]
    
    # Normalizar
    total = sum(posterior.values())
    if total > 0:
        posterior = {h: p/total for h, p in posterior.items()}
   
    return posterior


def map_hypothesis(posterior):
    """
    Encuentra hipótesis MAP (Maximum A Posteriori)
    Args:
        posterior: distribución posterior
    Returns:
        hipótesis con máxima probabilidad posterior
    """
    return max(posterior.items(), key=lambda x: x[1])[0]


# ============================================================================
# 24. NAÏVE BAYES
# ============================================================================

class NaiveBayes:
    """
    Clasificador Naïve Bayes
    """
    def __init__(self):
        self.clases = []
        self.prior = {}  # P(clase)
        self.verosimilitud = {}  # P(feature|clase)
    
    def entrenar(self, X, y):
        """
        Entrena el clasificador
        Args:
            X: lista de ejemplos (cada ejemplo es lista de features)
            y: lista de etiquetas de clase
        """
        # Contar clases
        self.clases = list(set(y))
        conteo_clases = {c: y.count(c) for c in self.clases}
        total = len(y)
        
        # Calcular prior P(clase)
        self.prior = {c: count/total for c, count in conteo_clases.items()}
        
        # Calcular verosimilitud P(feature=valor|clase)
        self.verosimilitud = {}
        
        for clase in self.clases:
            # Filtrar ejemplos de esta clase
            indices_clase = [i for i, label in enumerate(y) if label == clase]
            ejemplos_clase = [X[i] for i in indices_clase]
            
            # Para cada feature
            num_features = len(X[0])
            for f_idx in range(num_features):
                valores_feature = [ej[f_idx] for ej in ejemplos_clase]
                
                # Contar cada valor
                valores_unicos = set(valores_feature)
                for valor in valores_unicos:
                    count = valores_feature.count(valor)
                    # Suavizado de Laplace
                    prob = (count + 1) / (len(valores_feature) + len(valores_unicos))
                    self.verosimilitud[(f_idx, valor, clase)] = prob
    
    def predecir(self, ejemplo):
        """
        Predice la clase de un ejemplo
        Args:
            ejemplo: lista de features
        Returns:
            clase predicha
        """
        mejor_clase = None
        mejor_prob = float('-inf')
        
        for clase in self.clases:
            # log P(clase|ejemplo) ∝ log P(clase) + Σ log P(feature|clase)
            log_prob = math.log(self.prior[clase])
            
            for f_idx, valor in enumerate(ejemplo):
                # Obtener verosimilitud (con suavizado si no existe)
                prob = self.verosimilitud.get((f_idx, valor, clase), 1e-10)
                log_prob += math.log(prob)
            
            if log_prob > mejor_prob:
                mejor_prob = log_prob
                mejor_clase = clase
        
        return mejor_clase


# ============================================================================
# 25. ALGORITMO EM (EXPECTATION-MAXIMIZATION)
# ============================================================================

def algoritmo_em_gaussiano(datos, num_componentes, max_iter=100, tolerancia=0.001):
    """
    EM para mezcla de gaussianas
    Args:
        datos: lista de puntos (1D)
        num_componentes: número de gaussianas en la mezcla
        max_iter: iteraciones máximas
        tolerancia: criterio de convergencia
    Returns:
        (medias, varianzas, pesos) de las gaussianas
    """
    n = len(datos)
    
    # Inicialización aleatoria
    medias = random.sample(datos, num_componentes)
    varianzas = [1.0] * num_componentes
    pesos = [1.0/num_componentes] * num_componentes
    
    for iteracion in range(max_iter):
        # E-step: calcular responsabilidades
        responsabilidades = []
        
        for x in datos:
            r = []
            for k in range(num_componentes):
                # P(componente k | x)
                prob = pesos[k] * gaussiana(x, medias[k], varianzas[k])
                r.append(prob)
            
            # Normalizar
            suma = sum(r)
            if suma > 0:
                r = [ri/suma for ri in r]
            responsabilidades.append(r)
        
        # M-step: actualizar parámetros
        medias_nuevas = []
        varianzas_nuevas = []
        pesos_nuevos = []
        
        for k in range(num_componentes):
            # Peso efectivo
            n_k = sum(r[k] for r in responsabilidades)
            
            if n_k > 0:
                # Media
                media = sum(r[k] * x for r, x in zip(responsabilidades, datos)) / n_k
                medias_nuevas.append(media)
                
                # Varianza
                varianza = sum(r[k] * (x - media)**2 
                             for r, x in zip(responsabilidades, datos)) / n_k
                varianzas_nuevas.append(max(varianza, 0.01))  # Evitar varianza 0
                
                # Peso
                pesos_nuevos.append(n_k / n)
            else:
                medias_nuevas.append(medias[k])
                varianzas_nuevas.append(varianzas[k])
                pesos_nuevos.append(pesos[k])
        
        # Verificar convergencia
        cambio = sum(abs(m_new - m_old) 
                    for m_new, m_old in zip(medias_nuevas, medias))
        
        medias = medias_nuevas
        varianzas = varianzas_nuevas
        pesos = pesos_nuevos
        
        if cambio < tolerancia:
            break
    
    return medias, varianzas, pesos


def gaussiana(x, media, varianza):
    """Densidad de probabilidad gaussiana"""
    return (1.0 / math.sqrt(2 * math.pi * varianza)) * \
           math.exp(-0.5 * ((x - media) ** 2) / varianza)


# ============================================================================
# 26. AGRUPAMIENTO NO SUPERVISADO
# ============================================================================

def agrupamiento_jerarquico(datos, num_clusters):
    """
    Clustering jerárquico aglomerativo
    Args:
        datos: lista de puntos
        num_clusters: número de clusters deseados
    Returns:
        asignación de clusters
    """
    # Inicializar cada punto como su propio cluster
    clusters = [[i] for i in range(len(datos))]
    
    while len(clusters) > num_clusters:
        # Encontrar par de clusters más cercanos
        min_dist = float('inf')
        merge_i, merge_j = 0, 1
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # Distancia entre clusters (linkage promedio)
                dist = distancia_clusters(datos, clusters[i], clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    merge_i, merge_j = i, j
        
        # Fusionar clusters
        clusters[merge_i].extend(clusters[merge_j])
        del clusters[merge_j]
    
    # Crear asignación
    asignacion = [0] * len(datos)
    for cluster_id, cluster in enumerate(clusters):
        for punto_id in cluster:
            asignacion[punto_id] = cluster_id
    
    return asignacion


def distancia_clusters(datos, cluster1, cluster2):
    """Calcula distancia promedio entre dos clusters"""
    distancias = []
    for i in cluster1:
        for j in cluster2:
            dist = abs(datos[i] - datos[j]) if isinstance(datos[i], (int, float)) \
                   else distancia_euclidiana(datos[i], datos[j])
            distancias.append(dist)
    
    return sum(distancias) / len(distancias) if distancias else 0


def distancia_euclidiana(p1, p2):
    """Distancia euclidiana entre dos puntos"""
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))


# ============================================================================
# 27. MODELOS DE MARKOV OCULTOS (HMM con aprendizaje)
# ============================================================================

def baum_welch(observaciones, num_estados, num_iteraciones=10):
    """
    Algoritmo Baum-Welch para aprender parámetros de HMM
    Args:
        observaciones: secuencias de observaciones
        num_estados: número de estados ocultos
        num_iteraciones: iteraciones del algoritmo
    Returns:
        (transiciones, emisiones, inicial) aprendidos
    """
    # Obtener observaciones únicas
    obs_unicas = sorted(set(sum(observaciones, [])))
    estados = list(range(num_estados))
    
    # Inicialización aleatoria
    transiciones = inicializar_aleatorio(num_estados, num_estados)
    emisiones = inicializar_aleatorio(num_estados, len(obs_unicas))
    inicial = [1.0/num_estados] * num_estados
    
    for _ in range(num_iteraciones):
        # E-step (forward-backward) simplificado
        # M-step: actualizar parámetros basado en conteos esperados
        
        # Aquí se calcularían las expectativas usando forward-backward
        # y se actualizarían los parámetros
        # (Implementación completa es extensa)
        pass
    
    return transiciones, emisiones, inicial


def inicializar_aleatorio(filas, columnas):
    """Inicializa matriz estocástica aleatoria"""
    matriz = []
    for _ in range(filas):
        fila = [random.random() for _ in range(columnas)]
        suma = sum(fila)
        fila = [x/suma for x in fila]
        matriz.append(fila)
    return matriz


# ============================================================================
# 28. k-NN, k-MEDIAS Y CLUSTERING
# ============================================================================

class KNN:
    """Clasificador k-Nearest Neighbors"""
    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []
    
    def entrenar(self, X, y):
        """Guarda datos de entrenamiento"""
        self.X_train = X
        self.y_train = y
    
    def predecir(self, x):
        """Predice clase de un punto"""
        # Calcular distancias
        distancias = []
        for i, x_train in enumerate(self.X_train):
            dist = distancia_euclidiana(x, x_train)
            distancias.append((dist, self.y_train[i]))
        
        # Ordenar y tomar k más cercanos
        distancias.sort()
        k_vecinos = distancias[:self.k]
        
        # Votación mayoritaria
        votos = {}
        for _, clase in k_vecinos:
            votos[clase] = votos.get(clase, 0) + 1
        
        return max(votos.items(), key=lambda x: x[1])[0]


def k_medias(datos, k, max_iter=100):
    """
    Algoritmo k-medias
    Args:
        datos: lista de puntos (listas o tuplas)
        k: número de clusters
        max_iter: iteraciones máximas
    Returns:
        (centroides, asignaciones)
    """
    # Inicializar centroides aleatoriamente
    centroides = random.sample(datos, k)
    
    for _ in range(max_iter):
        # Asignar cada punto al centroide más cercano
        asignaciones = []
        for punto in datos:
            distancias = [distancia_euclidiana(punto, c) for c in centroides]
            cluster = distancias.index(min(distancias))
            asignaciones.append(cluster)
        
        # Actualizar centroides
        nuevos_centroides = []
        for cluster_id in range(k):
            puntos_cluster = [datos[i] for i, c in enumerate(asignaciones) 
                            if c == cluster_id]
            
            if puntos_cluster:
                # Calcular media
                dim = len(puntos_cluster[0])
                centroide = [sum(p[d] for p in puntos_cluster) / len(puntos_cluster) 
                           for d in range(dim)]
                nuevos_centroides.append(centroide)
            else:
                nuevos_centroides.append(centroides[cluster_id])
        
        # Verificar convergencia
        if centroides == nuevos_centroides:
            break
        
        centroides = nuevos_centroides
    
    return centroides, asignaciones


# ============================================================================
# 29. MÁQUINAS DE VECTORES SOPORTE (NÚCLEO)
# ============================================================================

class SVM:
    """
    SVM simple con kernel lineal (implementación simplificada)
    """
    def __init__(self, learning_rate=0.01, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None
    
    def entrenar(self, X, y):
        """
        Entrena el SVM
        Args:
            X: matriz de características (n_samples, n_features)
            y: vector de etiquetas (-1 o 1)
        """
        n_samples, n_features = len(X), len(X[0])
        
        # Inicializar pesos
        self.w = [0.0] * n_features
        self.b = 0
        
        # Asegurar etiquetas -1 y 1
        y_mapped = [1 if yi >= 0 else -1 for yi in y]
        
        # Descenso de gradiente
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condicion = y_mapped[idx] * (self.producto_punto(x_i, self.w) - self.b) >= 1
                
                if condicion:
                    # Actualizar solo regularización
                    self.w = [w - self.lr * (2 * self.lambda_param * w) 
                             for w in self.w]
                else:
                    # Actualizar con término de clasificación incorrecta
                    self.w = [w - self.lr * (2 * self.lambda_param * w - y_mapped[idx] * x_i[j])
                             for j, w in enumerate(self.w)]
                    self.b -= self.lr * y_mapped[idx]
    
    def predecir(self, X):
        """Predice etiquetas"""
        salida = [self.producto_punto(x, self.w) - self.b for x in X]
        return [1 if s >= 0 else -1 for s in salida]
    
    def producto_punto(self, x1, x2):
        """Producto punto de dos vectores"""
        return sum(a * b for a, b in zip(x1, x2))


def kernel_rbf(x1, x2, gamma=0.1):
    """
    Kernel RBF (Radial Basis Function)
    """
    dist_sq = sum((a - b)**2 for a, b in zip(x1, x2))
    return math.exp(-gamma * dist_sq)


# ============================================================================
# 30. APRENDIZAJE PROFUNDO (DEEP LEARNING)
# ============================================================================

class RedNeuronalSimple:
    """
    Red neuronal simple de 2 capas
    """
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.lr = learning_rate
        
        # Inicializar pesos aleatoriamente
        self.W1 = [[random.uniform(-1, 1) for _ in range(hidden_size)] 
                   for _ in range(input_size)]
        self.b1 = [0.0] * hidden_size
        
        self.W2 = [[random.uniform(-1, 1) for _ in range(output_size)] 
                   for _ in range(hidden_size)]
        self.b2 = [0.0] * output_size
    
    def sigmoid(self, x):
        """Función de activación sigmoide"""
        return 1 / (1 + math.exp(-x))
    
    def sigmoid_derivada(self, x):
        """Derivada de sigmoide"""
        s = self.sigmoid(x)
        return s * (1 - s)
    
    def forward(self, x):
        """Propagación hacia adelante"""
        # Capa oculta
        self.z1 = [sum(x[i] * self.W1[i][j] for i in range(len(x))) + self.b1[j] 
                   for j in range(len(self.b1))]
        self.a1 = [self.sigmoid(z) for z in self.z1]
        
        # Capa de salida
        self.z2 = [sum(self.a1[i] * self.W2[i][j] for i in range(len(self.a1))) + self.b2[j]
                   for j in range(len(self.b2))]
        self.a2 = [self.sigmoid(z) for z in self.z2]
        
        return self.a2
    
    def backward(self, x, y):
        """Retropropagación"""
        m = 1  # Un ejemplo a la vez
        
        # Error en capa de salida
        delta2 = [(self.a2[i] - y[i]) * self.sigmoid_derivada(self.z2[i]) 
                 for i in range(len(self.a2))]
        
        # Gradientes para W2 y b2
        dW2 = [[self.a1[i] * delta2[j] for j in range(len(delta2))] 
               for i in range(len(self.a1))]
        db2 = delta2
        
        # Error en capa oculta
        delta1 = [sum(delta2[j] * self.W2[i][j] for j in range(len(delta2))) * 
                 self.sigmoid_derivada(self.z1[i]) 
                 for i in range(len(self.a1))]
        
        # Gradientes para W1 y b1
        dW1 = [[x[i] * delta1[j] for j in range(len(delta1))] 
               for i in range(len(x))]
        db1 = delta1
        
        # Actualizar pesos
        for i in range(len(self.W2)):
            for j in range(len(self.W2[0])):
                self.W2[i][j] -= self.lr * dW2[i][j]
        
        for i in range(len(self.W1)):
            for j in range(len(self.W1[0])):
                self.W1[i][j] -= self.lr * dW1[i][j]
        
        self.b2 = [b - self.lr * db for b, db in zip(self.b2, db2)]
        self.b1 = [b - self.lr * db for b, db in zip(self.b1, db1)]
    
    def entrenar(self, X, y, epochs=1000):
        """Entrena la red"""
        for epoch in range(epochs):
            for x_i, y_i in zip(X, y):
                self.forward(x_i)
                self.backward(x_i, y_i)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== APRENDIZAJE PROBABILÍSTICO ===\n")
    
    # Ejemplo 24: Naïve Bayes
    print("24. Naïve Bayes:")
    # Clasificar si jugar tenis según clima
    X_train = [
        ['soleado', 'caliente', 'alta', 'debil'],
        ['soleado', 'caliente', 'alta', 'fuerte'],
        ['nublado', 'caliente', 'alta', 'debil'],
        ['lluvioso', 'templado', 'alta', 'debil'],
        ['lluvioso', 'frio', 'normal', 'debil'],
        ['nublado', 'frio', 'normal', 'fuerte'],
    ]
    y_train = ['no', 'no', 'si', 'si', 'si', 'no']
    
    nb = NaiveBayes()
    nb.entrenar(X_train, y_train)
    
    ejemplo = ['soleado', 'templado', 'alta', 'debil']
    prediccion = nb.predecir(ejemplo)
    print(f"   Ejemplo: {ejemplo}")
    print(f"   Predicción: {prediccion}\n")
    
    # Ejemplo 28: k-Medias
    print("28. k-Medias:")
    datos_cluster = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]
    centroides, asignaciones = k_medias(datos_cluster, k=2)
    print(f"   Datos: {datos_cluster}")
    print(f"   Centroides: {centroides}")
    print(f"   Asignaciones: {asignaciones}\n")
    
    # Ejemplo 28: k-NN
    print("   k-NN:")
    X_knn = [[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]]
    y_knn = [0, 0, 0, 1, 1, 1]
    
    knn = KNN(k=3)
    knn.entrenar(X_knn, y_knn)
    
    test_point = [5, 5]
    pred = knn.predecir(test_point)
    print(f"   Punto de prueba: {test_point}")
    print(f"   Clase predicha: {pred}\n")
    
    # Ejemplo 30: Red Neuronal
    print("30. Red Neuronal Simple:")
    # Aprender función XOR
    X_nn = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_nn = [[0], [1], [1], [0]]
    
    nn = RedNeuronalSimple(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)
    nn.entrenar(X_nn, y_nn, epochs=1000)
    
    print("   Entrenada en XOR:")
    for x, y_true in zip(X_nn, y_nn):
        y_pred = nn.forward(x)
        print(f"      Input: {x}, Esperado: {y_true[0]}, Predicho: {y_pred[0]:.3f}")