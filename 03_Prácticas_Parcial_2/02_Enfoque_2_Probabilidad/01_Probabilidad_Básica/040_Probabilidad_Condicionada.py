from collections import defaultdict

# ============================================================================
# 3. PROBABILIDAD CONDICIONADA Y NORMALIZACIÓN
# ============================================================================

def probabilidad_condicionada(p_ab, p_b):
    """
    Calcula P(A|B) = P(A∩B) / P(B)
    Args:
        p_ab: P(A∩B) - probabilidad de A y B juntos
        p_b: P(B) - probabilidad de B
    Returns:
        P(A|B) - probabilidad de A dado B
    """
    if p_b == 0:
        raise ValueError("P(B) no puede ser 0")
    
    return p_ab / p_b


def normalizar_distribucion(valores):
    """
    Normaliza una distribución para que sume 1
    Args:
        valores: lista o dict de valores no normalizados
    Returns:
        distribución normalizada
    """
    if isinstance(valores, dict):
        total = sum(valores.values())
        if total == 0:
            return {k: 1.0/len(valores) for k in valores} # Dist. uniforme si total es 0
        return {k: v/total for k, v in valores.items()}
    else: # Asumir lista
        total = sum(valores)
        if total == 0:
            return [1.0/len(valores)] * len(valores) # Dist. uniforme
        return [v/total for v in valores]


def probabilidad_conjunta_a_condicional(p_conjunta, variables):
    """
    Convierte probabilidad conjunta P(A,B) a condicional P(A|B)
    Args:
        p_conjunta: dict {(a, b): probabilidad}
        variables: lista de variables ['A', 'B']
    Returns:
        dict de probabilidades condicionales P(A|B) = {b: {a: prob}}
    """
    # Calcular marginales de B (la variable condicionante)
    marginal_b = defaultdict(float)
    for (a, b), prob in p_conjunta.items():
        marginal_b[b] += prob
    
    # Calcular condicionales
    condicionales = defaultdict(dict)
    for (a, b), prob_conjunta in p_conjunta.items():
        if marginal_b[b] > 0:
            # P(a|b) = P(a, b) / P(b)
            condicionales[b][a] = prob_conjunta / marginal_b[b]
    
    return dict(condicionales)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 3. Probabilidad Condicionada y Normalización ===\n")
    
    # Ejemplo 1: Probabilidad Condicionada
    # P(lluvia y paraguas) = 0.08
    # P(paraguas) = 0.1
    p_lluvia_dado_paraguas = probabilidad_condicionada(0.08, 0.1)
    print(f"   P(lluvia|paraguas) = {p_lluvia_dado_paraguas:.2f}\n")
    
    # Ejemplo 2: Normalización
    valores_no_normalizados = {'rojo': 5, 'verde': 10, 'azul': 5}
    normalizados = normalizar_distribucion(valores_no_normalizados)
    print(f"   Valores no normalizados: {valores_no_normalizados}")
    print(f"   Valores normalizados: {normalizados}")
    print(f"   Suma: {sum(normalizados.values())}\n")
    
    # Ejemplo 3: Conjunta a Condicional
    # P(Clima, Tráfico)
    p_conjunta = {
        ('sol', 'ligero'): 0.4,
        ('sol', 'denso'): 0.1,
        ('lluvia', 'ligero'): 0.1,
        ('lluvia', 'denso'): 0.4,
    }
    # Queremos P(Clima | Tráfico)
    p_clima_dado_trafico = probabilidad_conjunta_a_condicional(p_conjunta, ['Clima', 'Tráfico'])
    print(f"   P(Clima | Tráfico): {p_clima_dado_trafico}")