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
            observacion_prob: P(o|s',a) (Prob de observar 'o' al llegar a 's_prima' tras 'a')
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
        Actualiza la distribución de creencia sobre estados (Filtro de Bayes)
        Args:
            creencia: dict {estado: probabilidad} (creencia en t)
            accion: acción tomada en t
            observacion: observación recibida en t+1
        Returns:
            nueva creencia (en t+1)
        """
        nueva_creencia = {}
        
        for s_prima in self.estados:
            # P(o | s', a)
            obs_prob = self.observacion_prob.get((s_prima, accion, observacion), 0)
            
            # Sumatoria sobre s de [ P(s' | s, a) * P(s) ]
            suma_transicion_creencia = 0
            for s in self.estados:
                trans_prob = self.transiciones.get((s, accion, s_prima), 0)
                suma_transicion_creencia += trans_prob * creencia.get(s, 0)
            
            # P(s') = P(o | s', a) * Suma( P(s' | s, a) * P(s) )
            nueva_creencia[s_prima] = obs_prob * suma_transicion_creencia
        
        # Normalizar (dividir por P(o | a, creencia))
        total = sum(nueva_creencia.values())
        if total > 0:
            nueva_creencia = {s: p/total for s, p in nueva_creencia.items()}
        
        return nueva_creencia

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 30. MDP Parcialmente Observable (POMDP) ===\n")
    
    # Ejemplo: Robot en pasillo 
    estados = ['s1', 's2', 's3']
    acciones = ['avanzar']
    observaciones = ['pared', 'puerta']
    
    # Modelo de Transición P(s'|s,a)
    transiciones = {
        ('s1', 'avanzar', 's2'): 1.0,
        ('s2', 'avanzar', 's3'): 1.0,
        ('s3', 'avanzar', 's3'): 1.0, # Se queda
    }
    
    # Modelo de Observación P(o|s',a)
    obs_prob = {
        ('s1', 'avanzar', 'pared'): 1.0,
        ('s2', 'avanzar', 'puerta'): 1.0,
        ('s3', 'avanzar', 'pared'): 1.0,
    }
    
    # (Recompensas y gamma no son necesarias para solo actualizar creencias)
    pomdp = POMDP(estados, acciones, observaciones, transiciones, obs_prob, {}, gamma=0.9)
    
    # Creencia inicial: no sabe dónde está
    creencia_inicial = {'s1': 0.33, 's2': 0.33, 's3': 0.33}
    
    print(f"Creencia inicial: {creencia_inicial}")
    
    # 1. Agente toma acción 'avanzar' y observa 'puerta'
    accion = 'avanzar'
    obs = 'puerta'
    creencia_t1 = pomdp.actualizar_creencia(creencia_inicial, accion, obs)
    
    print(f"\nAcción: '{accion}', Observación: '{obs}'")
    print(f"Creencia t=1: {creencia_t1}")
    # (Debería estar seguro de que está en s2)
    
    # 2. Agente toma 'avanzar' de nuevo y observa 'pared'
    obs = 'pared'
    creencia_t2 = pomdp.actualizar_creencia(creencia_t1, accion, obs)

    print(f"\nAcción: '{accion}', Observación: '{obs}'")
    print(f"Creencia t=2: {creencia_t2}")
    # (Debería estar seguro de que está en s3)