from collections import deque

# ============================================================================
# 1. BÚSQUEDA EN ANCHURA (BFS) - Dependencia
# ============================================================================
def busqueda_anchura(grafo, inicio, objetivo):
    cola = deque([[inicio]])
    visitados = set()
    while cola:
        camino = cola.popleft()
        nodo = camino[-1]
        if nodo == objetivo:
            return camino
        if nodo not in visitados:
            visitados.add(nodo)
            for vecino in grafo.get(nodo, []):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    return None

# ============================================================================
# 3. BÚSQUEDA EN PROFUNDIDAD (DFS) - Dependencia
# ============================================================================
def busqueda_profundidad(grafo, inicio, objetivo, visitados=None):
    if visitados is None:
        visitados = set()
    visitados.add(inicio)
    if inicio == objetivo:
        return [inicio]
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            camino = busqueda_profundidad(grafo, vecino, objetivo, visitados)
            if camino:
                return [inicio] + camino
    return None

# ============================================================================
# 7. BÚSQUEDA EN GRAFOS (Plantilla general)
# ============================================================================

def busqueda_grafos(grafo, inicio, objetivo, estrategia='bfs'):
    """
    Búsqueda genérica en grafos con diferentes estrategias
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo inicial
        objetivo: nodo final
        estrategia: 'bfs' o 'dfs'
    Returns:
        camino o None
    """
    if estrategia == 'bfs':
        return busqueda_anchura(grafo, inicio, objetivo)
    elif estrategia == 'dfs':
        return busqueda_profundidad(grafo, inicio, objetivo)
    else:
        print(f"Estrategia '{estrategia}' no reconocida.")
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
    
    print("7. Búsqueda en Grafos General:")
    
    print("   Probando estrategia 'bfs':")
    camino_bfs = busqueda_grafos(grafo, 'A', 'F', estrategia='bfs')
    print(f"   Camino: {camino_bfs}\n")
    
    print("   Probando estrategia 'dfs':")
    camino_dfs = busqueda_grafos(grafo, 'A', 'F', estrategia='dfs')
    print(f"   Camino: {camino_dfs}\n")