import random
import math

# ============================================================================
# 32. FUNCIONES DE ACTIVACIÓN (DEPENDENCIA)
# ============================================================================
def funcion_sigmoide(x):
    try: return 1 / (1 + math.exp(-x))
    except OverflowError: return 0 if x < 0 else 1

def derivada_sigmoide(x):
    # Corrección: La derivada se calcula a partir de la *salida* de la sigmoide, no de x directamente
    s = funcion_sigmoide(x)
    return s * (1 - s)

# ============================================================================
# 35. REDES MULTICAPA (DEPENDENCIA - versión simplificada)
# ============================================================================
class RedMulticapa:
    def __init__(self, capas, tasa_aprendizaje=0.1):
        self.lr = tasa_aprendizaje
        self.num_capas = len(capas)
        self.pesos = []
        self.biases = [] # Cambiado de 'bias' a 'biases' para consistencia
        for i in range(len(capas) - 1):
            w = [[random.uniform(-0.5, 0.5) for _ in range(capas[i+1])] for _ in range(capas[i])]
            b = [random.uniform(-0.5, 0.5) for _ in range(capas[i+1])]
            self.pesos.append(w)
            self.biases.append(b) # Cambiado de 'bias' a 'biases'
        self.activaciones_capas = []
        self.z_valores_capas = []

    def forward(self, entradas):
        a = list(entradas)
        self.activaciones_capas = [a]
        self.z_valores_capas = []
        for i in range(len(self.pesos)):
            pesos_capa = self.pesos[i]
            bias_capa = self.biases[i] # Cambiado de 'bias' a 'biases'
            z = [0.0] * len(bias_capa)
            for j in range(len(bias_capa)):
                suma_ponderada = sum(a[k] * pesos_capa[k][j] for k in range(len(a)))
                z[j] = suma_ponderada + bias_capa[j]
            self.z_valores_capas.append(z)
            a = [funcion_sigmoide(zi) for zi in z]
            self.activaciones_capas.append(a)
        return a

    # --- MÉTODO AÑADIDO ---
    def predecir(self, entradas):
        """Alias para forward, devuelve la salida de la red"""
        return self.forward(entradas)
    # --- FIN MÉTODO AÑADIDO ---

# ============================================================================
# 36. RETROPROPAGACIÓN DEL ERROR
# ============================================================================

class RedBackpropagation(RedMulticapa):
    """
    Red neuronal con algoritmo de retropropagación (backpropagation)
    Hereda de RedMulticapa.
    """

    def backward(self, y_real):
        """
        Retropropagación del error para calcular gradientes.
        Args:
            y_real: lista con los valores objetivo (debe tener la misma
                    dimensión que la capa de salida)
        """
        # Calcular deltas (errores ponderados) por capa, empezando por el final
        deltas = [None] * len(self.pesos)

        # --- Delta de la capa de salida (L) ---
        # delta_L = (a_L - y) * g'(z_L)
        error_salida_directo = []
        capa_salida_a = self.activaciones_capas[-1] # a_L
        capa_salida_z = self.z_valores_capas[-1]    # z_L

        for i in range(len(capa_salida_a)):
            error = capa_salida_a[i] - y_real[i]
            # Corrección: La derivada de sigmoide se calcula sobre Z, no sobre A
            derivada = capa_salida_a[i] * (1 - capa_salida_a[i]) # derivada_sigmoide(z) = a * (1-a)
            delta = error * derivada
            error_salida_directo.append(delta)

        deltas[-1] = error_salida_directo

        # --- Deltas de capas ocultas (hacia atrás) ---
        # delta_l = (W_{l+1}^T * delta_{l+1}) .* g'(z_l)
        for capa_idx in range(len(self.pesos) - 2, -1, -1):
            delta_capa_siguiente = deltas[capa_idx + 1]
            pesos_siguientes = self.pesos[capa_idx + 1] # Pesos W_{l+1}
            a_capa_actual = self.activaciones_capas[capa_idx + 1] # a_l (la activación de esta capa)

            delta_capa_actual = [0.0] * len(a_capa_actual)

            # Para cada neurona i en la capa actual l
            for i in range(len(a_capa_actual)):
                # Calcular Suma( w_{ji}^{l+1} * delta_j^{l+1} )
                # Nota: El índice original estaba al revés W[k][j] debería ser W[i][j] si W es act x sig
                # Si W[i][j] es neurona_previa i -> neurona_actual j
                error_propagado = sum(pesos_siguientes[i][j] * delta_capa_siguiente[j]
                                    for j in range(len(delta_capa_siguiente)))

                # Corrección: Derivada de sigmoide g'(z_l) = a_l * (1 - a_l)
                derivada = a_capa_actual[i] * (1 - a_capa_actual[i])
                delta_capa_actual[i] = error_propagado * derivada

            deltas[capa_idx] = delta_capa_actual

        # --- Calcular Gradientes y Actualizar Pesos/Biases ---
        # dW_l = delta_{l+1} * (a_l)^T
        # db_l = delta_{l+1}

        for capa_idx in range(len(self.pesos)):
            activacion_previa = self.activaciones_capas[capa_idx] # a_l
            delta_actual = deltas[capa_idx] # delta_{l+1}

            # Actualizar Biases
            for j in range(len(self.biases[capa_idx])):
                self.biases[capa_idx][j] -= self.lr * delta_actual[j]

            # Actualizar Pesos
            # Si W[k][j] es neurona_previa k -> neurona_actual j
            for k in range(len(activacion_previa)): # Neurona k en capa l (previa)
                for j in range(len(delta_actual)): # Neurona j en capa l+1 (actual)
                    grad_w = activacion_previa[k] * delta_actual[j]
                    self.pesos[capa_idx][k][j] -= self.lr * grad_w

    def entrenar(self, X, y, epochs=1000, tol=0.01):
        """
        Entrena la red usando forward y backward pass.
        Args:
            X: lista de datos de entrada (lista de listas)
            y: lista de etiquetas objetivo (lista de listas)
            epochs: número máximo de épocas
            tol: tolerancia de error para parada temprana
        """
        historial_error = []
        for epoch in range(epochs):
            error_total_epoca = 0

            for entradas, objetivo in zip(X, y):
                # 1. Forward pass
                salida = self.forward(entradas)

                # 2. Calcular error (ej. MSE)
                error_muestra = sum((s - o)**2 for s, o in zip(salida, objetivo)) / len(objetivo)
                error_total_epoca += error_muestra

                # 3. Backward pass (calcula gradientes y actualiza pesos)
                self.backward(objetivo)

            mse_epoca = error_total_epoca / len(X)
            historial_error.append(mse_epoca)

            if epoch % 100 == 0 or epoch == epochs - 1:
                print(f"   Época {epoch}: Error MSE = {mse_epoca:.6f}")

            # Parada temprana
            if mse_epoca < tol:
                print(f"   Convergencia alcanzada en época {epoch} con MSE={mse_epoca:.6f}")
                break
        return historial_error

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 36. Retropropagación del Error ===\n")

    # Resolver XOR
    print("Entrenando red para resolver XOR:")
    X_xor = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_xor = [[0], [1], [1], [0]]

    # Arquitectura: 2 entradas, 4 ocultas, 1 salida
    red_bp = RedBackpropagation([2, 4, 1], tasa_aprendizaje=0.5)
    hist_error = red_bp.entrenar(X_xor, y_xor, epochs=5000, tol=0.005)

    print("\n   Predicciones finales en XOR:")
    for x, y_real in zip(X_xor, y_xor):
        pred = red_bp.predecir(x) # Ahora debería encontrar el método
        print(f"      {x} -> {pred[0]:.3f} (esperado: {y_real[0]})")