from collections import deque

# ============================================================================
# 12. BÚSQUEDA TABÚ
# ============================================================================

def busqueda_tabu(funcion_objetivo, estado_inicial, vecinos_func, tam_tabu=10, max_iter=100):
    """
    Búsqueda local con memoria de estados prohibidos (tabú)
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado inicial
        vecinos_func: función generadora de vecinos
        tam_tabu: tamaño de la lista tabú
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    mejor = actual
    mejor_valor = funcion_objetivo(mejor)
    lista_tabu = deque(maxlen=tam_tabu)  # Lista circular
    
    for _ in range(max_iter):
        vecinos = [v for v in vecinos_func(actual) if v not in lista_tabu]
        
        if not vecinos:
            break
        
        # Elegir el mejor vecino no tabú
        actual = max(vecinos, key=funcion_objetivo)
        valor_actual = funcion_objetivo(actual)
        lista_tabu.append(actual)
        
        # Actualizar mejor solución global
        if valor_actual > mejor_valor:
            mejor = actual
            mejor_valor = valor_actual
    
    return mejor

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("12. Búsqueda Tabú:")
    
    # Función objetivo: maximizar -x^2 (parábola invertida)
    # El máximo global está en x=5
    def objetivo_parabola(x):
        return -(x - 5)**2 + 25
    
    # Función de vecinos: explorar x-1 y x+1
    def vecinos_parabola(x):
        return [x - 1, x + 1]
    
    # Iniciar en x=0
    resultado = busqueda_tabu(objetivo_parabola, 0, vecinos_parabola, 
                              tam_tabu=5, max_iter=20)
    print(f"   Iniciando en x=0...")
    print(f"   Mejor estado encontrado en x = {resultado}")
    print(f"   Valor: {objetivo_parabola(resultado)}\n")