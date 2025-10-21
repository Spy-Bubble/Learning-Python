"""
REDES NEURONALES
Algoritmos 31-38: Arquitecturas y algoritmos de redes neuronales
"""

import random
import math
import numpy as np

# ============================================================================
# 31. COMPUTACIÓN NEURONAL
# ============================================================================

class Neurona:
    """
    Modelo de neurona artificial básica
    """
    def __init__(self, num_entradas):
        # Inicializar pesos aleatoriamente
        self.pesos = [random.uniform(-1, 1) for _ in range(num_entradas)]
        self.bias = random.uniform(-1, 1)
    
    def calcular_salida(self, entradas, funcion_activacion):
        """
        Calcula salida de la neurona
        Args:
            entradas: vector de entradas
            funcion_activacion: función a aplicar
        Returns:
            salida activada
        """
        # Suma ponderada
        suma = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        
        # Aplicar función de activación
        return funcion_activacion(suma)
    
    def actualizar_pesos(self, delta, entradas, tasa_aprendizaje):
        """Actualiza pesos usando regla delta"""
        for i in range(len(self.pesos)):
            self.pesos[i] += tasa_aprendizaje * delta * entradas[i]
        self.bias += tasa_aprendizaje * delta


def modelo_mcculloch_pitts(entradas, pesos, umbral):
    """
    Modelo de neurona de McCulloch-Pitts (1943)
    Args:
        entradas: vector binario de entradas
        pesos: pesos de conexiones
        umbral: umbral de activación
    Returns:
        1 si activa, 0 si no
    """
    suma = sum(w * x for w, x in zip(pesos, entradas))
    return 1 if suma >= umbral else 0


# ============================================================================
# 32. FUNCIONES DE ACTIVACIÓN
# ============================================================================

def funcion_escalon(x):
    """Función escalón (step function)"""
    return 1 if x >= 0 else 0


def funcion_sigmoide(x):
    """Función sigmoide (logística)"""
    return 1 / (1 + math.exp(-x))


def derivada_sigmoide(x):
    """Derivada de la función sigmoide"""
    s = funcion_sigmoide(x)
    return s * (1 - s)


def funcion_tanh(x):
    """Función tangente hiperbólica"""
    return math.tanh(x)


def derivada_tanh(x):
    """Derivada de tanh"""
    t = math.tanh(x)
    return 1 - t**2


def funcion_relu(x):
    """Rectified Linear Unit"""
    return max(0, x)


def derivada_relu(x):
    """Derivada de ReLU"""
    return 1 if x > 0 else 0


def funcion_leaky_relu(x, alpha=0.01):
    """Leaky ReLU"""
    return x if x > 0 else alpha * x


def funcion_softmax(vector):
    """
    Función softmax para clasificación multiclase
    Args:
        vector: vector de valores
    Returns:
        probabilidades normalizadas
    """
    # Evitar overflow
    exp_vals = [math.exp(x - max(vector)) for x in vector]
    suma = sum(exp_vals)
    return [e / suma for e in exp_vals]


# ============================================================================
# 33. PERCEPTRÓN, ADALINE Y MADALINE
# ============================================================================

class Perceptron:
    """
    Perceptrón de Rosenblatt (1958)
    """
    def __init__(self, num_entradas, tasa_aprendizaje=0.1):
        self.pesos = [random.uniform(-1, 1) for _ in range(num_entradas)]
        self.bias = random.uniform(-1, 1)
        self.lr = tasa_aprendizaje
    
    def predecir(self, entradas):
        """Predice clase (0 o 1)"""
        suma = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        return 1 if suma >= 0 else 0
    
    def entrenar(self, X, y, epochs=100):
        """
        Entrena el perceptrón
        Args:
            X: matriz de características
            y: vector de etiquetas (0 o 1)
            epochs: número de épocas
        """
        for epoch in range(epochs):
            errores = 0
            for entradas, etiqueta in zip(X, y):
                prediccion = self.predecir(entradas)
                error = etiqueta - prediccion
                
                if error != 0:
                    # Actualizar pesos
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self.lr * error * entradas[i]
                    self.bias += self.lr * error
                    errores += 1
            
            if errores == 0:
                print(f"   Convergió en época {epoch}")
                break


class Adaline:
    """
    ADALINE (Adaptive Linear Neuron) - Widrow & Hoff
    """
    def __init__(self, num_entradas, tasa_aprendizaje=0.01):
        self.pesos = [random.uniform(-0.5, 0.5) for _ in range(num_entradas)]
        self.bias = 0
        self.lr = tasa_aprendizaje
    
    def activacion(self, x):
        """Función de activación lineal"""
        return x
    
    def predecir(self, entradas):
        """Predice valor continuo"""
        suma = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        return self.activacion(suma)
    
    def entrenar(self, X, y, epochs=100):
        """Entrena usando regla delta (Widrow-Hoff)"""
        for epoch in range(epochs):
            error_total = 0
            
            for entradas, objetivo in zip(X, y):
                salida = self.predecir(entradas)
                error = objetivo - salida
                
                # Actualizar pesos (regla delta)
                for i in range(len(self.pesos)):
                    self.pesos[i] += self.lr * error * entradas[i]
                self.bias += self.lr * error
                
                error_total += error ** 2
            
            if epoch % 10 == 0:
                mse = error_total / len(X)
                if mse < 0.01:
                    break


class Madaline:
    """
    MADALINE (Multiple ADALINE) - red multicapa
    """
    def __init__(self, num_entradas, num_ocultas, tasa_aprendizaje=0.01):
        # Capa oculta de ADALINEs
        self.capa_oculta = [Adaline(num_entradas, tasa_aprendizaje) 
                           for _ in range(num_ocultas)]
        # ADALINE de salida
        self.salida = Adaline(num_ocultas, tasa_aprendizaje)
    
    def predecir(self, entradas):
        """Predicción forward"""
        # Salidas de capa oculta
        ocultas = [adaline.predecir(entradas) for adaline in self.capa_oculta]
        # Salida final
        return self.salida.predecir(ocultas)


# ============================================================================
# 34. SEPARABILIDAD LINEAL
# ============================================================================

def es_linealmente_separable(X, y):
    """
    Verifica si un conjunto de datos es linealmente separable
    Args:
        X: matriz de características
        y: vector de etiquetas
    Returns:
        True si es linealmente separable
    """
    # Intentar entrenar un perceptrón
    perceptron = Perceptron(len(X[0]))
    
    max_epochs = 1000
    for epoch in range(max_epochs):
        errores = 0
        for entradas, etiqueta in zip(X, y):
            prediccion = perceptron.predecir(entradas)
            if prediccion != etiqueta:
                errores += 1
                # Actualizar
                error = etiqueta - prediccion
                for i in range(len(perceptron.pesos)):
                    perceptron.pesos[i] += perceptron.lr * error * entradas[i]
                perceptron.bias += perceptron.lr * error
        
        if errores == 0:
            return True  # Convergió, es linealmente separable
    
    return False  # No convergió


def problema_xor():
    """
    Demuestra que XOR no es linealmente separable
    """
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 0]
    
    return es_linealmente_separable(X, y)


# ============================================================================
# 35. REDES MULTICAPA
# ============================================================================

class RedMulticapa:
    """
    Red neuronal multicapa (Multilayer Perceptron)
    """
    def __init__(self, capas, tasa_aprendizaje=0.1):
        """
        Args:
            capas: lista con número de neuronas por capa [entrada, oculta1, ..., salida]
            tasa_aprendizaje: tasa de aprendizaje
        """
        self.lr = tasa_aprendizaje
        self.num_capas = len(capas)
        
        # Inicializar pesos entre capas
        self.pesos = []
        self.bias = []
        
        for i in range(len(capas) - 1):
            # Matriz de pesos: [capa_actual x capa_siguiente]
            w = [[random.uniform(-1, 1) for _ in range(capas[i+1])] 
                 for _ in range(capas[i])]
            b = [random.uniform(-1, 1) for _ in range(capas[i+1])]
            
            self.pesos.append(w)
            self.bias.append(b)
        
        # Almacenar activaciones para backprop
        self.activaciones = []
        self.z_values = []
    
    def forward(self, entradas):
        """Propagación hacia adelante"""
        self.activaciones = [entradas]
        self.z_values = []
        
        activacion = entradas
        
        for i in range(len(self.pesos)):
            # Calcular z = W·a + b
            z = []
            for j in range(len(self.pesos[i][0])):
                suma = sum(self.pesos[i][k][j] * activacion[k] 
                          for k in range(len(activacion)))
                suma += self.bias[i][j]
                z.append(suma)
            
            self.z_values.append(z)
            
            # Aplicar función de activación
            activacion = [funcion_sigmoide(zi) for zi in z]
            self.activaciones.append(activacion)
        
        return activacion
    
    def predecir(self, entradas):
        """Predice salida"""
        return self.forward(entradas)


# ============================================================================
# 36. RETROPROPAGACIÓN DEL ERROR
# ============================================================================

class RedBackpropagation(RedMulticapa):
    """
    Red neuronal con algoritmo de retropropagación
    """
    
    def backward(self, y_real):
        """
        Retropropagación del error
        Args:
            y_real: valor objetivo
        """
        # Calcular deltas (errores) por capa
        deltas = [None] * len(self.pesos)
        
        # Delta de la capa de salida
        error_salida = []
        capa_salida = self.activaciones[-1]
        z_salida = self.z_values[-1]
        
        for i in range(len(capa_salida)):
            error = capa_salida[i] - y_real[i]
            delta = error * derivada_sigmoide(z_salida[i])
            error_salida.append(delta)
        
        deltas[-1] = error_salida
        
        # Deltas de capas ocultas (hacia atrás)
        for capa in range(len(self.pesos) - 2, -1, -1):
            delta_capa = []
            
            for i in range(len(self.pesos[capa][0])):
                error = sum(deltas[capa + 1][j] * self.pesos[capa + 1][i][j] 
                           for j in range(len(deltas[capa + 1])))
                delta = error * derivada_sigmoide(self.z_values[capa][i])
                delta_capa.append(delta)
            
            deltas[capa] = delta_capa
        
        # Actualizar pesos y bias
        for capa in range(len(self.pesos)):
            for i in range(len(self.pesos[capa])):
                for j in range(len(self.pesos[capa][i])):
                    grad = deltas[capa][j] * self.activaciones[capa][i]
                    self.pesos[capa][i][j] -= self.lr * grad
            
            for j in range(len(self.bias[capa])):
                self.bias[capa][j] -= self.lr * deltas[capa][j]
    
    def entrenar(self, X, y, epochs=1000):
        """
        Entrena la red
        Args:
            X: datos de entrada
            y: etiquetas objetivo
            epochs: número de épocas
        """
        for epoch in range(epochs):
            error_total = 0
            
            for entradas, objetivo in zip(X, y):
                # Forward
                salida = self.forward(entradas)
                
                # Calcular error
                error = sum((s - o)**2 for s, o in zip(salida, objetivo))
                error_total += error
                
                # Backward
                self.backward(objetivo)
            
            if epoch % 100 == 0:
                mse = error_total / len(X)
                print(f"   Época {epoch}: Error = {mse:.4f}")
                
                if mse < 0.01:
                    break


# ============================================================================
# 37. MAPAS AUTOORGANIZADOS DE KOHONEN (SOM)
# ============================================================================

class MapaKohonen:
    """
    Mapa autoorganizado de Kohonen (Self-Organizing Map)
    """
    def __init__(self, filas, columnas, dim_entrada, tasa_inicial=0.5):
        self.filas = filas
        self.columnas = columnas
        self.dim_entrada = dim_entrada
        self.tasa_inicial = tasa_inicial
        
        # Inicializar pesos aleatoriamente
        self.pesos = [[[random.random() for _ in range(dim_entrada)] 
                      for _ in range(columnas)] 
                     for _ in range(filas)]
    
    def distancia_euclidiana(self, v1, v2):
        """Calcula distancia euclidiana"""
        return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))
    
    def encontrar_bmu(self, entrada):
        """
        Encuentra la Best Matching Unit (neurona ganadora)
        Args:
            entrada: vector de entrada
        Returns:
            (fila, columna) de la BMU
        """
        min_dist = float('inf')
        bmu = (0, 0)
        
        for i in range(self.filas):
            for j in range(self.columnas):
                dist = self.distancia_euclidiana(entrada, self.pesos[i][j])
                if dist < min_dist:
                    min_dist = dist
                    bmu = (i, j)
        
        return bmu
    
    def funcion_vecindad(self, dist, radio):
        """Función de vecindad gaussiana"""
        return math.exp(-(dist**2) / (2 * radio**2))
    
    def entrenar(self, datos, num_iteraciones=1000):
        """
        Entrena el mapa autoorganizado
        Args:
            datos: lista de vectores de entrada
            num_iteraciones: iteraciones de entrenamiento
        """
        radio_inicial = max(self.filas, self.columnas) / 2
        
        for iteracion in range(num_iteraciones):
            # Decaimiento de parámetros
            tasa = self.tasa_inicial * (1 - iteracion / num_iteraciones)
            radio = radio_inicial * (1 - iteracion / num_iteraciones)
            
            # Tomar muestra aleatoria
            entrada = random.choice(datos)
            
            # Encontrar BMU
            bmu_i, bmu_j = self.encontrar_bmu(entrada)
            
            # Actualizar pesos de vecindad
            for i in range(self.filas):
                for j in range(self.columnas):
                    # Distancia a BMU en el mapa
                    dist_bmu = math.sqrt((i - bmu_i)**2 + (j - bmu_j)**2)
                    
                    if dist_bmu <= radio:
                        influencia = self.funcion_vecindad(dist_bmu, radio)
                        
                        # Actualizar pesos
                        for k in range(self.dim_entrada):
                            self.pesos[i][j][k] += tasa * influencia * \
                                                   (entrada[k] - self.pesos[i][j][k])
    
    def mapear(self, entrada):
        """Mapea una entrada a una posición en el mapa"""
        return self.encontrar_bmu(entrada)


# ============================================================================
# 38. HAMMING, HOPFIELD, HEBB, BOLTZMANN
# ============================================================================

class RedHamming:
    """
    Red de Hamming para reconocimiento de patrones
    """
    def __init__(self, patrones):
        """
        Args:
            patrones: lista de patrones a memorizar (vectores binarios)
        """
        self.patrones = patrones
        self.num_patrones = len(patrones)
        self.dim = len(patrones[0])
    
    def distancia_hamming(self, p1, p2):
        """Calcula distancia de Hamming"""
        return sum(a != b for a, b in zip(p1, p2))
    
    def reconocer(self, entrada):
        """Reconoce el patrón más cercano"""
        min_dist = float('inf')
        mejor_patron = None
        
        for patron in self.patrones:
            dist = self.distancia_hamming(entrada, patron)
            if dist < min_dist:
                min_dist = dist
                mejor_patron = patron
        
        return mejor_patron


class RedHopfield:
    """
    Red de Hopfield para memoria asociativa
    """
    def __init__(self, num_neuronas):
        self.n = num_neuronas
        self.pesos = [[0 for _ in range(num_neuronas)] 
                     for _ in range(num_neuronas)]
    
    def entrenar_hebb(self, patrones):
        """
        Entrena la red usando regla de Hebb
        Args:
            patrones: lista de patrones bipolares (-1, 1)
        """
        # Inicializar pesos a 0
        self.pesos = [[0 for _ in range(self.n)] for _ in range(self.n)]
        
        # Regla de Hebb: w_ij = Σ x_i * x_j
        for patron in patrones:
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        self.pesos[i][j] += patron[i] * patron[j]
        
        # Normalizar
        num_patrones = len(patrones)
        for i in range(self.n):
            for j in range(self.n):
                self.pesos[i][j] /= num_patrones
    
    def actualizar_asincrono(self, estado):
        """Actualización asíncrona (una neurona a la vez)"""
        nuevo_estado = list(estado)
        
        for i in range(self.n):
            suma = sum(self.pesos[i][j] * nuevo_estado[j] 
                      for j in range(self.n))
            nuevo_estado[i] = 1 if suma >= 0 else -1
        
        return nuevo_estado
    
    def recuperar(self, patron_ruidoso, max_iter=100):
        """
        Recupera patrón completo desde patrón parcial/ruidoso
        Args:
            patron_ruidoso: patrón de entrada (puede tener ruido)
            max_iter: iteraciones máximas
        Returns:
            patrón recuperado
        """
        estado = list(patron_ruidoso)
        
        for _ in range(max_iter):
            nuevo_estado = self.actualizar_asincrono(estado)
            
            # Verificar convergencia
            if nuevo_estado == estado:
                break
            
            estado = nuevo_estado
        
        return estado


class MaquinaBoltzmann:
    """
    Máquina de Boltzmann (versión simplificada)
    """
    def __init__(self, num_visibles, num_ocultas, temperatura=1.0):
        self.nv = num_visibles
        self.nh = num_ocultas
        self.T = temperatura
        
        # Pesos entre capas
        self.pesos = [[random.uniform(-0.1, 0.1) for _ in range(num_ocultas)] 
                     for _ in range(num_visibles)]
    
    def probabilidad_activacion(self, entrada):
        """Probabilidad de activación estocástica"""
        return 1 / (1 + math.exp(-entrada / self.T))
    
    def muestrear_ocultas(self, visibles):
        """Muestrea unidades ocultas dado visibles"""
        ocultas = []
        
        for j in range(self.nh):
            suma = sum(self.pesos[i][j] * visibles[i] for i in range(self.nv))
            prob = self.probabilidad_activacion(suma)
            ocultas.append(1 if random.random() < prob else 0)
        
        return ocultas
    
    def muestrear_visibles(self, ocultas):
        """Muestrea unidades visibles dado ocultas"""
        visibles = []
        
        for i in range(self.nv):
            suma = sum(self.pesos[i][j] * ocultas[j] for j in range(self.nh))
            prob = self.probabilidad_activacion(suma)
            visibles.append(1 if random.random() < prob else 0)
        
        return visibles


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== REDES NEURONALES ===\n")
    
    # Ejemplo 32: Funciones de activación
    print("32. Funciones de Activación:")
    x_vals = [-2, -1, 0, 1, 2]
    print(f"   x: {x_vals}")
    print(f"   Sigmoide: {[funcion_sigmoide(x) for x in x_vals]}")
    print(f"   ReLU: {[funcion_relu(x) for x in x_vals]}")
    print(f"   Tanh: {[funcion_tanh(x) for x in x_vals]}")
    print()
    
    # Ejemplo 33: Perceptrón
    print("33. Perceptrón (AND lógico):")
    X_and = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_and = [0, 0, 0, 1]
    
    perceptron = Perceptron(2, tasa_aprendizaje=0.1)
    perceptron.entrenar(X_and, y_and, epochs=100)
    
    print("   Predicciones:")
    for x, y_real in zip(X_and, y_and):
        pred = perceptron.predecir(x)
        print(f"      {x} -> {pred} (esperado: {y_real})")
    print()
    
    # Ejemplo 34: Separabilidad lineal
    print("34. Separabilidad Lineal:")
    xor_separable = problema_xor()
    print(f"   ¿XOR es linealmente separable? {xor_separable}")
    print("   (Falso, por eso se necesitan redes multicapa)")
    print()
    
    # Ejemplo 36: Backpropagation (XOR)
    print("36. Retropropagación (resolver XOR):")
    X_xor = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_xor = [[0], [1], [1], [0]]
    
    red_bp = RedBackpropagation([2, 4, 1], tasa_aprendizaje=0.5)
    red_bp.entrenar(X_xor, y_xor, epochs=500)
    
    print("\n   Predicciones finales:")
    for x, y_real in zip(X_xor, y_xor):
        pred = red_bp.predecir(x)
        print(f"      {x} -> {pred[0]:.3f} (esperado: {y_real[0]})")
    print()
    
    # Ejemplo 38: Red de Hopfield
    print("38. Red de Hopfield:")
    # Memorizar patrones
    patron1 = [1, 1, -1, -1]
    patron2 = [-1, -1, 1, 1]
    
    hopfield = RedHopfield(4)
    hopfield.entrenar_hebb([patron1, patron2])
    
    # Probar con patrón ruidoso
    ruidoso = [1, -1, -1, -1]  # Similar a patron1 pero con ruido
    recuperado = hopfield.recuperar(ruidoso)
    
    print(f"   Patrón memorizado 1: {patron1}")
    print(f"   Patrón ruidoso: {ruidoso}")
    print(f"   Patrón recuperado: {recuperado}")