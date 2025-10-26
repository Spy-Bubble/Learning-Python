# ============================================================================
# 3. BÚSQUEDA EN PROFUNDIDAD (DFS)
# ============================================================================

def busqueda_profundidad(grafo, inicio, objetivo, visitados=None):
    """
    Explora el grafo en profundidad usando recursión
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo actual
        objetivo: nodo a encontrar
        visitados: conjunto de nodos ya visitados
    Returns:
        camino o None
    """
    if visitados is None:
        visitados = set()
    
    visitados.add(inicio)
    
    if inicio == objetivo:
        return [inicio]
    
    # Explorar cada vecino recursivamente
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            camino = busqueda_profundidad(grafo, vecino, objetivo, visitados)
            if camino:
                return [inicio] + camino
    
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
    
    print("3. Búsqueda en Profundidad (DFS):")
    camino = busqueda_profundidad(grafo, 'A', 'F')
    print(f"   Camino de A a F: {camino}\n")