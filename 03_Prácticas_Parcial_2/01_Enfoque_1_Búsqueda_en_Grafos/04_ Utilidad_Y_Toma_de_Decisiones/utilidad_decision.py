"""
UTILIDAD Y TOMA DE DECISIONES
Algoritmos 24-32: Teoría de la utilidad, MDP, POMDP y teoría de juegos
"""

import random
import math

# ============================================================================
# 24. TEORÍA DE LA UTILIDAD: FUNCIÓN DE UTILIDAD
# ============================================================================

def funcion_utilidad_lineal(x, utilidad_min=0, utilidad_max=100):
    """
    Función de utilidad lineal simple
    Args:
        x: valor del resultado (entre 0 y 1)
        utilidad_min: utilidad mínima
        utilidad_max: utilidad máxima
    Returns:
        utilidad normalizada
    """
    return utilidad_min + (utilidad_max - utilidad_min) * x


def funcion_utilidad_logaritmica(riqueza, constante=1):
    """
    Función de utilidad logarítmica (aversión al riesgo)
    Args:
        riqueza: cantidad de dinero o recurso
        constante: constante de escala
    Returns:
        utilidad logarítmica
    """
    if riqueza <= 0:
        return float('-inf')
    return constante * math.log(riqueza)


def utilidad_esperada(acciones, probabilidades, utilidades):
    """
    Calcula utilidad esperada de una acción
    Args:
        acciones: lista de acciones posibles
        probabilidades: diccionario {accion: [probs de resultados]}
        utilidades: diccionario {accion: [utilidades de resultados]}
    Returns:
        diccionario {accion: utilidad_esperada}
    """
    utilidades_esperadas = {}
    
    for accion in acciones:
        probs = probabilidades[accion]
        utils = utilidades[accion]
        utilidades_esperadas[accion] = sum(p * u for p, u in zip(probs, utils))
    
    return utilidades_esperadas


# ============================================================================
# 25. REDES DE DECISIÓN
# ============================================================================

class RedDecision:
    """
    Representa una red de decisión (diagrama de influencia)
    """
    def __init__(self):
        self.nodos_azar = {}  # Nodos de probabilidad
        self.nodos_decision = []  # Nodos de decisión
        self.nodos_utilidad = {}  # Nodos de utilidad
    
    def agregar_nodo_azar(self, nombre, probabilidades):
        """Agrega nodo con incertidumbre"""
        self.nodos_azar[nombre] = probabilidades
    
    def agregar_nodo_decision(self, nombre, opciones):
        """Agrega nodo de decisión"""
        self.nodos_decision.append((nombre, opciones))
    
    def agregar_nodo_utilidad(self, nombre, funcion_utilidad):
        """Agrega nodo de utilidad"""
        self.nodos_utilidad[nombre] = funcion_utilidad
    
    def evaluar(self, decision):
        """
        Evalúa utilidad esperada de una decisión
        Args:
            decision: diccionario de decisiones
        Returns:
            utilidad esperada
        """
        utilidad_total = 0
        
        for nombre_util, func_util in self.nodos_utilidad.items():
            utilidad_total += func_util(decision)
        
        return utilidad_total


# ============================================================================
# 26. VALOR DE LA INFORMACIÓN
# ============================================================================

def valor_informacion_perfecta(probabilidades, utilidades):
    """
    Calcula el Valor de la Información Perfecta (VIP)
    Args:
        probabilidades: lista de probabilidades de estados
        utilidades: diccionario {estado: {accion: utilidad}}
    Returns:
        VIP (diferencia entre decisión con y sin información)
    """
    # Utilidad esperada SIN información (mejor acción promedio)
    utilidad_sin_info = max(
        sum(prob * utilidades[estado][accion] 
            for estado, prob in enumerate(probabilidades))
        for accion in utilidades[0].keys()
    )
    
    # Utilidad esperada CON información perfecta
    utilidad_con_info = sum(
        prob * max(utilidades[estado].values())
        for estado, prob in enumerate(probabilidades)
    )
    
    # VIP = diferencia
    return utilidad_con_info - utilidad_sin_info


# ============================================================================
# 27. ITERACIÓN DE VALORES
# ============================================================================

def iteracion_valores(estados, acciones, transiciones, recompensas, gamma=0.9, epsilon=0.01):
    """
    Algoritmo de iteración de valores para MDP
    Args:
        estados: lista de estados
        acciones: lista de acciones
        transiciones: dict {(s, a, s'): probabilidad}
        recompensas: dict {(s, a): recompensa}
        gamma: factor de descuento
        epsilon: umbral de convergencia
    Returns:
        valores óptimos de cada estado
    """
    # Inicializar valores
    V = {s: 0 for s in estados}
    
    while True:
        delta = 0
        V_nuevo = {}
        
        for s in estados:
            # Calcular valor para cada acción
            valores_acciones = []
            
            for a in acciones:
                valor = recompensas.get((s, a), 0)
                
                # Sumar valores esperados de estados siguientes
                for s_prima in estados:
                    prob = transiciones.get((s, a, s_prima), 0)
                    valor += gamma * prob * V[s_prima]
                
                valores_acciones.append(valor)
            
            # Mejor valor para este estado
            V_nuevo[s] = max(valores_acciones) if valores_acciones else 0
            delta = max(delta, abs(V_nuevo[s] - V[s]))
        
        V = V_nuevo
        
        # Convergencia
        if delta < epsilon:
            break
    
    return V


# ============================================================================
# 28. ITERACIÓN DE POLÍTICAS
# ============================================================================

def iteracion_politicas(estados, acciones, transiciones, recompensas, gamma=0.9):
    """
    Algoritmo de iteración de políticas para MDP
    Args:
        estados: lista de estados
        acciones: lista de acciones
        transiciones: dict {(s, a, s'): probabilidad}
        recompensas: dict {(s, a): recompensa}
        gamma: factor de descuento
    Returns:
        política óptima {estado: accion}
    """
    # Política inicial aleatoria
    politica = {s: random.choice(acciones) for s in estados}
    
    while True:
        # Evaluación de política
        V = evaluar_politica(estados, politica, transiciones, recompensas, gamma)
        
        # Mejora de política
        politica_estable = True
        
        for s in estados:
            accion_vieja = politica[s]
            
            # Encontrar mejor acción
            mejor_accion = None
            mejor_valor = float('-inf')
            
            for a in acciones:
                valor = recompensas.get((s, a), 0)
                for s_prima in estados:
                    prob = transiciones.get((s, a, s_prima), 0)
                    valor += gamma * prob * V[s_prima]
                
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_accion = a
            
            politica[s] = mejor_accion
            
            if accion_vieja != mejor_accion:
                politica_estable = False
        
        if politica_estable:
            break
    
    return politica


def evaluar_politica(estados, politica, transiciones, recompensas, gamma, epsilon=0.01):
    """Evalúa el valor de una política dada"""
    V = {s: 0 for s in estados}
    
    while True:
        delta = 0
        V_nuevo = {}
        
        for s in estados:
            a = politica[s]
            valor = recompensas.get((s, a), 0)
            
            for s_prima in estados:
                prob = transiciones.get((s, a, s_prima), 0)
                valor += gamma * prob * V[s_prima]
            
            V_nuevo[s] = valor
            delta = max(delta, abs(V_nuevo[s] - V[s]))
        
        V = V_nuevo
        
        if delta < epsilon:
            break
    
    return V


# ============================================================================
# 29. PROCESO DE DECISIÓN DE MARKOV (MDP)
# ============================================================================

class MDP:
    """
    Clase para representar un Proceso de Decisión de Markov
    """
    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9):
        """
        Args:
            estados: lista de estados
            acciones: lista de acciones
            transiciones: función o dict P(s'|s,a)
            recompensas: función o dict R(s,a)
            gamma: factor de descuento
        """
        self.estados = estados
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.gamma = gamma
    
    def resolver_iteracion_valores(self):
        """Resuelve el MDP usando iteración de valores"""
        return iteracion_valores(self.estados, self.acciones, 
                                self.transiciones, self.recompensas, self.gamma)
    
    def resolver_iteracion_politicas(self):
        """Resuelve el MDP usando iteración de políticas"""
        return iteracion_politicas(self.estados, self.acciones,
                                   self.transiciones, self.recompensas, self.gamma)


# ============================================================================
# 30. MDP PARCIALMENTE OBSERVABLE (POMDP)
# ============================================================================

class POMDP:
    """
    MDP Parcialmente Observable - el agente no observa el estado directamente
    """
    def __init__(self, estados, acciones, observaciones, transiciones, 
                 observacion_prob, recompensas, gamma=0.9):
        """
        Args:
            estados: estados posibles (ocultos)
            acciones: acciones posibles
            observaciones: observaciones posibles
            transiciones: P(s'|s,a)
            observacion_prob: P(o|s,a)
            recompensas: R(s,a)
            gamma: factor de descuento
        """
        self.estados = estados
        self.acciones = acciones
        self.observaciones = observaciones
        self.transiciones = transiciones
        self.observacion_prob = observacion_prob
        self.recompensas = recompensas
        self.gamma = gamma
    
    def actualizar_creencia(self, creencia, accion, observacion):
        """
        Actualiza la distribución de creencia sobre estados
        Args:
            creencia: dict {estado: probabilidad}
            accion: acción tomada
            observacion: observación recibida
        Returns:
            nueva creencia
        """
        nueva_creencia = {}
        
        for s_prima in self.estados:
            # P(s'|creencia, a, o)
            prob = 0
            for s in self.estados:
                trans_prob = self.transiciones.get((s, accion, s_prima), 0)
                obs_prob = self.observacion_prob.get((s_prima, accion, observacion), 0)
                prob += creencia.get(s, 0) * trans_prob * obs_prob
            
            nueva_creencia[s_prima] = prob
        
        # Normalizar
        total = sum(nueva_creencia.values())
        if total > 0:
            nueva_creencia = {s: p/total for s, p in nueva_creencia.items()}
        
        return nueva_creencia


# ============================================================================
# 31. RED BAYESIANA DINÁMICA
# ============================================================================

class RedBayesianaDinamica:
    """
    Representa una Red Bayesiana que evoluciona en el tiempo
    """
    def __init__(self, variables, probabilidades_transicion, probabilidades_iniciales):
        """
        Args:
            variables: lista de variables
            probabilidades_transicion: P(X_t|X_t-1)
            probabilidades_iniciales: P(X_0)
        """
        self.variables = variables
        self.prob_transicion = probabilidades_transicion
        self.prob_iniciales = probabilidades_iniciales
        self.estados_tiempo = [probabilidades_iniciales]
    
    def avanzar_tiempo(self):
        """Avanza un paso de tiempo usando el modelo de transición"""
        estado_actual = self.estados_tiempo[-1]
        nuevo_estado = {}
        
        for var in self.variables:
            # Calcular probabilidad en t+1 basada en t
            prob = 0
            for valor_previo, prob_previo in estado_actual.items():
                prob += prob_previo * self.prob_transicion.get((valor_previo, var), 0)
            nuevo_estado[var] = prob
        
        self.estados_tiempo.append(nuevo_estado)
        return nuevo_estado
    
    def filtrado(self, evidencia):
        """
        Actualiza creencias dado evidencia (filtrado forward)
        Args:
            evidencia: observación en tiempo actual
        Returns:
            distribución de probabilidad actualizada
        """
        estado_actual = self.estados_tiempo[-1]
        
        # Aplicar evidencia (simplificado)
        estado_filtrado = {}
        for var, prob in estado_actual.items():
            if var == evidencia:
                estado_filtrado[var] = prob * 0.9  # Mayor peso a la evidencia
            else:
                estado_filtrado[var] = prob * 0.1
        
        # Normalizar
        total = sum(estado_filtrado.values())
        if total > 0:
            estado_filtrado = {v: p/total for v, p in estado_filtrado.items()}
        
        return estado_filtrado


# ============================================================================
# 32. TEORÍA DE JUEGOS: EQUILIBRIOS Y MECANISMOS
# ============================================================================

def equilibrio_nash_puro(matriz_pagos_j1, matriz_pagos_j2):
    """
    Encuentra equilibrios de Nash en estrategias puras
    Args:
        matriz_pagos_j1: matriz de pagos del jugador 1
        matriz_pagos_j2: matriz de pagos del jugador 2
    Returns:
        lista de equilibrios (fila, columna)
    """
    equilibrios = []
    filas = len(matriz_pagos_j1)
    columnas = len(matriz_pagos_j1[0])
    
    for i in range(filas):
        for j in range(columnas):
            # Verificar si (i,j) es equilibrio de Nash
            # J1 no quiere desviarse de fila i dada columna j
            es_mejor_j1 = all(matriz_pagos_j1[i][j] >= matriz_pagos_j1[k][j] 
                             for k in range(filas))
            
            # J2 no quiere desviarse de columna j dada fila i
            es_mejor_j2 = all(matriz_pagos_j2[i][j] >= matriz_pagos_j2[i][k] 
                             for k in range(columnas))
            
            if es_mejor_j1 and es_mejor_j2:
                equilibrios.append((i, j))
    
    return equilibrios


def estrategia_minimax(matriz_pagos):
    """
    Encuentra estrategia minimax para juegos de suma cero
    Args:
        matriz_pagos: matriz de pagos del jugador maximizador
    Returns:
        (estrategia_fila, estrategia_columna, valor)
    """
    filas = len(matriz_pagos)
    columnas = len(matriz_pagos[0])
    
    # Jugador 1 (filas) maximiza el mínimo
    max_min = float('-inf')
    mejor_fila = 0
    
    for i in range(filas):
        min_en_fila = min(matriz_pagos[i])
        if min_en_fila > max_min:
            max_min = min_en_fila
            mejor_fila = i
    
    # Jugador 2 (columnas) minimiza el máximo
    min_max = float('inf')
    mejor_columna = 0
    
    for j in range(columnas):
        max_en_columna = max(matriz_pagos[i][j] for i in range(filas))
        if max_en_columna < min_max:
            min_max = max_en_columna
            mejor_columna = j
    
    return mejor_fila, mejor_columna, matriz_pagos[mejor_fila][mejor_columna]


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== UTILIDAD Y TOMA DE DECISIONES ===\n")
    
    # Ejemplo: MDP simple (robot en grid)
    print("29. Proceso de Decisión de Markov:")
    estados = ['s1', 's2', 's3', 'meta']
    acciones = ['ir_derecha', 'quedarse']
    
    # Transiciones: P(s'|s,a)
    transiciones = {
        ('s1', 'ir_derecha', 's2'): 0.8,
        ('s1', 'ir_derecha', 's1'): 0.2,
        ('s2', 'ir_derecha', 's3'): 0.8,
        ('s2', 'ir_derecha', 's2'): 0.2,
        ('s3', 'ir_derecha', 'meta'): 1.0,
        ('s1', 'quedarse', 's1'): 1.0,
        ('s2', 'quedarse', 's2'): 1.0,
        ('s3', 'quedarse', 's3'): 1.0,
        ('meta', 'ir_derecha', 'meta'): 1.0,
        ('meta', 'quedarse', 'meta'): 1.0,
    }
    
    # Recompensas: R(s,a)
    recompensas = {
        ('s1', 'ir_derecha'): -1,
        ('s2', 'ir_derecha'): -1,
        ('s3', 'ir_derecha'): 10,
        ('meta', 'ir_derecha'): 0,
        ('s1', 'quedarse'): -1,
        ('s2', 'quedarse'): -1,
        ('s3', 'quedarse'): -1,
        ('meta', 'quedarse'): 0,
    }
    
    mdp = MDP(estados, acciones, transiciones, recompensas, gamma=0.9)
    
    print("27. Iteración de Valores:")
    valores = mdp.resolver_iteracion_valores()
    print(f"   Valores óptimos: {valores}\n")
    
    print("28. Iteración de Políticas:")
    politica = mdp.resolver_iteracion_politicas()
    print(f"   Política óptima: {politica}\n")
    
    # Ejemplo: Teoría de Juegos
    print("32. Equilibrio de Nash:")
    # Juego del Dilema del Prisionero
    pagos_j1 = [
        [3, 0],  # Cooperar, Traicionar
        [5, 1]   # Traicionar, Traicionar
    ]
    pagos_j2 = [
        [3, 5],
        [0, 1]
    ]
    
    equilibrios = equilibrio_nash_puro(pagos_j1, pagos_j2)
    print(f"   Equilibrios de Nash: {equilibrios}")
    print("   (1,1) = Ambos traicionan\n")
    
    print("26. Valor de la Información Perfecta:")
    probs = [0.6, 0.4]  # Probabilidades de estados
    utils = {
        0: {'A1': 100, 'A2': 50},
        1: {'A1': 20, 'A2': 80}
    }
    vip = valor_informacion_perfecta(probs, utils)
    print(f"   VIP = {vip:.2f}")