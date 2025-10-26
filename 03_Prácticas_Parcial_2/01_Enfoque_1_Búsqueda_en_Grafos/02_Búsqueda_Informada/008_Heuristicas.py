import math

# ============================================================================
# 8. HEURÍSTICAS
# ============================================================================

def heuristica_distancia_manhattan(nodo, objetivo):
    """
    Calcula distancia Manhattan entre dos puntos (x, y)
    Args:
        nodo: tupla (x, y)
        objetivo: tupla (x, y)
    Returns:
        distancia Manhattan
    """
    return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])


def heuristica_distancia_euclidiana(nodo, objetivo):
    """
    Calcula distancia euclidiana entre dos puntos
    Args:
        nodo: tupla (x, y)
        objetivo: tupla (x, y)
    Returns:
        distancia euclidiana
    """
    return math.sqrt((nodo[0] - objetivo[0])**2 + (nodo[1] - objetivo[1])**2)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    punto_a = (0, 0)
    punto_b = (3, 4)
    
    print("=== Pruebas de Heurísticas ===\n")
    
    dist_man = heuristica_distancia_manhattan(punto_a, punto_b)
    print(f"Distancia Manhattan entre {punto_a} y {punto_b}: {dist_man}")
    
    dist_euc = heuristica_distancia_euclidiana(punto_a, punto_b)
    print(f"Distancia Euclidiana entre {punto_a} y {punto_b}: {dist_euc}")