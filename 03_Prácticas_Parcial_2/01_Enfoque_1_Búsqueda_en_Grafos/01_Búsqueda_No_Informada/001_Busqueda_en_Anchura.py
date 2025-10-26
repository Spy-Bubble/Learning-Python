from collections import deque

# ============================================================================
# 1. BÚSQUEDA EN ANCHURA (BFS)
# ============================================================================

def busqueda_anchura(grafo, inicio, objetivo):
    """
    Explora el grafo nivel por nivel usando una cola FIFO
    Args:
        grafo: diccionario {nodo: [vecinos]}
        inicio: nodo inicial
        objetivo: nodo a encontrar
    Returns:
        camino desde inicio hasta objetivo o None
    """
    # Cola para nodos por visitar y diccionario para rastrear el camino
    cola = deque([[inicio]])
    visitados = set()
    
    while cola:
        camino = cola.popleft()  # Tomar el primer camino de la cola
        nodo = camino[-1]  # Último nodo del camino
        
        if nodo == objetivo:
            return camino  # Encontrado
        
        if nodo not in visitados:
            visitados.add(nodo)
            # Agregar caminos a vecinos no visitados
            for vecino in grafo.get(nodo, []):
                nuevo_camino = list(camino)
                nuevo_camino.append(vecino)
                cola.append(nuevo_camino)
    
    return None  # No se encontró camino

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
    
    print("1. Búsqueda en Anchura (BFS):")
    camino = busqueda_anchura(grafo, 'A', 'F')
    print(f"   Camino de A a F: {camino}\n")