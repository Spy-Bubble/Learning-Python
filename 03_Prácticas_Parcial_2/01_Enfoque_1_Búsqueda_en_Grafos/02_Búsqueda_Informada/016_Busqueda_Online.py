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
    pila = []  # Para backtracking (estado_previo, accion_realizada)
    acciones_realizadas = []
    
    for _ in range(max_pasos):
        if es_objetivo(estado):
            return acciones_realizadas
        
        visitados.add(estado)
        
        # Obtener acciones no exploradas desde el estado actual
        acciones_no_exploradas = []
        for a in acciones_disponibles(estado):
            estado_siguiente = transicion(estado, a)
            if estado_siguiente not in visitados:
                acciones_no_exploradas.append(a)

        
        if acciones_no_exploradas:
            # Explorar nueva acción
            accion = acciones_no_exploradas[0] # Tomar la primera disponible
            pila.append((estado, accion))
            estado_nuevo = transicion(estado, accion)
            acciones_realizadas.append(accion)
            estado = estado_nuevo
        elif pila:
            # Backtrack
            estado_previo, accion_previa = pila.pop()
            # Asumimos que podemos "revertir" la acción o teletransportarnos
            # Para un agente real, necesitaría una acción "inversa"
            acciones_realizadas.append(f'BACKTRACK_A_{estado_previo}')
            estado = estado_previo
        else:
            # Atrapado
            break
    
    return acciones_realizadas

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("16. Búsqueda Online (DFS):")
    
    # Simular un laberinto simple (grid 3x3)
    # (0,0) (1,0) (2,0)
    # (0,1) [PARED] (2,1)
    # (0,2) (1,2) (2,2) <- Objetivo
    
    paredes = {(1, 1)}
    objetivo = (2, 2)
    
    def es_objetivo(estado):
        return estado == objetivo

    def acciones_disponibles(estado):
        # En un agente real, esto sería "percibir"
        return ['ARRIBA', 'ABAJO', 'IZQ', 'DER']

    def transicion(estado, accion):
        x, y = estado
        if accion == 'ARRIBA':
            y -= 1
        elif accion == 'ABAJO':
            y += 1
        elif accion == 'IZQ':
            x -= 1
        elif accion == 'DER':
            x += 1
        
        nuevo_estado = (x, y)
        
        # Validar límites y paredes
        if 0 <= x < 3 and 0 <= y < 3 and nuevo_estado not in paredes:
            return nuevo_estado
        else:
            return estado # Chocar contra la pared te mantiene en el lugar

    estado_inicial = (0, 0)
    secuencia = busqueda_online_dfs(estado_inicial, es_objetivo, 
                                    acciones_disponibles, transicion, 
                                    max_pasos=50)
    
    print(f"   Iniciando en (0,0), objetivo (2,2).")
    print(f"   Secuencia de acciones: {secuencia}")