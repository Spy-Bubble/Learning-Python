import random
import math

# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================

def distancia_euclidiana(p1, p2):
    """Distancia euclidiana entre dos puntos (listas o tuplas)"""
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

# ============================================================================
# 28. k-NN, k-MEDIAS Y CLUSTERING
# ============================================================================

# --- k-Nearest Neighbors ---
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
        # Calcular distancias a todos los puntos de entrenamiento
        distancias = []
        for i, x_train in enumerate(self.X_train):
            dist = distancia_euclidiana(x, x_train)
            distancias.append((dist, self.y_train[i]))
        
        # Ordenar y tomar k más cercanos
        distancias.sort(key=lambda item: item[0])
        k_vecinos = distancias[:self.k]
        
        # Votación mayoritaria
        votos = {}
        for _, clase in k_vecinos:
            votos[clase] = votos.get(clase, 0) + 1
            
        if not votos: return None # No hay vecinos?
        
        # Devolver la clase con más votos
        return max(votos.items(), key=lambda x: x[1])[0]

# --- k-Medias ---
def k_medias(datos, k, max_iter=100, tolerancia=1e-4):
    """
    Algoritmo k-medias
    Args:
        datos: lista de puntos (listas o tuplas)
        k: número de clusters
        max_iter: iteraciones máximas
        tolerancia: para convergencia de centroides
    Returns:
        (centroides, asignaciones)
    """
    n_samples = len(datos)
    if n_samples == 0 or k == 0: return [], []
    n_features = len(datos[0])

    # Inicializar centroides aleatoriamente (eligiendo k puntos)
    centroides = random.sample(datos, k)
    
    for iter_num in range(max_iter):
        # Asignar cada punto al centroide más cercano
        asignaciones = [-1] * n_samples
        for i, punto in enumerate(datos):
            distancias = [distancia_euclidiana(punto, c) for c in centroides]
            cluster_idx = distancias.index(min(distancias))
            asignaciones[i] = cluster_idx
            
        # Actualizar centroides
        nuevos_centroides = [[0.0] * n_features for _ in range(k)]
        conteos_cluster = [0] * k
        
        for i, punto in enumerate(datos):
            cluster_id = asignaciones[i]
            conteos_cluster[cluster_id] += 1
            for d in range(n_features):
                nuevos_centroides[cluster_id][d] += punto[d]
        
        centroides_antiguos = [list(c) for c in centroides] # Copia profunda
        
        for cluster_id in range(k):
            if conteos_cluster[cluster_id] > 0:
                for d in range(n_features):
                    nuevos_centroides[cluster_id][d] /= conteos_cluster[cluster_id]
            else: # Cluster vacío, re-inicializar (o mantener)
                nuevos_centroides[cluster_id] = random.choice(datos) 
        
        centroides = [tuple(c) for c in nuevos_centroides] # Convertir a tuplas para comparación

        # Verificar convergencia
        cambio_total = sum(distancia_euclidiana(centroides[i], centroides_antiguos[i]) for i in range(k))
        if cambio_total < tolerancia:
            break
            
    # Asignar puntos finales a los centroides convergidos
    asignaciones_finales = [-1] * n_samples
    for i, punto in enumerate(datos):
        distancias = [distancia_euclidiana(punto, c) for c in centroides]
        asignaciones_finales[i] = distancias.index(min(distancias))

    return centroides, asignaciones_finales

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 28. k-NN y k-Medias ===\n")
    
    # --- k-NN ---
    print("k-Nearest Neighbors (k-NN):")
    X_knn = [[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]]
    y_knn = [0, 0, 0, 1, 1, 1]
    
    knn = KNN(k=3)
    knn.entrenar(X_knn, y_knn)
    
    test_point = [5, 5]
    pred = knn.predecir(test_point)
    print(f"   Datos entrenamiento: {X_knn} (Clases: {y_knn})")
    print(f"   Punto de prueba: {test_point}")
    print(f"   Clase predicha (k=3): {pred}\n")
    
    # --- k-Medias ---
    print("k-Medias Clustering:")
    datos_cluster = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]
    centroides, asignaciones = k_medias(datos_cluster, k=2)
    print(f"   Datos: {datos_cluster}")
    print(f"   Centroides encontrados (k=2): {[list(c) for c in centroides]}")
    print(f"   Asignaciones a clusters: {asignaciones}")