"""
BÚSQUEDA NO INFORMADA EN GRAFOS
Algoritmos 1-7: Búsqueda sin heurísticas
"""

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
# 2. BÚSQUEDA EN ANCHURA DE COSTO UNIFORME
# ============================================================================

import heapq

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
    visitados_inicio = {inicio: [inicio]}
    visitados_objetivo = {objetivo: [objetivo]}
    
    while cola_inicio and cola_objetivo:
        # Expandir desde inicio
        camino = cola_inicio.popleft()
        nodo = camino[-1]
        
        # ¿Se encontraron las búsquedas?
        if nodo in visitados_objetivo:
            return camino + visitados_objetivo[nodo][::-1][1:]
        
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados_inicio:
                nuevo_camino = camino + [vecino]
                cola_inicio.append(nuevo_camino)
                visitados_inicio[vecino] = nuevo_camino
        
        # Expandir desde objetivo
        camino = cola_objetivo.popleft()
        nodo = camino[-1]
        
        if nodo in visitados_inicio:
            return visitados_inicio[nodo] + camino[::-1][1:]
        
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados_objetivo:
                nuevo_camino = camino + [vecino]
                cola_objetivo.append(nuevo_camino)
                visitados_objetivo[vecino] = nuevo_camino
    
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
        return None


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== BÚSQUEDA NO INFORMADA ===\n")
    
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
    
    print("3. Búsqueda en Profundidad (DFS):")
    camino = busqueda_profundidad(grafo, 'A', 'F')
    print(f"   Camino de A a F: {camino}\n")
    
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
    
    print("5. Búsqueda en Profundidad Iterativa:")
    camino = busqueda_profundidad_iterativa(grafo, 'A', 'F', max_profundidad=5)
    print(f"   Camino: {camino}\n")
    
    print("6. Búsqueda Bidireccional:")
    camino = busqueda_bidireccional(grafo, 'A', 'F')
    print(f"   Camino: {camino}\n")