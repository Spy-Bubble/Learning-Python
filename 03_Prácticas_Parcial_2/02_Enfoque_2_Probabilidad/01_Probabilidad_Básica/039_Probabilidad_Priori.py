# ============================================================================
# 2. PROBABILIDAD A PRIORI
# ============================================================================

def probabilidad_priori(evento, espacio_muestral):
    """
    Calcula probabilidad a priori (sin información adicional)
    Args:
        evento: conjunto de resultados favorables
        espacio_muestral: conjunto de todos los resultados posibles
    Returns:
        probabilidad del evento
    """
    # P(A) = |A| / |Ω|
    if len(espacio_muestral) == 0:
        return 0
    
    # Contar elementos del evento que están en el espacio muestral
    favorables = len(set(evento) & set(espacio_muestral))
    total = len(espacio_muestral)
    
    return favorables / total


def probabilidad_uniforme(num_resultados):
    """
    Distribución uniforme (todos igualmente probables)
    Args:
        num_resultados: número de resultados posibles
    Returns:
        probabilidad de cada resultado
    """
    if num_resultados == 0:
        return 0
    return 1.0 / num_resultados

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 2. Probabilidad A Priori ===\n")
    
    # Ejemplo 1: Dado
    dado = [1, 2, 3, 4, 5, 6]
    evento_par = [2, 4, 6]
    p_par = probabilidad_priori(evento_par, dado)
    print(f"   Espacio muestral (dado): {dado}")
    print(f"   Evento (par): {evento_par}")
    print(f"   P(número par) = {p_par:.3f}\n")
    
    # Ejemplo 2: Uniforme
    p_dado_uniforme = probabilidad_uniforme(len(dado))
    print(f"   Probabilidad uniforme de un resultado del dado: {p_dado_uniforme:.3f}")