import heapq
import math # Necesario para la heurística de ejemplo

# ============================================================================
# 10. BÚSQUEDA A* Y AO*
# ============================================================================

def busqueda_a_estrella(grafo, inicio, objetivo, heuristica):
    """
    Búsqueda óptima que considera costo real + heurística (f = g + h)
    Args:
        grafo: diccionario {nodo: [(vecino, costo), ...]}
        inicio: nodo inicial
        objetivo: nodo final
        heuristica: función estimadora
    Returns:
        (camino, costo) o (None, inf)
    """
    # Cola: (f, g, camino) donde f = g + h
    cola = [(heuristica(inicio, objetivo), 0, [inicio])]
    visitados = {}  # nodo: mejor_costo_g
    
    while cola:
        f, g, camino = heapq.heappop(cola)
        nodo = camino[-1]
        
        if nodo == objetivo:
            return camino, g
        
        # Solo procesar si es mejor que antes
        if nodo in visitados and visitados[nodo] <= g:
            continue
        
        visitados[nodo] = g
        
        for vecino, costo in grafo.get(nodo, []):
            nuevo_g = g + costo
            nuevo_camino = camino + [vecino]
            h = heuristica(vecino, objetivo)
            nuevo_f = nuevo_g + h
            heapq.heappush(cola, (nuevo_f, nuevo_g, nuevo_camino))
    
    return None, float('inf')


# Nota: AO* es para grafos AND/OR, implementación simplificada
def ao_estrella(grafo_and_or, inicio, objetivo, heuristica):
    """
    Versión simplificada de AO* para problemas con nodos AND/OR
    Args:
        grafo_and_or: diccionario con estructura especial
        inicio: nodo inicial
        objetivo: nodo final
        heuristica: función estimadora
    Returns:
        plan de solución
    """
    # Esta es una implementación conceptual simplificada
    # En la práctica, AO* maneja grafos con nodos AND/OR complejos
    print("Ejecutando AO* (versión simplificada, igual a A* para este ejemplo)")
    return busqueda_a_estrella(grafo_and_or, inicio, objetivo, heuristica)

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

    print("10. Búsqueda A*:")
    camino, costo = busqueda_a_estrella(grafo_coord, inicio, objetivo, 
                                        heuristica_distancia_manhattan)
    print(f"   Camino: {camino}")
    print(f"   Costo: {costo}\n")

    print("10. Búsqueda AO* (Simplificada):")
    camino_ao, costo_ao = ao_estrella(grafo_coord, inicio, objetivo, 
                                        heuristica_distancia_manhattan)
    print(f"   Camino: {camino_ao}")
    print(f"   Costo: {costo_ao}\n")