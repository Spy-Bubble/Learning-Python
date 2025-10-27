# ============================================================================
# 6. REGLA DE BAYES
# ============================================================================

def regla_bayes(p_b_dado_a, p_a, p_b):
    """
    Calcula P(A|B) usando: P(A|B) = P(B|A)·P(A) / P(B)
    Args:
        p_b_dado_a: P(B|A) - verosimilitud
        p_a: P(A) - probabilidad a priori
        p_b: P(B) - evidencia
    Returns:
        P(A|B) - probabilidad a posteriori
    """
    if p_b == 0:
        raise ValueError("P(B) (evidencia) no puede ser 0")
    
    return (p_b_dado_a * p_a) / p_b


def regla_bayes_multiple(p_b_dado_ai, p_ai):
    """
    Regla de Bayes con múltiples hipótesis (lista)
    Args:
        p_b_dado_ai: lista de P(B|Ai) para cada hipótesis
        p_ai: lista de P(Ai) para cada hipótesis
    Returns:
        lista de P(Ai|B) - posteriores normalizadas
    """
    if len(p_b_dado_ai) != len(p_ai):
        raise ValueError("Listas de verosimilitud y prioris deben ser iguales")
        
    # Calcular numeradores P(B|Ai) * P(Ai)
    numeradores = [p_b_dado_ai[i] * p_ai[i] for i in range(len(p_ai))]
    
    # Calcular P(B) = suma de todos los numeradores (Evidencia)
    p_b = sum(numeradores)
    
    if p_b == 0:
        return [0] * len(p_ai) # Evidencia imposible
    
    # Calcular posteriores P(Ai|B) = Numerador / P(B)
    posteriores = [num / p_b for num in numeradores]
    
    return posteriores


def actualizar_creencia_bayes(prior, verosimilitud, evidencia):
    """
    Actualización bayesiana de creencias (usando diccionarios)
    Args:
        prior: dict {hipótesis: probabilidad_previa}
        verosimilitud: dict {hipótesis: P(evidencia|hipótesis)}
        evidencia: (Opcional, solo para claridad)
    Returns:
        dict {hipótesis: probabilidad_posterior}
    """
    # Calcular numeradores
    numeradores = {}
    for hipotesis in prior.keys():
        numeradores[hipotesis] = prior[hipotesis] * verosimilitud.get(hipotesis, 0)
    
    # Normalizar (Calcular P(evidencia))
    total = sum(numeradores.values())
    
    if total == 0:
        # Evidencia imposible, retornar prior (o error)
        return prior 
    
    posterior = {h: num/total for h, num in numeradores.items()}
    
    return posterior

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 6. Regla de Bayes ===\n")
    
    # Ejemplo 1: Test médico
    print("Test Médico (Regla de Bayes simple):")
    # P(A|B) = P(B|A)·P(A) / P(B)
    # A = Enfermo, B = Test Positivo
    
    p_b_dado_a = 0.95  # P(Positivo | Enfermo) - Sensibilidad
    p_a = 0.01         # P(Enfermo) - Prevalencia (Prior)
    p_b = 0.05         # P(Positivo) - Evidencia (calculada)
    
    p_enfermo_dado_positivo = regla_bayes(p_b_dado_a, p_a, p_b)
    print(f"   P(Enfermo|Test positivo) = {p_enfermo_dado_positivo:.3f}")
    print(f"   Interpretación: Solo 19% de probabilidad real de estar enfermo\n")
    
    # Ejemplo 2: Múltiples hipótesis (actualización con dict)
    print("Actualización Bayesiana (Múltiples hipótesis):")
    
    # Hipótesis: ¿Qué tipo de dado es?
    prior = {'Dado Justo': 0.5, 'Dado Cargado': 0.5}
    
    # Evidencia: Salió un 6
    # P(6 | Justo) = 1/6
    # P(6 | Cargado) = 0.5 (del ejemplo 041)
    verosimilitud = {'Dado Justo': 1/6, 'Dado Cargado': 0.5}
    
    posterior = actualizar_creencia_bayes(prior, verosimilitud, 'Salió un 6')
    
    print(f"   Prior: {prior}")
    print(f"   Evidencia: 'Salió un 6'")
    print(f"   Posterior: {posterior}")