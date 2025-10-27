import math

# ============================================================================
# 24. TEORÍA DE LA UTILIDAD: FUNCIÓN DE UTILIDAD
# ============================================================================

def funcion_utilidad_lineal(x, utilidad_min=0, utilidad_max=100):
    """
    Función de utilidad lineal simple
    Args:
        x: valor del resultado (entre 0 y 1)
        utilidad_min: utilidad mínima
        utilidad_max: utilidad máxima
    Returns:
        utilidad normalizada
    """
    return utilidad_min + (utilidad_max - utilidad_min) * x


def funcion_utilidad_logaritmica(riqueza, constante=1):
    """
    Función de utilidad logarítmica (aversión al riesgo)
    Args:
        riqueza: cantidad de dinero o recurso
        constante: constante de escala
    Returns:
        utilidad logarítmica
    """
    if riqueza <= 0:
        return float('-inf')
    return constante * math.log(riqueza)


def utilidad_esperada(acciones, probabilidades, utilidades):
    """
    Calcula utilidad esperada de una acción
    Args:
        acciones: lista de acciones posibles
        probabilidades: diccionario {accion: [probs de resultados]}
        utilidades: diccionario {accion: [utilidades de resultados]}
    Returns:
        diccionario {accion: utilidad_esperada}
    """
    utilidades_esperadas = {}
    
    for accion in acciones:
        probs = probabilidades[accion]
        utils = utilidades[accion]
        utilidades_esperadas[accion] = sum(p * u for p, u in zip(probs, utils))
    
    return utilidades_esperadas

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 24. Teoría de la Utilidad ===\n")
    
    print("Probando Utilidad Lineal (x=0.75):")
    print(f"   Utilidad: {funcion_utilidad_lineal(0.75)}\n")

    print("Probando Utilidad Logarítmica (riqueza=1000):")
    print(f"   Utilidad: {funcion_utilidad_logaritmica(1000):.2f}\n")
    
    # Ejemplo de Utilidad Esperada
    acciones = ['invertir', 'ahorrar']
    probs = {
        'invertir': [0.5, 0.5], # 50% éxito, 50% fracaso
        'ahorrar': [1.0] # 100%
    }
    utils = {
        'invertir': [1000, -500], # Utilidad de éxito, utilidad de fracaso
        'ahorrar': [100] # Utilidad de ahorrar
    }
    
    print("Probando Utilidad Esperada:")
    ue = utilidad_esperada(acciones, probs, utils)
    print(f"   Utilidades Esperadas: {ue}")