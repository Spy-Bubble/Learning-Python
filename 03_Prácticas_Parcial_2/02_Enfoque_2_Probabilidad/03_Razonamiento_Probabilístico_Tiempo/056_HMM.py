import random

# ============================================================================
# 19. MODELOS OCULTOS DE MARKOV (HMM)
# ============================================================================

class HMM:
    """
    Modelo Oculto de Markov
    """
    def __init__(self, estados_ocultos, observaciones, transiciones, emisiones, inicial):
        """
        Args:
            estados_ocultos: lista de estados ocultos
            observaciones: lista de observaciones posibles
            transiciones: P(s'|s) dict {(s_prev, s_act): prob}
            emisiones: P(o|s) dict {(obs, estado): prob}
            inicial: P(s_0) dict {estado: prob}
        """
        self.estados = estados_ocultos
        self.observaciones = observaciones
        self.transiciones = transiciones
        self.emisiones = emisiones
        self.inicial = inicial
    
    def viterbi(self, secuencia_obs):
        """
        Algoritmo de Viterbi: encuentra la secuencia más probable de estados
        Args:
            secuencia_obs: lista de observaciones
        Returns:
            secuencia más probable de estados
        """
        T = len(secuencia_obs)
        
        # Inicializar
        viterbi_prob = [{} for _ in range(T)]
        camino = [{} for _ in range(T)]
        
        # t = 0
        obs_0 = secuencia_obs[0]
        for s in self.estados:
            viterbi_prob[0][s] = (self.inicial.get(s, 0) * self.emisiones.get((obs_0, s), 0))
            camino[0][s] = [s] # Camino termina en s
        
        # t > 0
        for t in range(1, T):
            obs_t = secuencia_obs[t]
            for s_nuevo in self.estados:
                # Encontrar estado previo con máxima probabilidad
                max_prob = -1
                mejor_estado = None
                
                emision_prob = self.emisiones.get((obs_t, s_nuevo), 0)
                
                for s_prev in self.estados:
                    prob = (viterbi_prob[t-1].get(s_prev, 0) * self.transiciones.get((s_prev, s_nuevo), 0))
                    
                    if prob > max_prob:
                        max_prob = prob
                        mejor_estado = s_prev
                
                viterbi_prob[t][s_nuevo] = max_prob * emision_prob
                
                if mejor_estado:
                    camino[t][s_nuevo] = camino[t-1][mejor_estado] + [s_nuevo]
                else:
                    camino[t][s_nuevo] = [s_nuevo]
        
        # Encontrar el mejor camino final
        max_prob_final = -1
        mejor_estado_final = None
        for s, prob in viterbi_prob[T-1].items():
            if prob > max_prob_final:
                max_prob_final = prob
                mejor_estado_final = s
        
        if mejor_estado_final is None:
            return [] # No se encontró camino
            
        return camino[T-1][mejor_estado_final]
    
    def generar_secuencia(self, longitud):
        """
        Genera una secuencia de observaciones del HMM
        Args:
            longitud: longitud de la secuencia
        Returns:
            (estados, observaciones)
        """
        estados_seq = []
        obs_seq = []
        
        # Estado inicial
        estados_lista = list(self.estados)
        pesos_iniciales = [self.inicial.get(s, 0) for s in estados_lista]
        if sum(pesos_iniciales) == 0:
            raise ValueError("La distribución inicial suma 0")
        
        estado = random.choices(estados_lista, weights=pesos_iniciales, k=1)[0]
        estados_seq.append(estado)
        
        # Generar resto de la secuencia
        for i in range(longitud):
            # Emitir observación
            obs_lista = list(self.observaciones)
            obs_probs = [self.emisiones.get((o, estado), 0) for o in obs_lista]
            obs = random.choices(obs_lista, weights=obs_probs, k=1)[0]
            obs_seq.append(obs)

            if i == longitud - 1:
                break # No necesitamos la siguiente transición

            # Transición
            trans_probs = [self.transiciones.get((estado, s_nuevo), 0) 
                           for s_nuevo in estados_lista]
            estado = random.choices(estados_lista, weights=trans_probs, k=1)[0]
            estados_seq.append(estado)
        
        return estados_seq, obs_seq

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 19. Modelo Oculto de Markov (HMM) ===\n")
    
    estados = ['Sano', 'Fiebre']
    observaciones = ['normal', 'frio', 'mareado']
    
    trans_hmm = {
        ('Sano', 'Sano'): 0.7,
        ('Sano', 'Fiebre'): 0.3,
        ('Fiebre', 'Sano'): 0.4,
        ('Fiebre', 'Fiebre'): 0.6
    }
    
    emis_hmm = {
        ('normal', 'Sano'): 0.5,
        ('frio', 'Sano'): 0.4,
        ('mareado', 'Sano'): 0.1,
        ('normal', 'Fiebre'): 0.1,
        ('frio', 'Fiebre'): 0.3,
        ('mareado', 'Fiebre'): 0.6
    }
    
    inicial_hmm = {'Sano': 0.6, 'Fiebre': 0.4}
    
    hmm = HMM(estados, observaciones, trans_hmm, emis_hmm, inicial_hmm)
    
    # Generar secuencia
    seq_estados, seq_obs = hmm.generar_secuencia(5)
    print(f"   Secuencia generada:")
    print(f"      Estados: {seq_estados}")
    print(f"      Observaciones: {seq_obs}")
    
    # Viterbi
    obs_test = ['normal', 'frio', 'mareado']
    estados_inferidos = hmm.viterbi(obs_test)
    print(f"   \n   Observaciones: {obs_test}")
    print(f"   Estados más probables (Viterbi): {estados_inferidos}")
    # (Esperado: ['Sano', 'Sano', 'Fiebre'])