"""
APRENDIZAJE POR REFUERZO
Algoritmos 33-37: Aprendizaje por interacción con el ambiente
"""

import random
import math
from collections import defaultdict

# ============================================================================
# 33. APRENDIZAJE POR REFUERZO PASIVO
# ============================================================================

def aprendizaje_td_pasivo(episodios, politica, alpha=0.1, gamma=0.9):
    """
    Temporal Difference Learning pasivo (sigue política fija)
    Args:
        episodios: lista de episodios [(s, a, r, s'), ...]
        politica: política fija a seguir {estado: accion}
        alpha: tasa de aprendizaje
        gamma: factor de descuento
    Returns:
        valores estimados de estados
    """
    V = defaultdict(float)  # Valores de estados
    
    for episodio in episodios:
        for s, a, r, s_siguiente in episodio:
            # Actualización TD(0)
            V[s] = V[s] + alpha * (r + gamma * V[s_siguiente] - V[s])
    
    return dict(V)


def montecarlo_pasivo(episodios, politica, gamma=0.9):
    """
    Aprendizaje Monte Carlo pasivo
    Args:
        episodios: lista de episodios completos
        politica: política fija
        gamma: factor de descuento
    Returns:
        valores estimados
    """
    retornos = defaultdict(list)  # Retornos observados por estado
    
    for episodio in episodios:
        G = 0  # Retorno acumulado
        
        # Recorrer episodio en reversa
        for s, a, r, _ in reversed(episodio):
            G = r + gamma * G
            retornos[s].append(G)
    
    # Promediar retornos
    V = {s: sum(returns)/len(returns) for s, returns in retornos.items()}
    return V


# ============================================================================
# 34. APRENDIZAJE POR REFUERZO ACTIVO
# ============================================================================

def sarsa(env, num_episodios=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """
    SARSA: on-policy TD control
    Args:
        env: ambiente con métodos step(s, a) y reset()
        num_episodios: número de episodios de entrenamiento
        alpha: tasa de aprendizaje
        gamma: factor de descuento
        epsilon: exploración epsilon-greedy
    Returns:
        Q-valores aprendidos {(estado, accion): valor}
    """
    Q = defaultdict(float)
    
    for _ in range(num_episodios):
        s = env.reset()
        a = epsilon_greedy(Q, s, env.acciones, epsilon)
        
        terminado = False
        while not terminado:
            # Ejecutar acción
            s_siguiente, r, terminado = env.step(s, a)
            a_siguiente = epsilon_greedy(Q, s_siguiente, env.acciones, epsilon)
            
            # Actualización SARSA
            Q[(s, a)] += alpha * (r + gamma * Q[(s_siguiente, a_siguiente)] - Q[(s, a)])
            
            s = s_siguiente
            a = a_siguiente
    
    return dict(Q)


def epsilon_greedy(Q, estado, acciones, epsilon):
    """Política epsilon-greedy"""
    if random.random() < epsilon:
        return random.choice(acciones)
    else:
        # Acción con mayor Q-valor
        return max(acciones, key=lambda a: Q[(estado, a)])


# ============================================================================
# 35. Q-LEARNING
# ============================================================================

def q_learning(env, num_episodios=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    """
    Q-Learning: off-policy TD control
    Args:
        env: ambiente de aprendizaje
        num_episodios: episodios de entrenamiento
        alpha: tasa de aprendizaje
        gamma: factor de descuento
        epsilon: exploración
    Returns:
        Q-valores óptimos
    """
    Q = defaultdict(float)
    
    for _ in range(num_episodios):
        s = env.reset()
        terminado = False
        
        while not terminado:
            # Seleccionar acción con epsilon-greedy
            a = epsilon_greedy(Q, s, env.acciones, epsilon)
            
            # Ejecutar acción
            s_siguiente, r, terminado = env.step(s, a)
            
            # Actualización Q-Learning (usa max, no la acción siguiente real)
            mejor_q_siguiente = max(Q[(s_siguiente, a_prima)] 
                                   for a_prima in env.acciones)
            Q[(s, a)] += alpha * (r + gamma * mejor_q_siguiente - Q[(s, a)])
            
            s = s_siguiente
    
    return dict(Q)


# ============================================================================
# 36. EXPLORACIÓN VS. EXPLOTACIÓN
# ============================================================================

def ucb1(Q, N, estado, acciones, c=2):
    """
    Upper Confidence Bound para balancear exploración/explotación
    Args:
        Q: Q-valores estimados
        N: contador de visitas {(estado, accion): conteo}
        estado: estado actual
        acciones: acciones posibles
        c: constante de exploración
    Returns:
        acción seleccionada
    """
    total_visitas = sum(N.get((estado, a), 0) for a in acciones)
    
    if total_visitas == 0:
        return random.choice(acciones)
    
    # Calcular UCB para cada acción
    mejor_accion = None
    mejor_ucb = float('-inf')
    
    for a in acciones:
        n_a = N.get((estado, a), 0)
        
        if n_a == 0:
            return a  # Priorizar acciones no exploradas
        
        q_valor = Q.get((estado, a), 0)
        bonus_exploracion = c * math.sqrt(math.log(total_visitas) / n_a)
        ucb = q_valor + bonus_exploracion
        
        if ucb > mejor_ucb:
            mejor_ucb = ucb
            mejor_accion = a
    
    return mejor_accion


def thompson_sampling(exitos, intentos, acciones):
    """
    Thompson Sampling para bandidos multi-brazo
    Args:
        exitos: dict {accion: num_exitos}
        intentos: dict {accion: num_intentos}
        acciones: lista de acciones
    Returns:
        acción seleccionada
    """
    mejor_accion = None
    mejor_muestra = -1
    
    for a in acciones:
        alpha = exitos.get(a, 1)  # Parámetro de distribución Beta
        beta = intentos.get(a, 1) - exitos.get(a, 0)
        
        # Muestrear de distribución Beta
        muestra = random.betavariate(alpha, beta)
        
        if muestra > mejor_muestra:
            mejor_muestra = muestra
            mejor_accion = a
    
    return mejor_accion


def epsilon_decreciente(episodio, epsilon_inicial=1.0, epsilon_final=0.01, decay=0.995):
    """
    Estrategia de exploración con epsilon decreciente
    Args:
        episodio: número de episodio actual
        epsilon_inicial: epsilon al inicio
        epsilon_final: epsilon mínimo
        decay: tasa de decaimiento
    Returns:
        epsilon actual
    """
    epsilon = epsilon_inicial * (decay ** episodio)
    return max(epsilon_final, epsilon)


# ============================================================================
# 37. BÚSQUEDA DE LA POLÍTICA
# ============================================================================

def reinforce(env, num_episodios=1000, alpha=0.01, gamma=0.9):
    """
    Algoritmo REINFORCE (Policy Gradient)
    Aprende parámetros de política directamente
    Args:
        env: ambiente
        num_episodios: episodios de entrenamiento
        alpha: tasa de aprendizaje
        gamma: factor de descuento
    Returns:
        política aprendida (parámetros)
    """
    # Inicializar parámetros de política (simplificado)
    theta = defaultdict(float)  # Parámetros {(estado, accion): peso}
    
    for _ in range(num_episodios):
        episodio = []
        s = env.reset()
        terminado = False
        
        # Generar episodio siguiendo política actual
        while not terminado:
            a = seleccionar_accion_softmax(theta, s, env.acciones)
            s_siguiente, r, terminado = env.step(s, a)
            episodio.append((s, a, r))
            s = s_siguiente
        
        # Actualizar parámetros con gradiente
        G = 0
        for t in range(len(episodio) - 1, -1, -1):
            s, a, r = episodio[t]
            G = r + gamma * G
            
            # Actualización de gradiente de política
            for a_prima in env.acciones:
                if a_prima == a:
                    theta[(s, a)] += alpha * G
                else:
                    theta[(s, a_prima)] -= alpha * G / (len(env.acciones) - 1)
    
    return dict(theta)


def seleccionar_accion_softmax(theta, estado, acciones, temperatura=1.0):
    """Selecciona acción usando softmax sobre parámetros"""
    logits = [theta.get((estado, a), 0) / temperatura for a in acciones]
    
    # Evitar overflow
    max_logit = max(logits)
    exp_logits = [math.exp(l - max_logit) for l in logits]
    suma = sum(exp_logits)
    
    probs = [e / suma for e in exp_logits]
    
    # Muestrear según probabilidades
    r = random.random()
    acum = 0
    for a, p in zip(acciones, probs):
        acum += p
        if r <= acum:
            return a
    
    return acciones[-1]


def actor_critic(env, num_episodios=1000, alpha_actor=0.01, alpha_critic=0.1, gamma=0.9):
    """
    Algoritmo Actor-Critic
    Combina búsqueda de política (actor) con estimación de valor (crítico)
    Args:
        env: ambiente
        num_episodios: episodios de entrenamiento
        alpha_actor: tasa de aprendizaje del actor
        alpha_critic: tasa de aprendizaje del crítico
        gamma: factor de descuento
    Returns:
        (política, valores)
    """
    theta = defaultdict(float)  # Parámetros de política (actor)
    V = defaultdict(float)  # Valores de estado (crítico)
    
    for _ in range(num_episodios):
        s = env.reset()
        terminado = False
        
        while not terminado:
            # Actor: seleccionar acción
            a = seleccionar_accion_softmax(theta, s, env.acciones)
            
            # Ejecutar acción
            s_siguiente, r, terminado = env.step(s, a)
            
            # Crítico: calcular error TD
            delta = r + gamma * V[s_siguiente] - V[s]
            
            # Actualizar crítico
            V[s] += alpha_critic * delta
            
            # Actualizar actor
            theta[(s, a)] += alpha_actor * delta
            
            s = s_siguiente
    
    return dict(theta), dict(V)


# ============================================================================
# CLASE DE AMBIENTE SIMPLE PARA PRUEBAS
# ============================================================================

class AmbienteSimple:
    """Ambiente simple de grid world para probar algoritmos de RL"""
    def __init__(self, tamano=5):
        self.tamano = tamano
        self.acciones = ['arriba', 'abajo', 'izquierda', 'derecha']
        self.estado_meta = (tamano-1, tamano-1)
        self.reset()
    
    def reset(self):
        """Reinicia al estado inicial"""
        self.estado_actual = (0, 0)
        return self.estado_actual
    
    def step(self, estado, accion):
        """
        Ejecuta una acción
        Returns: (nuevo_estado, recompensa, terminado)
        """
        x, y = estado
        
        # Aplicar acción
        if accion == 'arriba' and y > 0:
            y -= 1
        elif accion == 'abajo' and y < self.tamano - 1:
            y += 1
        elif accion == 'izquierda' and x > 0:
            x -= 1
        elif accion == 'derecha' and x < self.tamano - 1:
            x += 1
        
        nuevo_estado = (x, y)
        
        # Recompensa
        if nuevo_estado == self.estado_meta:
            recompensa = 10
            terminado = True
        else:
            recompensa = -0.1
            terminado = False
        
        return nuevo_estado, recompensa, terminado


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== APRENDIZAJE POR REFUERZO ===\n")
    
    # Crear ambiente
    env = AmbienteSimple(tamano=4)
    
    print("35. Q-Learning:")
    Q = q_learning(env, num_episodios=500, alpha=0.1, gamma=0.9, epsilon=0.2)
    print(f"   Total de pares (estado, acción) aprendidos: {len(Q)}")
    print(f"   Muestra de Q-valores:")
    for i, (clave, valor) in enumerate(list(Q.items())[:5]):
        print(f"      Q{clave} = {valor:.3f}")
    print()
    
    print("34. SARSA:")
    Q_sarsa = sarsa(env, num_episodios=500, alpha=0.1, gamma=0.9, epsilon=0.2)
    print(f"   Total de pares (estado, acción) aprendidos: {len(Q_sarsa)}")
    print(f"   Muestra de Q-valores:")
    for i, (clave, valor) in enumerate(list(Q_sarsa.items())[:5]):
        print(f"      Q{clave} = {valor:.3f}")
    print()
    
    # Ejemplo de exploración vs explotación
    print("36. Exploración vs. Explotación (UCB1):")
    Q_test = {((0, 0), 'derecha'): 5.0, ((0, 0), 'abajo'): 3.0}
    N_test = {((0, 0), 'derecha'): 10, ((0, 0), 'abajo'): 5}
    accion = ucb1(Q_test, N_test, (0, 0), ['arriba', 'abajo', 'izquierda', 'derecha'])
    print(f"   Acción seleccionada: {accion}")
    print()
    
    print("37. REINFORCE (Policy Gradient):")
    theta = reinforce(env, num_episodios=200, alpha=0.01, gamma=0.9)
    print(f"   Parámetros de política aprendidos: {len(theta)}")
    print(f"   Muestra de parámetros:")
    for i, (clave, valor) in enumerate(list(theta.items())[:5]):
        print(f"      θ{clave} = {valor:.3f}")
    print()
    
    # Comparación de estrategias de exploración
    print("Estrategias de Exploración:")
    print(f"   Epsilon en episodio 0: {epsilon_decreciente(0):.3f}")
    print(f"   Epsilon en episodio 100: {epsilon_decreciente(100):.3f}")
    print(f"   Epsilon en episodio 500: {epsilon_decreciente(500):.3f}")
    print()
    
    # Ejemplo de Thompson Sampling
    print("Thompson Sampling:")
    exitos = {'A': 8, 'B': 6, 'C': 4}
    intentos = {'A': 10, 'B': 10, 'C': 10}
    accion_ts = thompson_sampling(exitos, intentos, ['A', 'B', 'C'])
    print(f"   Acción seleccionada: {accion_ts}")
    print(f"   Tasas de éxito: A=80%, B=60%, C=40%")
    print()
    
    # Demostrar diferencia entre Q-Learning y SARSA
    print("Diferencia Q-Learning vs SARSA:")
    print("   Q-Learning: Off-policy (aprende política óptima independiente)")
    print("   SARSA: On-policy (aprende política que está siguiendo)")
    print("   Q-Learning converge más rápido pero puede ser inestable")
    print("   SARSA es más conservador y estable")