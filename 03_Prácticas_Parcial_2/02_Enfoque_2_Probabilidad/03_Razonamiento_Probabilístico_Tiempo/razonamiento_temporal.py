"""
RAZONAMIENTO PROBABILÍSTICO EN EL TIEMPO
Algoritmos 15-22: Procesos estocásticos, HMM, Kalman, etc.
"""

import random
import math
import numpy as np

# ============================================================================
# 15. PROCESOS ESTACIONARIOS
# ============================================================================

def es_proceso_estacionario(transiciones):
    """
    Verifica si un proceso tiene probabilidades de transición constantes
    Args:
        transiciones: dict {tiempo: {(estado, estado'): prob}}
    Returns:
        True si es estacionario
    """
    # Verificar que las transiciones no cambien con el tiempo
    tiempos = list(transiciones.keys())
    if len(tiempos) < 2:
        return True
    
    referencia = transiciones[tiempos[0]]
    
    for t in tiempos[1:]:
        if transiciones[t] != referencia:
            return False
    
    return True


def distribucion_estacionaria(matriz_transicion, epsilon=0.001, max_iter=1000):
    """
    Encuentra la distribución estacionaria de una cadena de Markov
    Args:
        matriz_transicion: dict {(estado_i, estado_j): probabilidad}
        epsilon: tolerancia de convergencia
        max_iter: iteraciones máximas
    Returns:
        distribución estacionaria
    """
    # Obtener estados únicos
    estados = set()
    for (s1, s2) in matriz_transicion.keys():
        estados.add(s1)
        estados.add(s2)
    estados = sorted(list(estados))
    
    # Inicializar distribución uniforme
    n = len(estados)
    dist = {s: 1.0/n for s in estados}
    
    for _ in range(max_iter):
        nueva_dist = {}
        
        # Aplicar transición: π' = π · P
        for s_j in estados:
            nueva_dist[s_j] = sum(
                dist[s_i] * matriz_transicion.get((s_i, s_j), 0)
                for s_i in estados
            )
        
        # Verificar convergencia
        cambio = sum(abs(nueva_dist[s] - dist[s]) for s in estados)
        dist = nueva_dist
        
        if cambio < epsilon:
            break
    
    return dist


# ============================================================================
# 16. HIPÓTESIS DE MARKOV: PROCESOS DE MARKOV
# ============================================================================

class ProcesoMarkov:
    """
    Proceso de Markov de primer orden
    """
    def __init__(self, estados, transiciones, dist_inicial):
        """
        Args:
            estados: lista de estados posibles
            transiciones: dict {(s, s'): P(s'|s)}
            dist_inicial: dict {estado: probabilidad}
        """
        self.estados = estados
        self.transiciones = transiciones
        self.dist_actual = dist_inicial
    
    def avanzar(self):
        """Avanza un paso de tiempo"""
        nueva_dist = {}
        
        for s_nuevo in self.estados:
            prob = sum(
                self.dist_actual.get(s, 0) * self.transiciones.get((s, s_nuevo), 0)
                for s in self.estados
            )
            nueva_dist[s_nuevo] = prob
        
        self.dist_actual = nueva_dist
        return nueva_dist
    
    def predecir(self, pasos):
        """Predice distribución después de n pasos"""
        for _ in range(pasos):
            self.avanzar()
        return self.dist_actual


def verificar_propiedad_markov(secuencia, transiciones):
    """
    Verifica si una secuencia cumple la propiedad de Markov
    P(X_t|X_0,...,X_{t-1}) = P(X_t|X_{t-1})
    Args:
        secuencia: lista de estados observados
        transiciones: probabilidades de transición
    Returns:
        True si satisface la propiedad
    """
    # En práctica, esto se verificaría con tests estadísticos
    # Aquí verificamos que las transiciones sean consistentes
    
    for i in range(1, len(secuencia)):
        estado_prev = secuencia[i-1]
        estado_actual = secuencia[i]
        
        # Verificar que la transición exista
        if (estado_prev, estado_actual) not in transiciones:
            return False
    
    return True


# ============================================================================
# 17. FILTRADO, PREDICCIÓN, SUAVIZADO Y EXPLICACIÓN
# ============================================================================

def filtrado(observaciones, transiciones, sensor, dist_inicial):
    """
    Filtrado (forward): calcula P(X_t|e_{1:t})
    Args:
        observaciones: lista de observaciones
        transiciones: P(X_t|X_{t-1})
        sensor: P(e_t|X_t) - modelo de sensor
        dist_inicial: P(X_0)
    Returns:
        lista de distribuciones filtradas
    """
    estados = list(dist_inicial.keys())
    distribuciones = [dist_inicial]
    
    for obs in observaciones:
        # Predicción
        prediccion = {}
        for s_nuevo in estados:
            prob = sum(
                distribuciones[-1].get(s, 0) * transiciones.get((s, s_nuevo), 0)
                for s in estados
            )
            prediccion[s_nuevo] = prob
        
        # Actualización con observación
        actualizacion = {}
        for s in estados:
            actualizacion[s] = sensor.get((obs, s), 0) * prediccion[s]
        
        # Normalizar
        total = sum(actualizacion.values())
        if total > 0:
            actualizacion = {k: v/total for k, v in actualizacion.items()}
        
        distribuciones.append(actualizacion)
    
    return distribuciones


def prediccion(dist_actual, transiciones, pasos):
    """
    Predicción: calcula P(X_{t+k}|e_{1:t})
    Args:
        dist_actual: distribución actual
        transiciones: matriz de transición
        pasos: pasos hacia adelante
    Returns:
        distribución predicha
    """
    estados = list(dist_actual.keys())
    dist = dict(dist_actual)
    
    for _ in range(pasos):
        nueva_dist = {}
        for s_nuevo in estados:
            prob = sum(
                dist.get(s, 0) * transiciones.get((s, s_nuevo), 0)
                for s in estados
            )
            nueva_dist[s_nuevo] = prob
        dist = nueva_dist
    
    return dist


def suavizado(observaciones, transiciones, sensor, dist_inicial):
    """
    Suavizado (forward-backward): calcula P(X_k|e_{1:t}) para k < t
    Args:
        observaciones: todas las observaciones
        transiciones: P(X_t|X_{t-1})
        sensor: P(e_t|X_t)
        dist_inicial: P(X_0)
    Returns:
        distribuciones suavizadas
    """
    # Forward pass
    forward = filtrado(observaciones, transiciones, sensor, dist_inicial)
    
    # Backward pass (simplificado)
    estados = list(dist_inicial.keys())
    backward = [{s: 1.0 for s in estados}]  # Mensaje hacia atrás inicial
    
    for i in range(len(observaciones) - 1, 0, -1):
        mensaje = {}
        for s in estados:
            prob = sum(
                transiciones.get((s, s_nuevo), 0) *
                sensor.get((observaciones[i], s_nuevo), 0) *
                backward[0].get(s_nuevo, 0)
                for s_nuevo in estados
            )
            mensaje[s] = prob
        backward.insert(0, mensaje)
    
    # Combinar forward y backward
    suavizadas = []
    for i in range(len(forward)):
        combinada = {}
        for s in estados:
            combinada[s] = forward[i].get(s, 0) * backward[i].get(s, 1.0)
        
        # Normalizar
        total = sum(combinada.values())
        if total > 0:
            combinada = {k: v/total for k, v in combinada.items()}
        suavizadas.append(combinada)
    
    return suavizadas


# ============================================================================
# 18. ALGORITMO HACIA DELANTE-ATRÁS
# ============================================================================

def forward_backward(observaciones, estados, transiciones, emisiones, dist_inicial):
    """
    Algoritmo completo Forward-Backward para HMM
    Args:
        observaciones: secuencia de observaciones
        estados: lista de estados ocultos
        transiciones: P(s'|s)
        emisiones: P(o|s)
        dist_inicial: P(s_0)
    Returns:
        (alphas, betas, gammas) - probabilidades forward, backward y suavizadas
    """
    T = len(observaciones)
    n_estados = len(estados)
    
    # Forward (alpha)
    alphas = []
    alpha = {s: dist_inicial.get(s, 0) * emisiones.get((observaciones[0], s), 0) 
             for s in estados}
    # Normalizar
    suma = sum(alpha.values())
    if suma > 0:
        alpha = {k: v/suma for k, v in alpha.items()}
    alphas.append(alpha)
    
    for t in range(1, T):
        alpha = {}
        for s_nuevo in estados:
            prob = sum(
                alphas[-1].get(s, 0) * transiciones.get((s, s_nuevo), 0)
                for s in estados
            ) * emisiones.get((observaciones[t], s_nuevo), 0)
            alpha[s_nuevo] = prob
        
        # Normalizar
        suma = sum(alpha.values())
        if suma > 0:
            alpha = {k: v/suma for k, v in alpha.items()}
        alphas.append(alpha)
    
    # Backward (beta)
    betas = [{s: 1.0 for s in estados}]
    
    for t in range(T-2, -1, -1):
        beta = {}
        for s in estados:
            prob = sum(
                transiciones.get((s, s_nuevo), 0) *
                emisiones.get((observaciones[t+1], s_nuevo), 0) *
                betas[0].get(s_nuevo, 0)
                for s_nuevo in estados
            )
            beta[s] = prob
        betas.insert(0, beta)
    
    # Gamma (suavizado)
    gammas = []
    for t in range(T):
        gamma = {}
        for s in estados:
            gamma[s] = alphas[t].get(s, 0) * betas[t].get(s, 0)
        
        # Normalizar
        suma = sum(gamma.values())
        if suma > 0:
            gamma = {k: v/suma for k, v in gamma.items()}
        gammas.append(gamma)
    
    return alphas, betas, gammas


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
            transiciones: P(s'|s)
            emisiones: P(o|s)
            inicial: P(s_0)
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
        for s in self.estados:
            viterbi_prob[0][s] = (self.inicial.get(s, 0) * 
                                 self.emisiones.get((secuencia_obs[0], s), 0))
            camino[0][s] = [s]
        
        # t > 0
        for t in range(1, T):
            for s_nuevo in self.estados:
                # Encontrar estado previo con máxima probabilidad
                max_prob = 0
                mejor_estado = None
                
                for s in self.estados:
                    prob = (viterbi_prob[t-1].get(s, 0) * 
                           self.transiciones.get((s, s_nuevo), 0) *
                           self.emisiones.get((secuencia_obs[t], s_nuevo), 0))
                    
                    if prob > max_prob:
                        max_prob = prob
                        mejor_estado = s
                
                viterbi_prob[t][s_nuevo] = max_prob
                if mejor_estado:
                    camino[t][s_nuevo] = camino[t-1][mejor_estado] + [s_nuevo]
        
        # Encontrar el mejor camino final
        max_prob_final = max(viterbi_prob[T-1].values())
        mejor_estado_final = [s for s in self.estados 
                             if viterbi_prob[T-1][s] == max_prob_final][0]
        
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
        estado = random.choices(self.estados, 
                               weights=[self.inicial.get(s, 0) for s in self.estados])[0]
        estados_seq.append(estado)
        
        # Emitir observación
        obs_probs = [self.emisiones.get((o, estado), 0) for o in self.observaciones]
        obs = random.choices(self.observaciones, weights=obs_probs)[0]
        obs_seq.append(obs)
        
        # Generar resto de la secuencia
        for _ in range(longitud - 1):
            # Transición
            trans_probs = [self.transiciones.get((estado, s_nuevo), 0) 
                          for s_nuevo in self.estados]
            estado = random.choices(self.estados, weights=trans_probs)[0]
            estados_seq.append(estado)
            
            # Emisión
            obs_probs = [self.emisiones.get((o, estado), 0) for o in self.observaciones]
            obs = random.choices(self.observaciones, weights=obs_probs)[0]
            obs_seq.append(obs)
        
        return estados_seq, obs_seq


# ============================================================================
# 20. FILTROS DE KALMAN
# ============================================================================

class FiltroKalman:
    """
    Filtro de Kalman para sistemas lineales con ruido gaussiano
    """
    def __init__(self, F, H, Q, R, x0, P0):
        """
        Args:
            F: matriz de transición de estado
            H: matriz de observación
            Q: covarianza del ruido del proceso
            R: covarianza del ruido de medición
            x0: estado inicial
            P0: covarianza inicial
        """
        self.F = np.array(F)  # Transición
        self.H = np.array(H)  # Observación
        self.Q = np.array(Q)  # Ruido proceso
        self.R = np.array(R)  # Ruido medición
        self.x = np.array(x0)  # Estado
        self.P = np.array(P0)  # Covarianza
    
    def predecir(self):
        """Paso de predicción"""
        # x = F * x
        self.x = self.F @ self.x
        # P = F * P * F' + Q
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.x, self.P
    
    def actualizar(self, z):
        """
        Paso de actualización con medición
        Args:
            z: vector de medición
        """
        z = np.array(z)
        
        # Innovación
        y = z - self.H @ self.x
        
        # Covarianza de la innovación
        S = self.H @ self.P @ self.H.T + self.R
        
        # Ganancia de Kalman
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualizar estado
        self.x = self.x + K @ y
        
        # Actualizar covarianza
        I = np.eye(len(self.x))
        self.P = (I - K @ self.H) @ self.P
        
        return self.x, self.P


# ============================================================================
# 21. RED BAYESIANA DINÁMICA: FILTRADO DE PARTÍCULAS
# ============================================================================

def filtrado_particulas(observaciones, transicion_func, sensor_func, num_particulas=1000):
    """
    Filtrado de partículas (Sequential Monte Carlo)
    Args:
        observaciones: lista de observaciones
        transicion_func: función que muestrea nuevo estado dado estado previo
        sensor_func: función que da P(obs|estado)
        num_particulas: número de partículas
    Returns:
        lista de conjuntos de partículas filtradas
    """
    # Inicializar partículas (distribución uniforme o a priori)
    particulas = [{'estado': random.random() * 10, 'peso': 1.0/num_particulas} 
                  for _ in range(num_particulas)]
    
    historia_particulas = [particulas]
    
    for obs in observaciones:
        # 1. Predicción: mover partículas según modelo de transición
        for p in particulas:
            p['estado'] = transicion_func(p['estado'])
        
        # 2. Actualización: ponderar por verosimilitud de observación
        for p in particulas:
            p['peso'] *= sensor_func(obs, p['estado'])
        
        # 3. Normalizar pesos
        suma_pesos = sum(p['peso'] for p in particulas)
        if suma_pesos > 0:
            for p in particulas:
                p['peso'] /= suma_pesos
        
        # 4. Re-muestreo (si es necesario)
        # Calcular tamaño efectivo de muestra
        n_eff = 1.0 / sum(p['peso']**2 for p in particulas)
        
        if n_eff < num_particulas / 2:
            # Re-muestrear
            estados = [p['estado'] for p in particulas]
            pesos = [p['peso'] for p in particulas]
            nuevos_estados = random.choices(estados, weights=pesos, k=num_particulas)
            particulas = [{'estado': e, 'peso': 1.0/num_particulas} 
                         for e in nuevos_estados]
        
        historia_particulas.append([dict(p) for p in particulas])
    
    return historia_particulas


# ============================================================================
# 22. RECONOCIMIENTO DEL HABLA
# ============================================================================

def reconocimiento_habla_hmm(audio_features, hmm_palabras):
    """
    Reconocimiento de habla usando HMMs para palabras
    Args:
        audio_features: características extraídas del audio
        hmm_palabras: dict {palabra: HMM}
    Returns:
        palabra más probable
    """
    mejor_palabra = None
    mejor_prob = float('-inf')
    
    for palabra, hmm in hmm_palabras.items():
        # Usar Viterbi para encontrar probabilidad
        try:
            secuencia = hmm.viterbi(audio_features)
            # Calcular log-probabilidad (simplificado)
            prob = len(secuencia)  # En práctica, calcular prob real
            
            if prob > mejor_prob:
                mejor_prob = prob
                mejor_palabra = palabra
        except:
            continue
    
    return mejor_palabra


def modelo_lenguaje_bigrama(corpus):
    """
    Crea modelo de lenguaje de bigramas para reconocimiento
    Args:
        corpus: lista de pares de palabras
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
        bigramas[(w1, w2)] = count / conteos_palabra1[w1]
    
    return bigramas


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== RAZONAMIENTO PROBABILÍSTICO EN EL TIEMPO ===\n")
    
    # Ejemplo 15: Procesos estacionarios
    print("15. Distribución Estacionaria:")
    transiciones = {
        ('sol', 'sol'): 0.8,
        ('sol', 'lluvia'): 0.2,
        ('lluvia', 'sol'): 0.4,
        ('lluvia', 'lluvia'): 0.6
    }
    dist_est = distribucion_estacionaria(transiciones)
    print(f"   Distribución estacionaria del clima:")
    for estado, prob in dist_est.items():
        print(f"      {estado}: {prob:.3f}")
    print()
    
    # Ejemplo 19: HMM
    print("19. Modelo Oculto de Markov:")
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
    print(f"      Estados: {seq_estados}")
    print(f"      Observaciones: {seq_obs}")
    
    # Viterbi
    obs_test = ['normal', 'frio', 'mareado']
    estados_inferidos = hmm.viterbi(obs_test)
    print(f"   \n   Observaciones: {obs_test}")
    print(f"   Estados más probables (Viterbi): {estados_inferidos}")
    print()
    
    # Ejemplo 20: Filtro de Kalman
    print("20. Filtro de Kalman:")
    # Sistema simple: posición con velocidad constante
    # Estado: [posición, velocidad]
    # Observación: solo posición
    
    F = [[1, 1], [0, 1]]  # Matriz de transición
    H = [[1, 0]]  # Matriz de observación (solo vemos posición)
    Q = [[0.1, 0], [0, 0.1]]  # Ruido del proceso
    R = [[1.0]]  # Ruido de medición
    x0 = [0, 1]  # Estado inicial: pos=0, vel=1
    P0 = [[1, 0], [0, 1]]  # Covarianza inicial
    
    kf = FiltroKalman(F, H, Q, R, x0, P0)
    
    # Simular mediciones
    mediciones = [1.1, 2.05, 2.9, 4.1, 5.2]
    
    print(f"   Estado inicial: {x0}")
    for i, z in enumerate(mediciones):
        kf.predecir()
        estado, _ = kf.actualizar([z])
        print(f"   Tiempo {i+1}: medición={z:.2f}, estimado={estado[0]:.2f}, velocidad={estado[1]:.2f}")
    print()
    
    # Ejemplo 21: Filtrado de partículas
    print("21. Filtrado de Partículas:")
    
    def transicion_simple(x):
        """Modelo de transición: x_t = x_{t-1} + ruido"""
        return x + random.gauss(0, 0.5)
    
    def sensor_simple(obs, estado):
        """Modelo de sensor: observación = estado + ruido"""
        # Verosimilitud gaussiana
        diff = obs - estado
        return math.exp(-0.5 * diff**2)
    
    obs_particulas = [5.1, 5.3, 5.2, 5.4, 5.6]
    particulas_hist = filtrado_particulas(obs_particulas, transicion_simple, 
                                          sensor_simple, num_particulas=100)
    
    print(f"   Observaciones: {obs_particulas}")
    print(f"   Estimaciones (media de partículas):")
    for i, particulas in enumerate(particulas_hist):
        media = sum(p['estado'] * p['peso'] for p in particulas) / sum(p['peso'] for p in particulas)
        print(f"      Tiempo {i}: {media:.2f}")