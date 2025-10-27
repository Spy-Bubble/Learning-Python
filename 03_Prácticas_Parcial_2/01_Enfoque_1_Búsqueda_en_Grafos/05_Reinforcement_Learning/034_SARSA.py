import random
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
# FUNCIÓN DE POLÍTICA (DEPENDENCIA)
# ============================================================================

def epsilon_greedy(Q, estado, acciones, epsilon):
    """Política epsilon-greedy"""
    if random.random() < epsilon:
        return random.choice(acciones)
    else:
        # Acción con mayor Q-valor (o una aleatoria si todos son 0)
        q_valores = {a: Q[(estado, a)] for a in acciones}
        max_q = max(q_valores.values())
        mejores_acciones = [a for a, q in q_valores.items() if q == max_q]
        return random.choice(mejores_acciones)

# ============================================================================
# 34. APRENDIZAJE POR REFUERZO ACTIVO (SARSA)
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
            # Elegir acción siguiente basado en la política
            a_siguiente = epsilon_greedy(Q, s_siguiente, env.acciones, epsilon)
            
            # Actualización SARSA (Estado, Acción, Recompensa, S_siguiente, A_siguiente)
            Q[(s, a)] += alpha * (r + gamma * Q[(s_siguiente, a_siguiente)] - Q[(s, a)])
            
            s = s_siguiente
            a = a_siguiente
    
    return dict(Q)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 34. Aprendizaje Activo (SARSA) ===\n")
    
    # Crear ambiente
    env = AmbienteSimple(tamano=4)

    print("Entrenando con SARSA...")
    Q_sarsa = sarsa(env, num_episodios=500, alpha=0.1, gamma=0.9, epsilon=0.2)
    print(f"   Total de pares (estado, acción) aprendidos: {len(Q_sarsa)}")
    print(f"   Muestra de Q-valores:")
    for i, (clave, valor) in enumerate(list(Q_sarsa.items())[:5]):
        print(f"      Q{clave} = {valor:.3f}")
    
    print(f"\n   Valor Q en (0,0) 'derecha': {Q_sarsa.get(((0,0), 'derecha'), 0):.3f}")
    print(f"   Valor Q en (0,0) 'abajo': {Q_sarsa.get(((0,0), 'abajo'), 0):.3f}")