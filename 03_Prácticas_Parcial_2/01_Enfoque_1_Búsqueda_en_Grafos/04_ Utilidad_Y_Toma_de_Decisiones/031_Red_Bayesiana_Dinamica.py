# ============================================================================
# 31. RED BAYESIANA DINÁMICA
# ============================================================================

class RedBayesianaDinamica:
    """
    Representa una Red Bayesiana que evoluciona en el tiempo
    (Modelo de Markov Oculto - HMM - es un tipo de DBN)
    """
    def __init__(self, estados_ocultos, observaciones_posibles, 
                 prob_inicial, prob_transicion, prob_emision):
        """
        Args:
            estados_ocultos: lista de estados (ej. 'lluvia', 'sol')
            observaciones_posibles: lista de obs (ej. 'paraguas', 'sin_paraguas')
            prob_inicial: P(X_0) dict {estado: prob}
            prob_transicion: P(X_t | X_t-1) dict {(estado_prev, estado_act): prob}
            prob_emision: P(E_t | X_t) dict {(estado_act, obs): prob}
        """
        self.estados = estados_ocultos
        self.observaciones = observaciones_posibles
        self.prob_inicial = prob_inicial
        self.prob_transicion = prob_transicion
        self.prob_emision = prob_emision
        self.creencia_actual = prob_inicial
    
    def predecir(self):
        """Avanza la creencia un paso en el tiempo (sin evidencia)"""
        nueva_creencia = {s: 0 for s in self.estados}
        
        for s_actual in self.estados:
            # Sumatoria sobre s_previo de [ P(s_actual | s_previo) * P(s_previo) ]
            suma = 0
            for s_previo in self.estados:
                prob = self.prob_transicion.get((s_previo, s_actual), 0)
                suma += prob * self.creencia_actual.get(s_previo, 0)
            nueva_creencia[s_actual] = suma
        
        self.creencia_actual = nueva_creencia
    
    def actualizar_con_evidencia(self, evidencia):
        """
        Actualiza creencias dado evidencia (filtrado forward)
        Args:
            evidencia: observación en tiempo actual
        """
        # P(E | X) * P(X)
        for s in self.estados:
            prob_em = self.prob_emision.get((s, evidencia), 0)
            self.creencia_actual[s] = prob_em * self.creencia_actual[s]
            
        # Normalizar
        total = sum(self.creencia_actual.values())
        if total > 0:
            self.creencia_actual = {s: p/total for s, p in self.creencia_actual.items()}

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 31. Red Bayesiana Dinámica (HMM) ===\n")
    
    # Ejemplo: ¿Está lloviendo?
    estados = ['Lluvia', 'Sol']
    obs = ['Paraguas', 'Sin_Paraguas']
    
    # P(X_0)
    p_inicial = {'Lluvia': 0.5, 'Sol': 0.5}
    
    # P(X_t | X_t-1)
    p_trans = {
        ('Lluvia', 'Lluvia'): 0.7,
        ('Lluvia', 'Sol'): 0.3,
        ('Sol', 'Lluvia'): 0.3,
        ('Sol', 'Sol'): 0.7,
    }
    
    # P(E_t | X_t)
    p_emision = {
        ('Lluvia', 'Paraguas'): 0.9,
        ('Lluvia', 'Sin_Paraguas'): 0.1,
        ('Sol', 'Paraguas'): 0.2,
        ('Sol', 'Sin_Paraguas'): 0.8,
    }
    
    dbn = RedBayesianaDinamica(estados, obs, p_inicial, p_trans, p_emision)
    
    print(f"Creencia t=0 (inicial): {dbn.creencia_actual}")
    
    # Día 1: Observamos 'Paraguas'
    # 1. Predecir (avanzar t-1 a t)
    dbn.predecir()
    print(f"Creencia t=1 (predicción): {dbn.creencia_actual}")
    # 2. Actualizar (usar evidencia)
    dbn.actualizar_con_evidencia('Paraguas')
    print(f"Creencia t=1 (filtrado): {dbn.creencia_actual}\n") # Debería ser alta P(Lluvia)

    # Día 2: Observamos 'Paraguas'
    dbn.predecir()
    print(f"Creencia t=2 (predicción): {dbn.creencia_actual}")
    dbn.actualizar_con_evidencia('Paraguas')
    print(f"Creencia t=2 (filtrado): {dbn.creencia_actual}\n") # Aún más alta P(Lluvia)