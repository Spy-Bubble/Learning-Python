import random

# ============================================================================
# 33. PERCEPTRÓN (DEPENDENCIA)
# ============================================================================
class Perceptron:
    def __init__(self, num_entradas, tasa_aprendizaje=0.1):
        self.pesos = [random.uniform(-1, 1) for _ in range(num_entradas)]
        self.bias = random.uniform(-1, 1)
        self.lr = tasa_aprendizaje
    def predecir(self, entradas):
        suma_ponderada = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        return 1 if suma_ponderada >= 0 else 0
    # (Función entrenar simplificada para esta demo)

# ============================================================================
# 34. SEPARABILIDAD LINEAL
# ============================================================================

def es_linealmente_separable(X, y, max_epochs=1000, lr=0.1):
    """
    Verifica si un conjunto de datos binario es linealmente separable
    intentando entrenar un Perceptrón.
    Args:
        X: matriz de características (lista de listas)
        y: vector de etiquetas (0 o 1)
        max_epochs: número máximo de iteraciones
        lr: tasa de aprendizaje
    Returns:
        True si el Perceptrón converge (es linealmente separable), False si no.
    """
    if not X: return True # Vacío es separable
    
    perceptron = Perceptron(len(X[0]), tasa_aprendizaje=lr)
    
    for epoch in range(max_epochs):
        errores_epoca = 0
        for entradas, etiqueta in zip(X, y):
            prediccion = perceptron.predecir(entradas)
            error = etiqueta - prediccion
            
            if error != 0:
                # Actualizar pesos
                for i in range(len(perceptron.pesos)):
                    perceptron.pesos[i] += perceptron.lr * error * entradas[i]
                perceptron.bias += perceptron.lr * error
                errores_epoca += 1
        
        # Si no hubo errores en una época, convergió
        if errores_epoca == 0:
            return True
            
    return False # No convergió


def problema_xor():
    """
    Demuestra que XOR no es linealmente separable.
    """
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 0] # Etiquetas para XOR
    
    print("Verificando separabilidad lineal de XOR:")
    return es_linealmente_separable(X, y)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 34. Separabilidad Lineal ===\n")
    
    # 1. Compuerta AND (Linealmente Separable)
    print("Compuerta AND:")
    X_and = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y_and = [0, 0, 0, 1]
    and_separable = es_linealmente_separable(X_and, y_and)
    print(f"   ¿AND es linealmente separable? {and_separable}\n")

    # 2. Compuerta XOR (No Linealmente Separable)
    xor_separable = problema_xor()
    print(f"   ¿XOR es linealmente separable? {xor_separable}")
    print("   (Falso, el Perceptrón no puede converger)")