# ============================================================================
# 5. INDEPENDENCIA CONDICIONAL
# ============================================================================

def son_independientes(p_a, p_b, p_ab, tolerancia=0.001):
    """
    Verifica si A y B son independientes: P(A∩B) = P(A)·P(B)
    Args:
        p_a: P(A)
        p_b: P(B)
        p_ab: P(A∩B)
        tolerancia: margen de error
    Returns:
        True si son independientes
    """
    return abs(p_ab - (p_a * p_b)) < tolerancia


def independencia_condicional(p_a_dado_c, p_b_dado_c, p_ab_dado_c, tolerancia=0.001):
    """
    Verifica independencia condicional: P(A,B|C) = P(A|C)·P(B|C)
    Args:
        p_a_dado_c: P(A|C)
        p_b_dado_c: P(B|C)
        p_ab_dado_c: P(A,B|C)
        tolerancia: margen de error
    Returns:
        True si A y B son condicionalmente independientes dado C
    """
    return abs(p_ab_dado_c - (p_a_dado_c * p_b_dado_c)) < tolerancia


def factorizar_por_independencia(variables, dependencias):
    """
    Factoriza una distribución conjunta usando independencias (Regla de la Cadena)
    Args:
        variables: lista de variables (en orden topológico)
        dependencias: dict {var: lista de padres}
    Returns:
        factorización como string
    """
    factores = []
    for var in variables:
        padres = dependencias.get(var, [])
        if padres:
            factores.append(f"P({var}|{','.join(padres)})")
        else:
            factores.append(f"P({var})")
    
    return " × ".join(factores)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 5. Independencia Condicional ===\n")
    
    # Ejemplo 1: Independencia
    print("Independencia (Lanzar moneda y dado):")
    p_cara = 0.5
    p_seis = 1/6
    p_cara_y_seis = 0.5 * (1/6) # Se sabe que son independientes
    son_indep = son_independientes(p_cara, p_seis, p_cara_y_seis)
    print(f"   P(Cara)={p_cara:.2f}, P(Seis)={p_seis:.2f}, P(Cara y Seis)={p_cara_y_seis:.2f}")
    print(f"   ¿Son independientes? {son_indep}\n")
    
    # Ejemplo 2: Independencia Condicional
    print("Independencia Condicional:")
    # P(DolorCabeza | Gripe) = 0.8
    # P(Fiebre | Gripe) = 0.9
    # P(DolorCabeza y Fiebre | Gripe) = 0.72 (Asumiendo 0.8 * 0.9)
    son_indep_cond = independencia_condicional(0.8, 0.9, 0.72)
    print(f"   P(DC|G)=0.8, P(F|G)=0.9, P(DC,F|G)=0.72")
    print(f"   ¿Son cond. independientes (dado Gripe)? {son_indep_cond}\n")
    
    # Ejemplo 3: Factorización (Red Bayesiana simple)
    print("Factorización (Regla de la Cadena):")
    # A -> B, A -> C
    variables_red = ['A', 'B', 'C']
    dependencias_red = {'A': [], 'B': ['A'], 'C': ['A']}
    fact = factorizar_por_independencia(variables_red, dependencias_red)
    print(f"   Red: A -> B, A -> C")
    print(f"   P(A,B,C) = {fact}")