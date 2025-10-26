from collections import deque

# ============================================================================
# 6. BÚSQUEDA BIDIRECCIONAL
# ============================================================================

def busqueda_bidireccional(grafo, inicio, objetivo):
    """
    Busca simultáneamente desde inicio y objetivo hasta que se encuentren
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo inicial
        objetivo: nodo final
    Returns:
        camino completo o None
    """
    # Búsquedas desde ambos extremos
    cola_inicio = deque([[inicio]])
    cola_objetivo = deque([[objetivo]])
    
    # {nodo: camino_hasta_el}
    visitados_inicio = {inicio: [inicio]}
    visitados_objetivo = {objetivo: [objetivo]}
    
    while cola_inicio and cola_objetivo:
        # 1. Expandir desde inicio
        if cola_inicio:
            camino = cola_inicio.popleft()
            nodo = camino[-1]
            
            # ¿Se encontraron las búsquedas?
            if nodo in visitados_objetivo:
                # Unir camino_inicio + reverso(camino_objetivo)[1:]
                return camino + visitados_objetivo[nodo][::-1][1:]
            
            for vecino in grafo.get(nodo, []):
                if vecino not in visitados_inicio:
                    nuevo_camino = camino + [vecino]
                    cola_inicio.append(nuevo_camino)
                    visitados_inicio[vecino] = nuevo_camino
        
        # 2. Expandir desde objetivo
        if cola_objetivo:
            camino = cola_objetivo.popleft()
            nodo = camino[-1]
            
            # ¿Se encontraron las búsquedas?
            if nodo in visitados_inicio:
                # Unir camino_inicio[nodo] + reverso(camino_actual)[1:]
                return visitados_inicio[nodo] + camino[::-1][1:]
            
            for vecino in grafo.get(nodo, []):
                if vecino not in visitados_objetivo:
                    nuevo_camino = camino + [vecino]
                    cola_objetivo.append(nuevo_camino)
                    visitados_objetivo[vecino] = nuevo_camino
    
    return None # No se encontró conexión

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

    print("6. Búsqueda Bidireccional:")
    camino = busqueda_bidireccional(grafo, 'A', 'F')
    print(f"   Camino: {camino}\n")