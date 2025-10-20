"""
BÚSQUEDA INFORMADA (HEURÍSTICAS)
Algoritmos 8-16: Búsqueda con heurísticas y optimización
"""

import heapq
import random
import math
from collections import deque

# ============================================================================
# 8. HEURÍSTICAS
# ============================================================================

def heuristica_distancia_manhattan(nodo, objetivo):
    """
    Calcula distancia Manhattan entre dos puntos (x, y)
    Args:
        nodo: tupla (x, y)
        objetivo: tupla (x, y)
    Returns:
        distancia Manhattan
    """
    return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])


def heuristica_distancia_euclidiana(nodo, objetivo):
    """
    Calcula distancia euclidiana entre dos puntos
    Args:
        nodo: tupla (x, y)
        objetivo: tupla (x, y)
    Returns:
        distancia euclidiana
    """
    return math.sqrt((nodo[0] - objetivo[0])**2 + (nodo[1] - objetivo[1])**2)


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
    return busqueda_a_estrella(grafo_and_or, inicio, objetivo, heuristica)


# ============================================================================
# 11. BÚSQUEDA DE ASCENSIÓN DE COLINAS
# ============================================================================

def ascension_colinas(funcion_objetivo, estado_inicial, vecinos_func, max_iter=100):
    """
    Búsqueda local que siempre se mueve al mejor vecino
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado de inicio
        vecinos_func: función que genera estados vecinos
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    valor_actual = funcion_objetivo(actual)
    
    for _ in range(max_iter):
        vecinos = vecinos_func(actual)
        
        # Encontrar el mejor vecino
        mejor_vecino = None
        mejor_valor = valor_actual
        
        for vecino in vecinos:
            valor_vecino = funcion_objetivo(vecino)
            if valor_vecino > mejor_valor:
                mejor_vecino = vecino
                mejor_valor = valor_vecino
        
        # Si no hay mejora, terminar (máximo local)
        if mejor_vecino is None:
            break
        
        actual = mejor_vecino
        valor_actual = mejor_valor
    
    return actual


# ============================================================================
# 12. BÚSQUEDA TABÚ
# ============================================================================

def busqueda_tabu(funcion_objetivo, estado_inicial, vecinos_func, tam_tabu=10, max_iter=100):
    """
    Búsqueda local con memoria de estados prohibidos (tabú)
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado inicial
        vecinos_func: función generadora de vecinos
        tam_tabu: tamaño de la lista tabú
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    mejor = actual
    mejor_valor = funcion_objetivo(mejor)
    lista_tabu = deque(maxlen=tam_tabu)  # Lista circular
    
    for _ in range(max_iter):
        vecinos = [v for v in vecinos_func(actual) if v not in lista_tabu]
        
        if not vecinos:
            break
        
        # Elegir el mejor vecino no tabú
        actual = max(vecinos, key=funcion_objetivo)
        valor_actual = funcion_objetivo(actual)
        lista_tabu.append(actual)
        
        # Actualizar mejor solución global
        if valor_actual > mejor_valor:
            mejor = actual
            mejor_valor = valor_actual
    
    return mejor


# ============================================================================
# 13. BÚSQUEDA DE TEMPLE SIMULADO
# ============================================================================

def temple_simulado(funcion_objetivo, estado_inicial, vecinos_func, 
                    temp_inicial=100, alpha=0.95, max_iter=1000):
    """
    Búsqueda probabilística inspirada en el recocido de metales
    Args:
        funcion_objetivo: función a maximizar
        estado_inicial: estado inicial
        vecinos_func: función generadora de vecinos
        temp_inicial: temperatura inicial
        alpha: factor de enfriamiento (0 < alpha < 1)
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actual = estado_inicial
    mejor = actual
    mejor_valor = funcion_objetivo(mejor)
    temperatura = temp_inicial
    
    for _ in range(max_iter):
        vecinos = vecinos_func(actual)
        if not vecinos:
            break
        
        vecino = random.choice(vecinos)
        valor_actual = funcion_objetivo(actual)
        valor_vecino = funcion_objetivo(vecino)
        
        delta = valor_vecino - valor_actual
        
        # Aceptar si mejora o con probabilidad decreciente
        if delta > 0 or random.random() < math.exp(delta / temperatura):
            actual = vecino
            
            if valor_vecino > mejor_valor:
                mejor = vecino
                mejor_valor = valor_vecino
        
        # Enfriar
        temperatura *= alpha
    
    return mejor


# ============================================================================
# 14. BÚSQUEDA DE HAZ LOCAL
# ============================================================================

def busqueda_haz_local(funcion_objetivo, estados_iniciales, vecinos_func, k=3, max_iter=100):
    """
    Mantiene k mejores estados y expande solo esos
    Args:
        funcion_objetivo: función a maximizar
        estados_iniciales: lista de estados iniciales
        vecinos_func: función generadora de vecinos
        k: número de estados a mantener (ancho del haz)
        max_iter: iteraciones máximas
    Returns:
        mejor estado encontrado
    """
    actuales = estados_iniciales[:k]
    
    for _ in range(max_iter):
        # Generar todos los vecinos de los k estados
        todos_vecinos = []
        for estado in actuales:
            todos_vecinos.extend(vecinos_func(estado))
        
        if not todos_vecinos:
            break
        
        # Seleccionar los k mejores vecinos
        todos_vecinos.sort(key=funcion_objetivo, reverse=True)
        actuales = todos_vecinos[:k]
    
    # Retornar el mejor de los k estados finales
    return max(actuales, key=funcion_objetivo)


# ============================================================================
# 15. ALGORITMOS GENÉTICOS
# ============================================================================

def algoritmo_genetico(funcion_fitness, tam_poblacion=50, tam_cromosoma=10, 
                       generaciones=100, prob_mutacion=0.01, prob_cruce=0.7):
    """
    Evolución de población mediante selección, cruce y mutación
    Args:
        funcion_fitness: función de aptitud a maximizar
        tam_poblacion: tamaño de la población
        tam_cromosoma: longitud de cada cromosoma (lista binaria)
        generaciones: número de generaciones
        prob_mutacion: probabilidad de mutación
        prob_cruce: probabilidad de cruce
    Returns:
        mejor cromosoma encontrado
    """
    # Generar población inicial aleatoria
    poblacion = [[random.randint(0, 1) for _ in range(tam_cromosoma)] 
                 for _ in range(tam_poblacion)]
    
    for _ in range(generaciones):
        # Evaluar fitness
        fitness = [funcion_fitness(cromosoma) for cromosoma in poblacion]
        
        # Selección por torneo
        nueva_poblacion = []
        for _ in range(tam_poblacion):
            # Seleccionar 2 padres
            padres = random.choices(poblacion, weights=fitness, k=2)
            
            # Cruce
            if random.random() < prob_cruce:
                punto_cruce = random.randint(1, tam_cromosoma - 1)
                hijo = padres[0][:punto_cruce] + padres[1][punto_cruce:]
            else:
                hijo = padres[0][:]
            
            # Mutación
            for i in range(tam_cromosoma):
                if random.random() < prob_mutacion:
                    hijo[i] = 1 - hijo[i]
            
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
    
    # Retornar el mejor individuo
    return max(poblacion, key=funcion_fitness)


# ============================================================================
# 16. BÚSQUEDA ONLINE
# ============================================================================

def busqueda_online_dfs(estado_inicial, es_objetivo, acciones_disponibles, 
                        transicion, max_pasos=100):
    """
    Búsqueda en profundidad para agentes que descubren el entorno
    Args:
        estado_inicial: estado de inicio
        es_objetivo: función que verifica si es estado objetivo
        acciones_disponibles: función que da acciones posibles
        transicion: función que aplica acción al estado
        max_pasos: pasos máximos
    Returns:
        secuencia de acciones
    """
    estado = estado_inicial
    visitados = set()
    pila = []  # Para backtracking
    acciones_realizadas = []
    
    for _ in range(max_pasos):
        if es_objetivo(estado):
            return acciones_realizadas
        
        visitados.add(estado)
        
        # Obtener acciones no exploradas
        acciones = [a for a in acciones_disponibles(estado) 
                   if transicion(estado, a) not in visitados]
        
        if acciones:
            # Explorar nueva acción
            accion = acciones[0]
            pila.append((estado, accion))
            estado = transicion(estado, accion)
            acciones_realizadas.append(accion)
        elif pila:
            # Backtrack
            estado_previo, accion_previa = pila.pop()
            # Regresar al estado previo (acción inversa)
            acciones_realizadas.append(('back', accion_previa))
            estado = estado_previo
        else:
            break
    
    return acciones_realizadas


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== BÚSQUEDA INFORMADA (HEURÍSTICAS) ===\n")
    
    # Grafo con coordenadas para heurísticas
    grafo_coord = {
        (0, 0): [((1, 0), 1), ((0, 1), 1)],
        (1, 0): [((1, 1), 1), ((2, 0), 1)],
        (0, 1): [((1, 1), 1)],
        (1, 1): [((2, 1), 1)],
        (2, 0): [((2, 1), 1)],
        (2, 1): []
    }
    
    print("10. Búsqueda A*:")
    camino, costo = busqueda_a_estrella(grafo_coord, (0, 0), (2, 1), 
                                        heuristica_distancia_manhattan)
    print(f"   Camino: {camino}")
    print(f"   Costo: {costo}\n")
    
    # Ejemplo de Ascensión de Colinas
    print("11. Ascensión de Colinas:")
    # Función objetivo: maximizar -x^2 (parábola invertida)
    def objetivo(x):
        return -(x - 5)**2 + 25
    
    def vecinos(x):
        return [x - 1, x + 1]
    
    resultado = ascension_colinas(objetivo, 0, vecinos, max_iter=20)
    print(f"   Máximo encontrado en x = {resultado}")
    print(f"   Valor: {objetivo(resultado)}\n")
    
    # Ejemplo de Algoritmo Genético
    print("15. Algoritmo Genético:")
    # Fitness: contar número de 1s en cromosoma
    def fitness(cromosoma):
        return sum(cromosoma)
    
    mejor = algoritmo_genetico(fitness, tam_poblacion=20, tam_cromosoma=10, 
                               generaciones=50)
    print(f"   Mejor cromosoma: {mejor}")
    print(f"   Fitness: {fitness(mejor)}")