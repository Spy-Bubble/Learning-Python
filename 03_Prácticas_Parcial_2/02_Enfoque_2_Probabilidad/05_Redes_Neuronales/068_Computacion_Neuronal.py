import random

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
        suma_ponderada = sum(w * x for w, x in zip(self.pesos, entradas)) + self.bias
        
        # Aplicar función de activación
        return funcion_activacion(suma_ponderada)
    
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
    suma_ponderada = sum(w * x for w, x in zip(pesos, entradas))
    return 1 if suma_ponderada >= umbral else 0

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

# Función de activación de ejemplo (escalón)
def funcion_escalon_simple(x):
    return 1 if x >= 0 else 0

if __name__ == "__main__":
    print("=== 31. Computación Neuronal ===\n")

    # 1. Neurona Artificial Básica
    print("Neurona Artificial:")
    neurona = Neurona(num_entradas=2)
    entradas_ejemplo = [0.5, -0.2]
    salida = neurona.calcular_salida(entradas_ejemplo, funcion_escalon_simple)
    print(f"   Entradas: {entradas_ejemplo}")
    print(f"   Pesos iniciales: {[f'{w:.2f}' for w in neurona.pesos]}")
    print(f"   Bias inicial: {neurona.bias:.2f}")
    print(f"   Salida (con escalón): {salida}\n")

    # 2. Modelo McCulloch-Pitts (Compuerta AND)
    print("Modelo McCulloch-Pitts (AND):")
    pesos_and = [1, 1]
    umbral_and = 2
    
    entradas_mcp = [[0, 0], [0, 1], [1, 0], [1, 1]]
    print("   Entradas | Salida")
    print("   ---------|-------")
    for inp in entradas_mcp:
        salida_mcp = modelo_mcculloch_pitts(inp, pesos_and, umbral_and)
        print(f"   {inp[0]}, {inp[1]}    |   {salida_mcp}")