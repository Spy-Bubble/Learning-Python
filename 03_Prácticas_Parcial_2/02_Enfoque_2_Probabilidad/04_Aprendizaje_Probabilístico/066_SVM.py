import math
import random # Puede ser útil para inicializar o SGD

# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================

def kernel_rbf(x1, x2, gamma=0.1):
    """
    Kernel RBF (Radial Basis Function)
    """
    dist_sq = sum((a - b)**2 for a, b in zip(x1, x2))
    return math.exp(-gamma * dist_sq)

# ============================================================================
# 29. MÁQUINAS DE VECTORES SOPORTE (NÚCLEO)
# ============================================================================

class SVM:
    """
    SVM simple con kernel lineal (descenso de gradiente estocástico)
    """
    def __init__(self, learning_rate=0.001, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param # Parámetro de regularización
        self.n_iters = n_iters
        self.w = None # Pesos
        self.b = None # Bias
    
    def _producto_punto(self, x1, x2):
        """Producto punto de dos vectores"""
        return sum(a * b for a, b in zip(x1, x2))

    def entrenar(self, X, y):
        """
        Entrena el SVM usando descenso de gradiente para la hinge loss
        Args:
            X: matriz de características (lista de listas)
            y: vector de etiquetas (-1 o 1)
        """
        n_samples, n_features = len(X), len(X[0])
        
        # Inicializar pesos
        self.w = [0.0] * n_features
        self.b = 0
        
        # Asegurar etiquetas -1 y 1
        y_mapped = [1 if yi >= 0 else -1 for yi in y]
        
        # Descenso de gradiente estocástico
        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                # Calcular condición de margen: y_i * (w.x_i - b) >= 1
                linear_output = self._producto_punto(x_i, self.w) - self.b
                condition = y_mapped[idx] * linear_output >= 1
                
                # Calcular gradientes
                if condition:
                    # Punto fuera del margen o correctamente clasificado
                    dw = [2 * self.lambda_param * w_j for w_j in self.w]
                    db = 0
                else:
                    # Punto viola el margen
                    dw = [2 * self.lambda_param * w_j - y_mapped[idx] * x_i[j] 
                          for j, w_j in enumerate(self.w)]
                    db = -y_mapped[idx]
                
                # Actualizar pesos y bias
                self.w = [w_j - self.lr * dw_j for w_j, dw_j in zip(self.w, dw)]
                self.b -= self.lr * db
    
    def predecir(self, X):
        """Predice etiquetas para nuevas muestras"""
        if self.w is None:
            raise Exception("SVM no entrenado.")
            
        linear_output = [self._producto_punto(x, self.w) - self.b for x in X]
        # Signo de la salida determina la clase
        return [1 if s >= 0 else -1 for s in linear_output]

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 29. Máquinas de Vectores Soporte (SVM) ===\n")

    # Datos linealmente separables
    X_svm = [[1, 2], [2, 3], [3, 3], [6, 5], [7, 8], [8, 7]]
    y_svm = [-1, -1, -1, 1, 1, 1] # Clases -1 y 1

    svm = SVM(learning_rate=0.01, lambda_param=0.01, n_iters=1000)
    svm.entrenar(X_svm, y_svm)

    print(f"   Datos de entrenamiento: {X_svm}")
    print(f"   Etiquetas: {y_svm}")
    print(f"   Pesos aprendidos (w): {[f'{wi:.3f}' for wi in svm.w]}")
    print(f"   Bias aprendido (b): {svm.b:.3f}\n")

    # Predecir nuevos puntos
    X_test = [[0, 1], [4, 4], [8, 9]]
    predicciones = svm.predecir(X_test)
    print(f"   Predicciones para {X_test}: {predicciones}")

    # Ejemplo de Kernel RBF
    p1 = [1, 1]
    p2 = [2, 2]
    print(f"\n   Kernel RBF entre {p1} y {p2}: {kernel_rbf(p1, p2):.3f}")