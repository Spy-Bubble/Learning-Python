# ============================================================================
# 17. FILTRADO, PREDICCIÓN, SUAVIZADO Y EXPLICACIÓN
# ============================================================================

def filtrado(observaciones, transiciones, sensor, dist_inicial):
    """
    Filtrado (forward): calcula P(X_t|e_{1:t})
    Args:
        observaciones: lista de observaciones [e_1, e_2, ...]
        transiciones: P(X_t|X_{t-1}) dict {(s_prev, s_act): prob}
        sensor: P(e_t|X_t) - modelo de sensor dict {(obs, estado): prob}
        dist_inicial: P(X_0)
    Returns:
        lista de distribuciones filtradas [P(X_0|e_0), P(X_1|e_1), ...]
        (Nota: el original parece alinear obs[0] con t=1)
    """
    estados = list(dist_inicial.keys())
    distribuciones = []
    
    # t = 0 (usando dist_inicial)
    dist_t = dist_inicial
    distribuciones.append(dist_t) # P(X_0)
    
    for obs in observaciones:
        # 1. Predicción P(X_{t} | e_{1:t-1})
        prediccion = {}
        for s_nuevo in estados:
            prob = sum(
                dist_t.get(s, 0) * transiciones.get((s, s_nuevo), 0)
                for s in estados
            )
            prediccion[s_nuevo] = prob
        
        # 2. Actualización con observación P(X_t | e_{1:t})
        actualizacion = {}
        for s in estados:
            # P(e_t | X_t) * P(X_t | e_{1:t-1})
            actualizacion[s] = sensor.get((obs, s), 0) * prediccion[s]
        
        # 3. Normalizar
        total = sum(actualizacion.values())
        if total > 0:
            dist_t = {k: v/total for k, v in actualizacion.items()}
        else:
            dist_t = {k: 0 for k in actualizacion} # Evidencia imposible
        
        distribuciones.append(dist_t)
    
    return distribuciones # Retorna [P(X_0), P(X_1|e_1), ..., P(X_t|e_1:t)]


def prediccion(dist_actual, transiciones, pasos):
    """
    Predicción: calcula P(X_{t+k}|e_{1:t})
    Args:
        dist_actual: P(X_t | e_{1:t})
        transiciones: matriz de transición
        pasos: k (pasos hacia adelante)
    Returns:
        distribución predicha P(X_{t+k})
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
        observaciones: todas las observaciones [e_1, ..., e_t]
        transiciones: P(X_t|X_{t-1})
        sensor: P(e_t|X_t)
        dist_inicial: P(X_0)
    Returns:
        distribuciones suavizadas
    """
    estados = list(dist_inicial.keys())
    T = len(observaciones)

    # 1. Forward pass (filtrado)
    # alphas = [P(X_0), P(X_1|e_1), ..., P(X_t|e_1:t)]
    alphas = filtrado(observaciones, transiciones, sensor, dist_inicial)
    
    # 2. Backward pass
    # b_k = P(e_{k+1:t} | X_k)
    betas = [{s: 1.0 for s in estados}] # b_t = 1
    
    for t in range(T - 1, -1, -1):
        obs_t_mas_1 = observaciones[t]
        mensaje_b_t_mas_1 = betas[0] # P(e_{t+2:T} | X_{t+1})
        
        mensaje_b_t = {}
        for s in estados: # s = X_t
            prob = sum(
                transiciones.get((s, s_nuevo), 0) * # P(X_{t+1}|X_t)
                sensor.get((obs_t_mas_1, s_nuevo), 0) * # P(e_{t+1}|X_{t+1})
                mensaje_b_t_mas_1.get(s_nuevo, 0)           # P(e_{t+2:T} | X_{t+1})
                for s_nuevo in estados # s_nuevo = X_{t+1}
            )
            mensaje_b_t[s] = prob
        
        # (Opcional: Normalizar betas para evitar underflow)
        total_b = sum(mensaje_b_t.values())
        if total_b > 0:
            mensaje_b_t = {k: v/total_b for k, v in mensaje_b_t.items()}
            
        betas.insert(0, mensaje_b_t)
    
    # 3. Combinar forward y backward
    # P(X_k | e_{1:t}) ∝ P(X_k | e_{1:k}) * P(e_{k+1:t} | X_k)
    # P(X_k | e_{1:t}) ∝ alpha[k] * beta[k+1]
    
    # (El índice de alphas está desplazado por P(X_0))
    suavizadas = []
    for k in range(T + 1):
        combinada = {}
        for s in estados:
            combinada[s] = alphas[k].get(s, 0) * betas[k].get(s, 1.0)
        
        # Normalizar
        total = sum(combinada.values())
        if total > 0:
            combinada = {k: v/total for k, v in combinada.items()}
        suavizadas.append(combinada)
    
    return suavizadas

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 17. Filtrado, Predicción y Suavizado ===\n")
    
    # Ejemplo HMM (Paraguas):
    estados = ['Lluvia', 'Sol']
    observaciones = ['Paraguas', 'Sin_Paraguas']
    
    trans = {
        ('Lluvia', 'Lluvia'): 0.7, ('Lluvia', 'Sol'): 0.3,
        ('Sol', 'Lluvia'): 0.3, ('Sol', 'Sol'): 0.7,
    }
    sensor = {
        ('Paraguas', 'Lluvia'): 0.9, ('Paraguas', 'Sol'): 0.2,
        ('Sin_Paraguas', 'Lluvia'): 0.1, ('Sin_Paraguas', 'Sol'): 0.8,
    }
    inicial = {'Lluvia': 0.5, 'Sol': 0.5}
    
    obs_seq = ['Paraguas', 'Paraguas']
    
    # 1. Filtrado
    print("Filtrado P(X_t | e_{1:t}):")
    dist_filtradas = filtrado(obs_seq, trans, sensor, inicial)
    # dist_filtradas[0] = P(X_0)
    # dist_filtradas[1] = P(X_1 | e_1='Paraguas')
    # dist_filtradas[2] = P(X_2 | e_1='Paraguas', e_2='Paraguas')
    print(f"   P(X_0): {dist_filtradas[0]}")
    print(f"   P(X_1 | 'Paraguas'): {dist_filtradas[1]}")
    print(f"   P(X_2 | 'Paraguas', 'Paraguas'): {dist_filtradas[2]}\n")

    # 2. Predicción
    print("Predicción P(X_{t+k} | e_{1:t}):")
    # Predecir P(X_3) basado en P(X_2 | e_1:2)
    dist_predicha = prediccion(dist_filtradas[2], trans, pasos=1)
    print(f"   P(X_3 | e_1:2): {dist_predicha}\n")
    
    # 3. Suavizado
    print("Suavizado P(X_k | e_{1:t}):")
    dist_suavizadas = suavizado(obs_seq, trans, sensor, inicial)
    # dist_suavizadas[0] = P(X_0 | e_1:2)
    # dist_suavizadas[1] = P(X_1 | e_1:2)
    # dist_suavizadas[2] = P(X_2 | e_1:2)
    print(f"   P(X_0 | 'Paraguas', 'Paraguas'): {dist_suavizadas[0]}")
    print(f"   P(X_1 | 'Paraguas', 'Paraguas'): {dist_suavizadas[1]}")
    print(f"   P(X_2 | 'Paraguas', 'Paraguas'): {dist_suavizadas[2]}")