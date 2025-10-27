import random
import math
from collections import defaultdict

# ============================================================================
# CLASE DE AMBIENTE SIMPLE PARA PRUEBAS (DEPENDENCIA)
# ============================================================================

class AmbienteSimple:
    """Ambiente simple de grid world para probar algoritmos de RL"""
    def __init__(self, tamano=4):
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
        if accion == 'arriba' and y > 0: y -= 1
        elif accion == 'abajo' and y < self.tamano - 1: y += 1
        elif accion == 'izquierda' and x > 0: x -= 1
        elif accion == 'derecha' and x < self.tamano - 1: x += 1
        nuevo_estado = (x, y)
        if nuevo_estado == self.estado_meta:
            recompensa = 10
            terminado = True
        else:
            recompensa = -0.1
            terminado = False
        return nuevo_estado, recompensa, terminado

# ============================================================================
# FUNCIÓN DE POLÍTICA (DEPENDENCIA)
# ============================================================================

def seleccionar_accion_softmax(theta, estado, acciones, temperatura=1.0):
    """Selecciona acción usando softmax sobre parámetros"""
    logits = [theta.get((estado, a), 0) / temperatura for a in acciones]
    
    # Evitar overflow (restar el max_logit es estable numéricamente)
    max_logit = max(logits)
    exp_logits = [math.exp(l - max_logit) for l in logits]
    suma_exp_logits = sum(exp_logits)
    
    if suma_exp_logits == 0:
        return random.choice(acciones) # Evitar división por cero
        
    probs = [e / suma_exp_logits for e in exp_logits]
    
    # Muestrear según probabilidades
    r = random.random()
    acum = 0
    for a, p in zip(acciones, probs):
        acum += p
        if r <= acum:
            return a
    
    return acciones[-1] # Fallback por precisión de flotantes

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
    # Inicializar parámetros de política (preferencias)
    theta = defaultdict(float)  # Parámetros {(estado, accion): peso}
    
    for _ in range(num_episodios):
        episodio = []
        s = env.reset()
        terminado = False
        
        # Generar episodio siguiendo política actual (softmax)
        while not terminado:
            a = seleccionar_accion_softmax(theta, s, env.acciones)
            s_siguiente, r, terminado = env.step(s, a)
            episodio.append((s, a, r))
            s = s_siguiente
        
        # Actualizar parámetros con gradiente
        G = 0
        estados_acciones_visitados = set()
        
        # Recorrer el episodio en reversa
        for t in range(len(episodio) - 1, -1, -1):
            s, a, r = episodio[t]
            G = r + gamma * G
            
            # Actualizar solo la primera visita (First-visit REINFORCE)
            if (s, a) not in estados_acciones_visitados:
                
                # Calcular probabilidades softmax (pi(a|s, theta))
                logits = [theta.get((s, a_p), 0) for a_p in env.acciones]
                max_logit = max(logits)
                exp_logits = [math.exp(l - max_logit) for l in logits]
                suma_exp = sum(exp_logits)
                probs = [e / suma_exp for e in exp_logits]
                
                prob_a = probs[env.acciones.index(a)]

                # Actualización de gradiente de política
                # grad(log(pi(a|s))) = grad(theta_sa) - sum(pi(a'|s) * grad(theta_sa'))
                for a_prima in env.acciones:
                    if a_prima == a:
                        grad_log_pi = (1 - prob_a)
                    else:
                        prob_a_prima = probs[env.acciones.index(a_prima)]
                        grad_log_pi = -prob_a_prima
                    
                    # Aplicar actualización
                    theta[(s, a_prima)] += alpha * G * grad_log_pi
                
                estados_acciones_visitados.add((s, a))
    
    return dict(theta)


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
    V = defaultdict(float)      # Valores de estado (crítico)
    
    for _ in range(num_episodios):
        s = env.reset()
        terminado = False
        
        while not terminado:
            # Actor: seleccionar acción
            a = seleccionar_accion_softmax(theta, s, env.acciones)
            
            # Ejecutar acción
            s_siguiente, r, terminado = env.step(s, a)
            
            # Crítico: calcular error TD (ventaja)
            delta = r + gamma * V[s_siguiente] - V[s] # V[meta] es 0 por defecto
            
            # Actualizar crítico (aprende V(s))
            V[s] += alpha_critic * delta
            
            # Actualizar actor (aprende theta)
            # (Usamos una forma simplificada del gradiente log-softmax)
            theta[(s, a)] += alpha_actor * delta
            
            s = s_siguiente
    
    return dict(theta), dict(V)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 37. Búsqueda de la Política ===\n")

    # Crear ambiente
    env = AmbienteSimple(tamano=4)

    print("1. REINFORCE (Policy Gradient):")
    theta_rf = reinforce(env, num_episodios=500, alpha=0.001, gamma=0.9)
    print(f"   Parámetros de política aprendidos: {len(theta_rf)}")
    print(f"   Muestra de parámetros:")
    for i, (clave, valor) in enumerate(list(theta_rf.items())[:5]):
        print(f"      θ{clave} = {valor:.3f}")
    print()

    print("2. Actor-Critic:")
    theta_ac, V_ac = actor_critic(env, num_episodios=500, alpha_actor=0.01, alpha_critic=0.1, gamma=0.9)
    print(f"   Parámetros de actor aprendidos: {len(theta_ac)}")
    print(f"   Valores de crítico aprendidos: {len(V_ac)}")
    print(f"   Muestra de parámetros de actor:")
    for i, (clave, valor) in enumerate(list(theta_ac.items())[:5]):
         print(f"      θ{clave} = {valor:.3f}")
    print(f"   Muestra de valores de crítico:")
    for i, (clave, valor) in enumerate(list(V_ac.items())[:5]):
         print(f"      V{clave} = {valor:.3f}")
    print()