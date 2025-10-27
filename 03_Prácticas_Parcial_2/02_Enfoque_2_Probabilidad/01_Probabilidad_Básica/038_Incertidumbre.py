import math

# ============================================================================
# 1. INCERTIDUMBRE
# ============================================================================

def manejar_incertidumbre(eventos_posibles, probabilidades):
    """
    Modela incertidumbre mediante distribución de probabilidad
    Args:
        eventos_posibles: lista de eventos
        probabilidades: lista de probabilidades correspondientes
    Returns:
        diccionario {evento: probabilidad}
    """
    # Validar que las probabilidades sumen 1
    total = sum(probabilidades)
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"Las probabilidades deben sumar 1, suman {total}")
    
    # Crear distribución
    distribucion = {}
    for evento, prob in zip(eventos_posibles, probabilidades):
        distribucion[evento] = prob
    
    return distribucion


def calcular_entropia(distribucion):
    """
    Calcula la entropía (medida de incertidumbre)
    Args:
        distribucion: dict {evento: probabilidad}
    Returns:
        entropía en bits
    """
    entropia = 0
    for prob in distribucion.values():
        if prob > 0:
            entropia -= prob * math.log2(prob)
    return entropia

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 1. Modelar Incertidumbre ===\n")
    
    clima = ['soleado', 'nublado', 'lluvioso']
    probs_clima = [0.6, 0.3, 0.1]
    
    try:
        dist_clima = manejar_incertidumbre(clima, probs_clima)
        print(f"   Distribución del clima: {dist_clima}")
        
        entropia = calcular_entropia(dist_clima)
        print(f"   Entropía (incertidumbre): {entropia:.3f} bits\n")
    
    except ValueError as e:
        print(f"Error: {e}")