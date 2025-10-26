import heapq

# ============================================================================
# 2. BÚSQUEDA EN ANCHURA DE COSTO UNIFORME
# ============================================================================

def busqueda_costo_uniforme(grafo, inicio, objetivo):
    """
    Similar a BFS pero considera costos de aristas usando cola de prioridad
    Args:
        grafo: diccionario {nodo: [(vecino, costo), ...]}
        inicio: nodo inicial
        objetivo: nodo a encontrar
    Returns:
        (camino, costo_total) o (None, float('inf'))
    """
    # Cola de prioridad: (costo_acumulado, camino)
    cola_prioridad = [(0, [inicio])]
    visitados = set()
    
    while cola_prioridad:
        costo, camino = heapq.heappop(cola_prioridad)
        nodo = camino[-1]
        
        if nodo == objetivo:
            return camino, costo
        
        if nodo not in visitados:
            visitados.add(nodo)
            # Explorar vecinos
            for vecino, costo_arista in grafo.get(nodo, []):
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    nuevo_costo = costo + costo_arista
                    heapq.heappush(cola_prioridad, (nuevo_costo, nuevo_camino))
    
    return None, float('inf')

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Grafo con costos para Costo Uniforme
    grafo_costos = {
        'A': [('B', 1), ('C', 4)],
        'B': [('D', 3), ('E', 2)],
        'C': [('F', 2)],
        'D': [],
        'E': [('F', 1)],
        'F': []
    }
    
    print("2. Búsqueda de Costo Uniforme:")
    camino, costo = busqueda_costo_uniforme(grafo_costos, 'A', 'F')
    print(f"   Camino: {camino}, Costo total: {costo}\n")