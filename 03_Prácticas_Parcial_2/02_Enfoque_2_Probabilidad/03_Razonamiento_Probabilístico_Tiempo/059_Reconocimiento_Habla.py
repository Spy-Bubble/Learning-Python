import random

# ============================================================================
# 19. MODELOS OCULTOS DE MARKOV (HMM) - DEPENDENCIA
# ============================================================================
# (Necesario para que reconocimiento_habla_hmm funcione)

class HMM:
    def __init__(self, estados_ocultos, observaciones, transiciones, emisiones, inicial):
        self.estados = estados_ocultos
        self.observaciones = observaciones
        self.transiciones = transiciones
        self.emisiones = emisiones
        self.inicial = inicial
    
    def viterbi(self, secuencia_obs):
        # (Implementación de Viterbi, copiada de 056_HMM.py)
        T = len(secuencia_obs)
        viterbi_prob = [{} for _ in range(T)]
        camino = [{} for _ in range(T)]
        
        if T == 0: return []
        
        obs_0 = secuencia_obs[0]
        for s in self.estados:
            viterbi_prob[0][s] = (self.inicial.get(s, 0) * self.emisiones.get((obs_0, s), 0))
            camino[0][s] = [s]
        
        for t in range(1, T):
            obs_t = secuencia_obs[t]
            for s_nuevo in self.estados:
                max_prob = -1
                mejor_estado = None
                emision_prob = self.emisiones.get((obs_t, s_nuevo), 0)
                
                for s_prev in self.estados:
                    prob = (viterbi_prob[t-1].get(s_prev, 0) * self.transiciones.get((s_prev, s_nuevo), 0))
                    if prob > max_prob:
                        max_prob = prob
                        mejor_estado = s_prev
                
                viterbi_prob[t][s_nuevo] = max_prob * emision_prob
                if mejor_estado and camino[t-1].get(mejor_estado):
                    camino[t][s_nuevo] = camino[t-1][mejor_estado] + [s_nuevo]
                else:
                    camino[t][s_nuevo] = [s_nuevo]
        
        max_prob_final = -1
        mejor_estado_final = None
        for s, prob in viterbi_prob[T-1].items():
            if prob > max_prob_final:
                max_prob_final = prob
                mejor_estado_final = s
        
        if mejor_estado_final is None:
            return []
        return camino[T-1][mejor_estado_final]

# ============================================================================
# 22. RECONOCIMIENTO DEL HABLA
# ============================================================================

def reconocimiento_habla_hmm(audio_features, hmm_palabras):
    """
    Reconocimiento de habla usando HMMs para palabras (conceptual)
    Args:
        audio_features: características extraídas del audio (ej. MFCCs)
        hmm_palabras: dict {palabra: HMM}
    Returns:
        palabra más probable
    """
    mejor_palabra = None
    mejor_prob = float('-inf') # Usar log-probabilidades en la práctica
    
    for palabra, hmm in hmm_palabras.items():
        # Usar Viterbi para encontrar P(audio_features | HMM_palabra)
        try:
            secuencia = hmm.viterbi(audio_features)
            
            # (Simplificado: En la práctica, se calcula la probabilidad
            # del camino de Viterbi, no solo su longitud)
            prob_secuencia = -len(secuencia) # Ejemplo simple
            
            if prob_secuencia > mejor_prob:
                mejor_prob = prob_secuencia
                mejor_palabra = palabra
        except Exception:
            continue
    
    return mejor_palabra


def modelo_lenguaje_bigrama(corpus):
    """
    Crea modelo de lenguaje de bigramas para reconocimiento
    Args:
        corpus: lista de pares de palabras (w_{i-1}, w_i)
    Returns:
        dict {(palabra1, palabra2): probabilidad}
    """
    conteos = {}
    conteos_palabra1 = {}
    
    for w1, w2 in corpus:
        conteos[(w1, w2)] = conteos.get((w1, w2), 0) + 1
        conteos_palabra1[w1] = conteos_palabra1.get(w1, 0) + 1
    
    # Calcular probabilidades
    bigramas = {}
    for (w1, w2), count in conteos.items():
        if conteos_palabra1[w1] > 0:
            bigramas[(w1, w2)] = count / conteos_palabra1[w1]
    
    return bigramas

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 22. Reconocimiento del Habla (Conceptual) ===\n")
    
    # 1. Modelo de Lenguaje (Bigramas)
    print("Modelo de Lenguaje (Bigramas):")
    corpus = [
        ('<s>', 'hola'), ('hola', 'mundo'), ('mundo', '</s>'),
        ('<s>', 'hola'), ('hola', 'IA'), ('IA', '</s>')
    ]
    bigramas = modelo_lenguaje_bigrama(corpus)
    print(f"   Corpus: {corpus}")
    print(f"   P(mundo | hola) = {bigramas.get(('hola', 'mundo'), 0):.2f}")
    print(f"   P(IA | hola) = {bigramas.get(('hola', 'IA'), 0):.2f}\n")
    
    # 2. Reconocimiento HMM (Conceptual)
    print("Reconocimiento HMM (Conceptual):")
    # Features de audio (simulados como fonemas)
    audio_features = ['H', 'O', 'L', 'A']
    
    # HMM para "hola" (simplificado)
    hmm_hola = HMM(
        estados_ocultos=['sH', 'sO', 'sL', 'sA'],
        observaciones=['H', 'O', 'L', 'A'],
        transiciones={('sH','sO'): 1.0, ('sO','sL'): 1.0, ('sL','sA'): 1.0},
        emisiones={('H','sH'): 0.9, ('O','sO'): 0.9, ('L','sL'): 0.9, ('A','sA'): 0.9},
        inicial={'sH': 1.0}
    )
    
    # HMM para "adios"
    hmm_adios = HMM(
        estados_ocultos=['sA', 'sD', 'sI', 'sO', 'sS'],
        observaciones=['A', 'D', 'I', 'O', 'S'],
        transiciones={('sA','sD'): 1.0, ('sD','sI'): 1.0, ('sI','sO'): 1.0, ('sO','sS'): 1.0},
        emisiones={('A','sA'): 0.9, ('D','sD'): 0.9, ('I','sI'): 0.9, ('O','sO'): 0.9, ('S','sS'): 0.9},
        inicial={'sA': 1.0}
    )
    
    hmm_palabras = {'hola': hmm_hola, 'adios': hmm_adios}
    
    palabra_reconocida = reconocimiento_habla_hmm(audio_features, hmm_palabras)
    print(f"   Features de audio: {audio_features}")
    print(f"   Palabra reconocida: {palabra_reconocida}")