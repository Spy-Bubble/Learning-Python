import random
import math
import numpy as np # Numpy es casi indispensable para redes neuronales

# ============================================================================
# 30. APRENDIZAJE PROFUNDO (DEEP LEARNING)
# ============================================================================

class RedNeuronalSimple:
    """
    Red neuronal simple (feedforward) con 1 capa oculta (usando Numpy)
    """
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.lr = learning_rate
        
        # Inicializar pesos aleatoriamente (mejoras: Xavier/He)
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        
        # Variables para guardar activaciones intermedias (cache)
        self.cache = {}

    def _sigmoid(self, x):
        """Función de activación sigmoide"""
        return 1 / (1 + np.exp(-x))
    
    def _sigmoid_derivada(self, sigmoid_output):
        """Derivada de sigmoide (usa la salida de sigmoide)"""
        return sigmoid_output * (1 - sigmoid_output)
    
    def forward(self, X):
        """Propagación hacia adelante"""
        # Asegurar que X es un array de numpy 2D
        X = np.array(X)
        if X.ndim == 1:
            X = X.reshape(1, -1) # Convertir vector fila a matriz 1xN

        # Capa oculta
        z1 = X @ self.W1 + self.b1
        a1 = self._sigmoid(z1)
        
        # Capa de salida
        z2 = a1 @ self.W2 + self.b2
        a2 = self._sigmoid(z2) # Usar Softmax para clasificación multiclase
        
        # Guardar en cache para backpropagation
        self.cache['X'] = X
        self.cache['z1'] = z1
        self.cache['a1'] = a1
        self.cache['z2'] = z2
        self.cache['a2'] = a2
        
        return a2
    
    def backward(self, y):
        """Retropropagación del error"""
        m = self.cache['X'].shape[0] # Número de ejemplos (batch size)
        
        # Asegurar que y es un array de numpy 2D
        y = np.array(y)
        if y.ndim == 1:
            y = y.reshape(-1, self.b2.shape[1]) # Convertir a matriz NxOutput

        # Error en capa de salida (dC/da2 * da2/dz2)
        # Asumiendo Mean Squared Error: dC/da2 = a2 - y
        delta2 = (self.cache['a2'] - y) * self._sigmoid_derivada(self.cache['a2'])
        
        # Gradientes para W2 y b2
        dW2 = (self.cache['a1'].T @ delta2) / m
        db2 = np.sum(delta2, axis=0, keepdims=True) / m
        
        # Error en capa oculta (dC/da2 * da2/dz2 * dz2/da1 * da1/dz1)
        delta1 = (delta2 @ self.W2.T) * self._sigmoid_derivada(self.cache['a1'])
        
        # Gradientes para W1 y b1
        dW1 = (self.cache['X'].T @ delta1) / m
        db1 = np.sum(delta1, axis=0, keepdims=True) / m
        
        # Actualizar pesos (descenso de gradiente)
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
    
    def entrenar(self, X, y, epochs=1000):
        """Entrena la red usando forward y backward"""
        for epoch in range(epochs):
            # En una red real, se usarían batches
            self.forward(X)
            self.backward(y)
            
            # Opcional: Calcular y mostrar pérdida (loss)
            if epoch % 100 == 0:
                 y_pred = self.forward(X)
                 loss = np.mean((y_pred - y)**2) # MSE Loss
                 # print(f"Epoch {epoch}, Loss: {loss:.4f}")

    def predecir(self, X):
         """Realiza predicciones"""
         output = self.forward(X)
         # Convertir salida sigmoide a clase (ej. umbral 0.5)
         return (output > 0.5).astype(int)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 30. Aprendizaje Profundo (Red Neuronal Simple) ===\n")
    
    # Aprender función XOR
    X_nn = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_nn = np.array([[0], [1], [1], [0]]) # Vector columna
    
    input_dim = X_nn.shape[1]
    output_dim = y_nn.shape[1]
    hidden_dim = 4 # Tamaño de la capa oculta
    
    nn = RedNeuronalSimple(input_size=input_dim, 
                         hidden_size=hidden_dim, 
                         output_size=output_dim, 
                         learning_rate=0.5)
    
    print("Entrenando red neuronal en XOR...")
    nn.entrenar(X_nn, y_nn, epochs=10000)
    print("Entrenamiento completado.\n")
    
    print("   Predicciones en datos de entrenamiento:")
    for x, y_true in zip(X_nn, y_nn):
        y_pred_prob = nn.forward(x) # Probabilidad
        y_pred_class = (y_pred_prob > 0.5).astype(int) # Clase
        print(f"      Input: {x}, Esperado: {y_true[0]}, Pred. Prob: {y_pred_prob[0][0]:.3f}, Pred. Clase: {y_pred_class[0][0]}")