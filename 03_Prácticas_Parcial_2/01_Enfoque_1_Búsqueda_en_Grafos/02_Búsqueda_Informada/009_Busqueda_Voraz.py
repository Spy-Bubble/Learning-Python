import heapq
import math # Necesario para la heurística de ejemplo

# ============================================================================
# 9. BÚSQUEDA VORAZ PRIMERO EL MEJOR
# ============================================================================

def busqueda_voraz(grafo, inicio, objetivo, heuristica):
    """
    Selecciona el nodo con mejor heurística sin considerar costo acumulado
    Args:
        grafo: diccionario {nodo: [(vecino, costo), ...]}
        inicio: nodo inicial
        objetivo: nodo final
        heuristica: función que estima distancia al objetivo
    Returns:
        camino o None
    """
    # Cola de prioridad: (valor_heuristica, camino)
    cola = [(heuristica(inicio, objetivo), [inicio])]
    visitados = set()
    
    while cola:
        _, camino = heapq.heappop(cola)
        nodo = camino[-1]
        
        if nodo == objetivo:
            return camino
        
        if nodo not in visitados:
            visitados.add(nodo)
            
            for vecino, _ in grafo.get(nodo, []):
                if vecino not in visitados:
                    nuevo_camino = camino + [vecino]
                    h = heuristica(vecino, objetivo)
                    heapq.heappush(cola, (h, nuevo_camino))
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

# Heurística de ejemplo (Manhattan)
def heuristica_distancia_manhattan(nodo, objetivo):
    return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])

if __name__ == "__main__":
    # Grafo con coordenadas para heurísticas
    grafo_coord = {
        (0, 0): [((1, 0), 1), ((0, 1), 1)],
        (1, 0): [((1, 1), 1), ((2, 0), 1)],
        (0, 1): [((1, 1), 1)],
        (1, 1): [((2, 1), 1)],
        (2, 0): [((2, 1), 1)],
        (2, 1): []
    }
    
    inicio = (0, 0)
    objetivo = (2, 1)
    
    print("9. Búsqueda Voraz Primero el Mejor:")
    camino = busqueda_voraz(grafo_coord, inicio, objetivo, 
                             heuristica_distancia_manhattan)
    print(f"   Camino: {camino}\n")