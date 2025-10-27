import math # Although not directly used, useful for probability calculations

# ============================================================================
# 23. APRENDIZAJE BAYESIANO
# ============================================================================

def aprendizaje_bayesiano(datos, hipotesis, prior, verosimilitud_func):
    """
    Aprendizaje bayesiano: actualiza creencias sobre hipótesis
    Args:
        datos: datos observados
        hipotesis: lista de hipótesis posibles
        prior: dict {hipótesis: P(h)}
        verosimilitud_func: función que calcula P(datos|h)
    Returns:
        posterior: dict {hipótesis: P(h|datos)}
    """
    posterior = {}
    
    # Calcular P(datos|h) * P(h) para cada hipótesis (numerador de Bayes)
    for h in hipotesis:
        verosimilitud = verosimilitud_func(datos, h)
        posterior[h] = verosimilitud * prior[h]
    
    # Normalizar (dividir por P(datos))
    total = sum(posterior.values()) # P(datos) = Suma_h [ P(datos|h) * P(h) ]
    if total > 0:
        posterior = {h: p/total for h, p in posterior.items()}
   
    return posterior


def map_hypothesis(posterior):
    """
    Encuentra hipótesis MAP (Maximum A Posteriori)
    Args:
        posterior: distribución posterior
    Returns:
        hipótesis con máxima probabilidad posterior
    """
    if not posterior:
        return None
    return max(posterior.items(), key=lambda x: x[1])[0]

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 23. Aprendizaje Bayesiano ===\n")

    # Ejemplo: Moneda sesgada
    # Datos: Observar 3 caras (C) en 5 lanzamientos (N=5)
    datos_moneda = {'N': 5, 'C': 3}
    
    # Hipótesis: Diferentes sesgos (p=probabilidad de cara)
    hipotesis_moneda = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    # Prior: Todas las hipótesis son igualmente probables
    prior_moneda = {h: 1.0/len(hipotesis_moneda) for h in hipotesis_moneda}
    
    # Verosimilitud: Binomial P(datos|h) = P(k caras | N, p=h)
    from math import comb
    def verosimilitud_binomial(datos, h):
        n = datos['N']
        k = datos['C']
        p = h
        if not (0 <= p <= 1): return 0
        if k < 0 or k > n: return 0
        return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

    # Aprender
    posterior_moneda = aprendizaje_bayesiano(datos_moneda, hipotesis_moneda, 
                                            prior_moneda, verosimilitud_binomial)
    
    print(f"   Datos: {datos_moneda['C']} caras en {datos_moneda['N']} lanzamientos")
    print(f"   Prior: {prior_moneda}")
    print(f"   Posterior:")
    for h, p in posterior_moneda.items():
        print(f"      P(h={h}|datos) = {p:.3f}")

    # Encontrar MAP
    map_h = map_hypothesis(posterior_moneda)
    print(f"\n   Hipótesis MAP (Maximum A Posteriori): {map_h}")