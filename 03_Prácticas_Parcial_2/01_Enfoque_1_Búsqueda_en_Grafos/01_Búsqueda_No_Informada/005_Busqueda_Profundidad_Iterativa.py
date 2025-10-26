# ============================================================================
# 4. BÚSQUEDA EN PROFUNDIDAD LIMITADA (Dependencia)
# ============================================================================
# Esta función es requerida por la Búsqueda Iterativa

def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite, visitados=None):
    if visitados is None:
        visitados = set()
    
    if limite < 0:
        return None
    
    visitados.add(inicio)
    
    if inicio == objetivo:
        return [inicio]
    
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            camino = busqueda_profundidad_limitada(grafo, vecino, objetivo, 
                                                 limite - 1, visitados.copy())
            if camino:
                return [inicio] + camino
    return None

# ============================================================================
# 5. BÚSQUEDA EN PROFUNDIDAD ITERATIVA
# ============================================================================

def busqueda_profundidad_iterativa(grafo, inicio, objetivo, max_profundidad=10):
    """
    Aplica DFS con límites incrementales de profundidad
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo inicial
        objetivo: nodo a encontrar
        max_profundidad: profundidad máxima a intentar
    Returns:
        camino o None
    """
    # Intentar con profundidades crecientes
    for profundidad in range(max_profundidad):
        resultado = busqueda_profundidad_limitada(grafo, inicio, objetivo, profundidad)
        if resultado:
            return resultado
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Grafo de ejemplo
    grafo = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    
    print("5. Búsqueda en Profundidad Iterativa:")
    camino = busqueda_profundidad_iterativa(grafo, 'A', 'F', max_profundidad=5)
    print(f"   Camino: {camino}\n")