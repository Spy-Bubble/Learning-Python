import random

# ============================================================================
# 33. PERCEPTRÓN, ADALINE Y MADALINE
# ============================================================================

class Perceptron:
    """
    Perceptrón de Rosenblatt (1958) - Clasificación binaria
    """
    def __init__(self, num_entradas, tasa_aprendizaje=0.1):
        self.pesos = [random.uniform(-1, 1) for _ in range(num_entradas)]
        self.bias = random.uniform(-1, 1)
        self.lr = tasa_aprendizaje
    
    def predecir(self, entradas):
        """Predice clase (0 o 1) usando función escalón"""
        suma_ponderada = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        return 1 if suma_ponderada >= 0 else 0
    
    def entrenar(self, X, y, epochs=100):
        """
        Entrena el perceptrón usando la regla del perceptrón
        Args:
            X: matriz de características (lista de listas)
            y: vector de etiquetas (0 o 1)
            epochs: número de épocas
        Returns:
            True si convergió, False si no.
        """
        for epoch in range(epochs):
            errores_epoca = 0
            for entradas, etiqueta in zip(X, y):
                prediccion = self.predecir(entradas)
                error = etiqueta - prediccion
                
                if error != 0:
                    # Actualizar pesos
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self.lr * error * entradas[i]
                    self.bias += self.lr * error
                    errores_epoca += 1
            
            # Si no hubo errores en una época, convergió
            if errores_epoca == 0:
                print(f"   (Perceptrón convergió en época {epoch+1})")
                return True
        print(f"   (Perceptrón no convergió después de {epochs} épocas)")
        return False


class Adaline:
    """
    ADALINE (Adaptive Linear Neuron) - Widrow & Hoff
    """
    def __init__(self, num_entradas, tasa_aprendizaje=0.01):
        self.pesos = [random.uniform(-0.5, 0.5) for _ in range(num_entradas)]
        self.bias = 0.0 # Bias a menudo se inicializa en 0
        self.lr = tasa_aprendizaje
    
    def _activacion_lineal(self, x):
        """Función de activación lineal (identidad)"""
        return x
    
    def _suma_ponderada(self, entradas):
        """Calcula la entrada neta a la neurona"""
        return sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias

    def predecir(self, entradas):
        """Predice valor continuo (salida lineal)"""
        net_input = self._suma_ponderada(entradas)
        return self._activacion_lineal(net_input)
    
    def entrenar(self, X, y, epochs=100, tol=0.01):
        """Entrena usando regla delta (Widrow-Hoff) - Descenso Gradiente"""
        costos = []
        for epoch in range(epochs):
            error_total_epoca = 0
            
            # Descenso de gradiente en batch (actualizar después de ver todos)
            delta_w = [0.0] * len(self.pesos)
            delta_b = 0.0

            for entradas, objetivo in zip(X, y):
                salida_lineal = self._suma_ponderada(entradas) # Net input
                error = objetivo - salida_lineal
                
                # Acumular gradientes
                for i in range(len(self.pesos)):
                    delta_w[i] += error * entradas[i]
                delta_b += error
                
                error_total_epoca += error**2

            # Actualizar pesos y bias (promediando gradientes)
            n_samples = len(X)
            for i in range(len(self.pesos)):
                self.pesos[i] += self.lr * delta_w[i] / n_samples
            self.bias += self.lr * delta_b / n_samples
            
            mse = error_total_epoca / n_samples
            costos.append(mse)
            
            # Condición de parada (opcional)
            if mse < tol:
                 print(f"   (Adaline convergió en época {epoch+1} con MSE={mse:.4f})")
                 break
        # print(f"   (Adaline terminó entrenamiento con MSE={mse:.4f})")
        return costos


class Madaline:
    """
    MADALINE (Multiple ADALINE) - red multicapa simple (conceptual)
    """
    def __init__(self, num_entradas, num_ocultas, tasa_aprendizaje=0.01):
        # Capa oculta de ADALINEs
        self.capa_oculta = [Adaline(num_entradas, tasa_aprendizaje) 
                           for _ in range(num_ocultas)]
        # ADALINE de salida (o podría ser otra neurona)
        self.salida = Adaline(num_ocultas, tasa_aprendizaje)
    
    def predecir(self, entradas):
        """Predicción forward"""
        # Salidas de capa oculta
        salidas_ocultas = [adaline.predecir(entradas) for adaline in self.capa_oculta]
        # Salida final
        return self.salida.predecir(salidas_ocultas)

    # Nota: El entrenamiento de MADALINE es más complejo que entrenar
    # Adalines individuales (ej. regla MRI, backpropagation).
    # Esta clase es más una demostración estructural.

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 33. Perceptrón, Adaline y Madaline ===\n")
    
    # --- Perceptrón (AND lógico) ---
    print("Perceptrón (AND lógico):")
    X_and = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_and = [0, 0, 0, 1]
    
    perceptron = Perceptron(2, tasa_aprendizaje=0.1)
    perceptron.entrenar(X_and, y_and, epochs=20)
    
    print("   Predicciones:")
    for x, y_real in zip(X_and, y_and):
        pred = perceptron.predecir(x)
        print(f"      {x} -> {pred} (esperado: {y_real})")
    print()

    # --- Adaline (Regresión Lineal Simple) ---
    print("Adaline (Regresión Lineal Simple):")
    # Intentar aprender y = 2x + 1
    X_reg = [[1], [2], [3], [4], [5]]
    y_reg = [3, 5, 7, 9, 11]
    
    adaline = Adaline(1, tasa_aprendizaje=0.01)
    adaline.entrenar(X_reg, y_reg, epochs=100, tol=0.01)
    
    print(f"   Pesos aprendidos: w={adaline.pesos[0]:.2f}, b={adaline.bias:.2f} (esperado w=2, b=1)")
    print(f"   Predicción para x=6: {adaline.predecir([6]):.2f} (esperado: 13)\n")
    
    # --- Madaline (Estructura) ---
    print("Madaline (Estructura):")
    madaline = Madaline(num_entradas=2, num_ocultas=3, tasa_aprendizaje=0.01)
    print(f"   Madaline creado con 3 neuronas ocultas Adaline.")
    # (El entrenamiento no está implementado aquí)