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
            
            # Actualización Q-Learning (off-policy)
            # Usa el máximo Q-valor del estado siguiente (política greedy)
            mejor_q_siguiente = max(Q[(s_siguiente, a_prima)] 
                                  for a_prima in env.acciones)
            
            Q[(s, a)] += alpha * (r + gamma * mejor_q_siguiente - Q[(s, a)])
            
            s = s_siguiente
    
    return dict(Q)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 35. Q-Learning ===\n")
    
    # Crear ambiente
    env = AmbienteSimple(tamano=4)
    
    print("Entrenando con Q-Learning...")
    Q = q_learning(env, num_episodios=500, alpha=0.1, gamma=0.9, epsilon=0.2)
    print(f"   Total de pares (estado, acción) aprendidos: {len(Q)}")
    print(f"   Muestra de Q-valores:")
    for i, (clave, valor) in enumerate(list(Q.items())[:5]):
        print(f"      Q{clave} = {valor:.3f}")

    print(f"\n   Valor Q en (0,0) 'derecha': {Q.get(((0,0), 'derecha'), 0):.3f}")
    print(f"   Valor Q en (0,0) 'abajo': {Q.get(((0,0), 'abajo'), 0):.3f}")