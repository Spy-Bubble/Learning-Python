from collections import defaultdict

# ============================================================================
# 33. APRENDIZAJE POR REFUERZO PASIVO
# ============================================================================

def aprendizaje_td_pasivo(episodios, politica, alpha=0.1, gamma=0.9):
    """
    Temporal Difference Learning pasivo (sigue política fija)
    Args:
        episodios: lista de episodios [(s, a, r, s'), ...]
        politica: política fija a seguir {estado: accion}
        alpha: tasa de aprendizaje
        gamma: factor de descuento
    Returns:
        valores estimados de estados
    """
    V = defaultdict(float)  # Valores de estados
    
    for episodio in episodios:
        for (s, a, r, s_siguiente) in episodio:
            # Asegurarse de que el estado siguiente tenga un valor (incluso si es 0)
            _ = V[s_siguiente] 
            
            # Actualización TD(0)
            V[s] = V[s] + alpha * (r + gamma * V[s_siguiente] - V[s])
    
    return dict(V)


def montecarlo_pasivo(episodios, politica, gamma=0.9):
    """
    Aprendizaje Monte Carlo pasivo
    Args:
        episodios: lista de episodios completos
        politica: política fija
        gamma: factor de descuento
    Returns:
        valores estimados
    """
    retornos = defaultdict(list)  # Retornos observados por estado
    
    for episodio in episodios:
        G = 0  # Retorno acumulado
        
        # Recorrer episodio en reversa
        for s, a, r, _ in reversed(episodio):
            G = r + gamma * G
            retornos[s].append(G)
    
    # Promediar retornos
    V = {s: sum(returns)/len(returns) for s, returns in retornos.items()}
    return V

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 33. Aprendizaje por Refuerzo Pasivo ===\n")
    
    # Episodios de ejemplo (s, a, r, s_siguiente)
    episodios = [
        [('s1', 'ir', 0, 's2'), ('s2', 'ir', 0, 's3'), ('s3', 'ir', 10, 'meta')],
        [('s1', 'ir', 0, 's2'), ('s2', 'ir', -1, 's1'), ('s1', 'ir', 0, 's2'), ('s2', 'ir', 0, 's3'), ('s3', 'ir', 10, 'meta')],
        [('s1', 'ir', 0, 's2'), ('s2', 'ir', 0, 's3'), ('s3', 'ir', 0, 's3'), ('s3', 'ir', 10, 'meta')]
    ]
    
    # Política fija (no se usa en este cálculo, pero es parte de la definición)
    politica = {'s1': 'ir', 's2': 'ir', 's3': 'ir'}

    print("Resultados de TD Pasivo:")
    valores_td = aprendizaje_td_pasivo(episodios, politica, alpha=0.1, gamma=0.9)
    for s, v in valores_td.items():
        print(f"   V({s}): {v:.2f}")

    print("\nResultados de Monte Carlo Pasivo:")
    valores_mc = montecarlo_pasivo(episodios, politica, gamma=0.9)
    for s, v in valores_mc.items():
        print(f"   V({s}): {v:.2f}")