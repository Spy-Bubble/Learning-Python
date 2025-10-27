# ============================================================================
# 26. VALOR DE LA INFORMACIÓN
# ============================================================================

def valor_informacion_perfecta(probabilidades, utilidades):
    """
    Calcula el Valor de la Información Perfecta (VIP)
    Args:
        probabilidades: lista de probabilidades de estados [P(s0), P(s1), ...]
        utilidades: diccionario {estado: {accion: utilidad}}
                    Ej: {0: {'A1': 100}, 1: {'A1': 20}}
    Returns:
        VIP (diferencia entre decisión con y sin información)
    """
    
    if not probabilidades or not utilidades:
        return 0
        
    acciones = list(utilidades[0].keys())
    estados = list(range(len(probabilidades)))

    # 1. Utilidad esperada SIN información (elegir la mejor acción promedio)
    utilidad_sin_info = float('-inf')
    for accion in acciones:
        ue_accion = 0
        for estado, prob in enumerate(probabilidades):
            ue_accion += prob * utilidades[estado][accion]
        utilidad_sin_info = max(utilidad_sin_info, ue_accion)

    # 2. Utilidad esperada CON información perfecta
    # (Para cada estado, elegir la mejor acción sabiendo el estado)
    utilidad_con_info = 0
    for estado, prob in enumerate(probabilidades):
        mejor_util_en_estado = max(utilidades[estado].values())
        utilidad_con_info += prob * mejor_util_en_estado
    
    # VIP = diferencia
    return utilidad_con_info - utilidad_sin_info

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 26. Valor de la Información Perfecta ===\n")
    
    # Estados: 0='Petróleo', 1='Seco'
    probs = [0.6, 0.4] # P(Petróleo)=0.6, P(Seco)=0.4
    
    # Acciones: 'A1'='Perforar', 'A2'='No Perforar'
    utils = {
        0: {'A1': 100, 'A2': 0}, # Utilidad si hay Petróleo
        1: {'A1': -50, 'A2': 0}  # Utilidad si está Seco
    }
    
    vip = valor_informacion_perfecta(probs, utils)
    
    print(f"Probabilidades de estado: {probs}")
    print(f"Utilidades (Estado, Acción): {utils}")
    print(f"\n   Valor de la Información Perfecta (VIP) = {vip:.2f}")