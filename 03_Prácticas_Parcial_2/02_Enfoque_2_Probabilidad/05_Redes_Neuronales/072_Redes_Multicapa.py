import random
import math

# ============================================================================
# 32. FUNCIONES DE ACTIVACIÓN (DEPENDENCIA)
# ============================================================================
def funcion_sigmoide(x):
    try: return 1 / (1 + math.exp(-x))
    except OverflowError: return 0 if x < 0 else 1

# ============================================================================
# 35. REDES MULTICAPA
# ============================================================================

class RedMulticapa:
    """
    Red neuronal multicapa (Multilayer Perceptron - MLP)
    Implementación básica sin backpropagation aún.
    """
    def __init__(self, capas):
        """
        Args:
            capas: lista con número de neuronas por capa [entrada, oculta1, ..., salida]
        """
        self.num_capas = len(capas)
        self.capas = capas
        
        # Inicializar pesos y biases aleatoriamente
        self.pesos = []
        self.biases = []
        
        # Pesos entre capa i y capa i+1
        for i in range(len(capas) - 1):
            # Matriz de pesos W: [neuronas_capa_siguiente x neuronas_capa_actual]
            # (Más común en librerías, pero la implementación original era al revés)
            # Adaptamos a la implementación original: [neuronas_capa_actual x neuronas_capa_siguiente]
            w = [[random.uniform(-0.5, 0.5) for _ in range(capas[i+1])] 
                 for _ in range(capas[i])]
            b = [random.uniform(-0.5, 0.5) for _ in range(capas[i+1])]
            
            self.pesos.append(w)
            self.biases.append(b)
        
        # Almacenar activaciones intermedias (útil para backprop)
        self.activaciones_capas = [] # Guardará la salida de cada capa
        self.z_valores_capas = []    # Guardará la entrada neta (antes de activar)

    def forward(self, entradas):
        """Propagación hacia adelante"""
        # Asegurarse que las entradas sean una lista
        a = list(entradas)
        
        self.activaciones_capas = [a]
        self.z_valores_capas = []
        
        # Iterar a través de las capas (excepto la de entrada)
        for i in range(len(self.pesos)):
            pesos_capa = self.pesos[i]
            bias_capa = self.biases[i]
            
            # Calcular entrada neta (z) para la siguiente capa
            # z = W^T * a + b  (Si W es [sig x act])
            # O z = a * W + b (Si W es [act x sig]) <-- Usaremos esta por consistencia
            
            z = [0.0] * len(bias_capa) # Inicializar z para la capa siguiente
            
            for j in range(len(bias_capa)): # Neurona j en la capa siguiente
                suma_ponderada = sum(a[k] * pesos_capa[k][j] for k in range(len(a)))
                z[j] = suma_ponderada + bias_capa[j]

            self.z_valores_capas.append(z)
            
            # Aplicar función de activación (sigmoide por defecto)
            a = [funcion_sigmoide(zi) for zi in z]
            self.activaciones_capas.append(a)
            
        return a # Salida final
    
    def predecir(self, entradas):
        """Alias para forward, devuelve la salida de la red"""
        return self.forward(entradas)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 35. Redes Multicapa (MLP - Solo Forward Pass) ===\n")
    
    # Definir arquitectura: 2 entradas, 3 neuronas ocultas, 1 salida
    arquitectura = [2, 3, 1]
    mlp = RedMulticapa(arquitectura)
    
    print(f"   Red creada con arquitectura: {arquitectura}")
    print(f"   Número de capas de pesos: {len(mlp.pesos)}")
    print(f"   Dimensiones W1: {len(mlp.pesos[0])}x{len(mlp.pesos[0][0])}")
    print(f"   Dimensiones b1: {len(mlp.biases[0])}")
    print(f"   Dimensiones W2: {len(mlp.pesos[1])}x{len(mlp.pesos[1][0])}")
    print(f"   Dimensiones b2: {len(mlp.biases[1])}\n")

    # Probar forward pass
    entrada_ejemplo = [0.5, -0.2]
    salida = mlp.predecir(entrada_ejemplo)
    
    print(f"   Entrada: {entrada_ejemplo}")
    print(f"   Salida de la red (sin entrenar): {[f'{s:.3f}' for s in salida]}")