import random

# ============================================================================
# 14. BÚSQUEDA DE HAZ LOCAL
# ============================================================================

def busqueda_haz_local(funcion_objetivo, estados_iniciales, vecinos_func, k=3, max_iter=100):
    """
    Mantiene k mejores estados y expande solo esos
    Args:
        funcion_objetivo: función a maximizar
        estados_iniciales: lista de estados iniciales
        vecinos_func: función generadora de vecinos
        k: número de estados a mantener (ancho del haz)
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actuales = estados_iniciales[:k]
    
    for _ in range(max_iter):
        # Generar todos los vecinos de los k estados
        todos_vecinos = []
        for estado in actuales:
            todos_vecinos.extend(vecinos_func(estado))
        
        if not todos_vecinos:
            break
        
        # Seleccionar los k mejores vecinos (evitando duplicados)
        todos_vecinos = list(set(todos_vecinos)) # Opcional: mantener diversidad
        todos_vecinos.sort(key=funcion_objetivo, reverse=True)
        actuales = todos_vecinos[:k]
    
    # Retornar el mejor de los k estados finales
    return max(actuales, key=funcion_objetivo)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("14. Búsqueda de Haz Local:")
    
    # Función objetivo: maximizar -x^2 (parábola invertida)
    # El máximo global está en x=5
    def objetivo_parabola(x):
        return -(x - 5)**2 + 25
    
    # Función de vecinos: explorar x-1 y x+1
    def vecinos_parabola(x):
        return [x - 1, x + 1]
    
    # Iniciar con k=3 estados aleatorios
    k = 3
    estados_iniciales = [random.randint(0, 10) for _ in range(k)]
    
    resultado = busqueda_haz_local(objetivo_parabola, estados_iniciales, 
                                   vecinos_parabola, k=k, max_iter=20)
    
    print(f"   Iniciando con k={k} estados: {estados_iniciales}")
    print(f"   Mejor estado encontrado en x = {resultado}")
    print(f"   Valor: {objetivo_parabola(resultado)}\n")