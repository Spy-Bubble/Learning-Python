import random
import math

# ============================================================================
# 13. BÚSQUEDA DE TEMPLE SIMULADO
# ============================================================================

def temple_simulado(funcion_objetivo, estado_inicial, vecinos_func, 
                    temp_inicial=100, alpha=0.95, max_iter=1000):
    """
    Búsqueda probabilística inspirada en el recocido de metales
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado inicial
        vecinos_func: función generadora de vecinos
        temp_inicial: temperatura inicial
        alpha: factor de enfriamiento (0 < alpha < 1)
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    mejor = actual
    mejor_valor = funcion_objetivo(mejor)
    temperatura = temp_inicial
    
    for _ in range(max_iter):
        vecinos = vecinos_func(actual)
        if not vecinos:
            break
        
        vecino = random.choice(vecinos)
        valor_actual = funcion_objetivo(actual)
        valor_vecino = funcion_objetivo(vecino)
        
        delta = valor_vecino - valor_actual
        
        # Aceptar si mejora o con probabilidad decreciente
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual = vecino
            
            if valor_vecino > mejor_valor:
                mejor = vecino
                mejor_valor = valor_vecino
        
        # Enfriar
        temperatura *= alpha
    
    return mejor

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("13. Búsqueda de Temple Simulado:")
    
    # Función objetivo con múltiples máximos locales
    # f(x) = sin(x) + sin(x*2)
    def objetivo_sin(x):
        return math.sin(x) + math.sin(x * 2)

    # Función de vecinos: explorar cerca
    def vecinos_sin(x):
        return [x - 0.1, x + 0.1]
    
    # Iniciar en x=0
    resultado = temple_simulado(objetivo_sin, 0, vecinos_sin, 
                                temp_inicial=10, alpha=0.99, max_iter=2000)
    print(f"   Iniciando en x=0 (buscando máximo de sin(x) + sin(x*2))...")
    print(f"   Mejor estado encontrado en x = {resultado:.4f}")
    print(f"   Valor: {objetivo_sin(resultado):.4f}\n")