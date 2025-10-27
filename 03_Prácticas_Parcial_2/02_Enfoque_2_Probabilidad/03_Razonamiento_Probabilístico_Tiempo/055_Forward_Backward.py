# ============================================================================
# 18. ALGORITMO HACIA DELANTE-ATRÁS
# ============================================================================

def forward_backward(observaciones, estados, transiciones, emisiones, dist_inicial):
    """
    Algoritmo completo Forward-Backward para HMM
    Args:
        observaciones: secuencia de observaciones
        estados: lista de estados ocultos
        transiciones: P(s'|s) dict {(s, s'): prob}
        emisiones: P(o|s) dict {(obs, estado): prob}
        dist_inicial: P(s_0) dict {estado: prob}
    Returns:
        (alphas, betas, gammas) - probabilidades forward, backward y suavizadas
    """
    T = len(observaciones)
    
    # --- Forward (alpha) ---
    # alpha_t(i) = P(e_{1:t}, X_t = i)
    alphas = []
    
    # t = 0 (usando obs[0])
    alpha = {}
    for s in estados:
        alpha[s] = dist_inicial.get(s, 0) * emisiones.get((observaciones[0], s), 0)
    alphas.append(alpha)
    
    # t = 1 a T-1
    for t in range(1, T):
        alpha_t = {}
        for s_nuevo in estados:
            prob = sum(
                alphas[-1].get(s, 0) * transiciones.get((s, s_nuevo), 0)
                for s in estados
            ) * emisiones.get((observaciones[t], s_nuevo), 0)
            alpha_t[s_nuevo] = prob
        alphas.append(alpha_t)
    
    # --- Backward (beta) ---
    # beta_t(i) = P(e_{t+1:T} | X_t = i)
    betas = [{s: 1.0 for s in estados}] # t = T-1
    
    for t in range(T - 2, -1, -1):
        beta_t = {}
        obs_t_mas_1 = observaciones[t+1]
        beta_t_mas_1 = betas[0] # beta de t+1
        
        for s in estados: # s = X_t
            prob = sum(
                transiciones.get((s, s_nuevo), 0) * # P(X_{t+1}|X_t)
                emisiones.get((obs_t_mas_1, s_nuevo), 0) * # P(e_{t+1}|X_{t+1})
                beta_t_mas_1.get(s_nuevo, 0)              # P(e_{t+2:T}|X_{t+1})
                for s_nuevo in estados # s_nuevo = X_{t+1}
            )
            beta_t[s] = prob
        betas.insert(0, beta_t)
    
    # --- Gamma (suavizado) ---
    # gamma_t(i) = P(X_t = i | e_{1:T})
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
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 18. Algoritmo Forward-Backward ===\n")
    
    # Ejemplo HMM (Paraguas):
    estados = ['Lluvia', 'Sol']
    observaciones_posibles = ['Paraguas', 'Sin_Paraguas']
    
    trans = {
        ('Lluvia', 'Lluvia'): 0.7, ('Lluvia', 'Sol'): 0.3,
        ('Sol', 'Lluvia'): 0.3, ('Sol', 'Sol'): 0.7,
    }
    emis = {
        ('Paraguas', 'Lluvia'): 0.9, ('Paraguas', 'Sol'): 0.2,
        ('Sin_Paraguas', 'Lluvia'): 0.1, ('Sin_Paraguas', 'Sol'): 0.8,
    }
    inicial = {'Lluvia': 0.5, 'Sol': 0.5}
    
    obs_seq = ['Paraguas', 'Paraguas']
    
    alphas, betas, gammas = forward_backward(obs_seq, estados, trans, emis, inicial)
    
    print(f"Observaciones: {obs_seq}\n")
    
    print("--- Alphas (Forward) P(X_t, e_{1:t}) ---")
    for t, alpha in enumerate(alphas):
        print(f"   t={t}: {alpha}")
        
    print("\n--- Betas (Backward) P(e_{t+1:T} | X_t) ---")
    for t, beta in enumerate(betas):
        print(f"   t={t}: {beta}")
        
    print("\n--- Gammas (Suavizado) P(X_t | e_{1:T}) ---")
    for t, gamma in enumerate(gammas):
        print(f"   t={t}: {gamma}")