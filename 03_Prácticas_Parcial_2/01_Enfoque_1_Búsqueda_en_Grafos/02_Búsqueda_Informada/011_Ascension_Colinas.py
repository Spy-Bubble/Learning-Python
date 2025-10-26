# ============================================================================
# 11. BÚSQUEDA DE ASCENSIÓN DE COLINAS
# ============================================================================

def ascension_colinas(funcion_objetivo, estado_inicial, vecinos_func, max_iter=100):
    """
    Búsqueda local que siempre se mueve al mejor vecino
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado de inicio
        vecinos_func: función que genera estados vecinos
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    valor_actual = funcion_objetivo(actual)
    
    for _ in range(max_iter):
        vecinos = vecinos_func(actual)
        
        # Encontrar el mejor vecino
        mejor_vecino = None
        mejor_valor = valor_actual
        
        for vecino in vecinos:
            valor_vecino = funcion_objetivo(vecino)
            if valor_vecino > mejor_valor:
                mejor_vecino = vecino
                mejor_valor = valor_vecino
        
        # Si no hay mejora, terminar (máximo local)
        if mejor_vecino is None:
            break
        
        actual = mejor_vecino
        valor_actual = mejor_valor
    
    return actual

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("11. Ascensión de Colinas:")
    
    # Función objetivo: maximizar -x^2 (parábola invertida)
    # El máximo global está en x=5
    def objetivo_parabola(x):
        return -(x - 5)**2 + 25
    
    # Función de vecinos: explorar x-1 y x+1
    def vecinos_parabola(x):
        return [x - 1, x + 1]
    
    # Iniciar en x=0
    resultado = ascension_colinas(objetivo_parabola, 0, vecinos_parabola, max_iter=20)
    print(f"   Iniciando en x=0...")
    print(f"   Máximo local encontrado en x = {resultado}")
    print(f"   Valor: {objetivo_parabola(resultado)}\n")
    
    # Iniciar en x=10 (caerá en el mismo máximo local)
    resultado = ascension_colinas(objetivo_parabola, 10, vecinos_parabola, max_iter=20)
    print(f"   Iniciando en x=10...")
    print(f"   Máximo local encontrado en x = {resultado}")
    print(f"   Valor: {objetivo_parabola(resultado)}\n")