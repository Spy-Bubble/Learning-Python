# ============================================================================
# 4. BÚSQUEDA EN PROFUNDIDAD LIMITADA
# ============================================================================

def busqueda_profundidad_limitada(grafo, inicio, objetivo, limite, visitados=None):
    """
    DFS con límite de profundidad para evitar bucles infinitos
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo actual
        objetivo: nodo a encontrar
        limite: profundidad máxima permitida
        visitados: conjunto de nodos visitados
    Returns:
        camino o None
    """
    if visitados is None:
        visitados = set()
    
    if limite < 0:
        return None  # Se alcanzó el límite
    
    visitados.add(inicio)
    
    if inicio == objetivo:
        return [inicio]
    
    # Explorar vecinos con límite reducido
    for vecino in grafo.get(inicio, []):
        if vecino not in visitados:
            # Pasamos una copia de visitados para explorar otras ramas
            camino = busqueda_profundidad_limitada(grafo, vecino, objetivo, 
                                                 limite - 1, visitados.copy())
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
    
    print("4. Búsqueda en Profundidad Limitada (DLS):")
    
    print("   Buscando 'F' con límite 1:")
    camino_lim_1 = busqueda_profundidad_limitada(grafo, 'A', 'F', 1)
    print(f"   Camino: {camino_lim_1}\n") # Debería ser None
    
    print("   Buscando 'F' con límite 2:")
    camino_lim_2 = busqueda_profundidad_limitada(grafo, 'A', 'F', 2)
    print(f"   Camino: {camino_lim_2}\n") # Debería ser ['A', 'C', 'F']