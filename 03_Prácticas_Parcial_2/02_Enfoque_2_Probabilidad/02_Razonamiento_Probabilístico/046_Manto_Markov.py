# ============================================================================
# 7. RED BAYESIANA (DEPENDENCIA)
# ============================================================================
class RedBayesiana:
    def __init__(self):
        self.nodos = {}
        self.estructura = {}
    
    def agregar_nodo(self, nombre, padres, tabla_prob):
        self.nodos[nombre] = {'padres': padres, 'tabla': tabla_prob}
        self.estructura[nombre] = padres
    
    # (prob_dado_padres no es necesaria para esta función)

# ============================================================================
# 9. MANTO DE MARKOV
# ============================================================================

def manto_markov(nodo, red_bayesiana):
    """
    Encuentra el manto de Markov de un nodo
    (padres, hijos, y co-padres de los hijos)
    Args:
        nodo: nombre del nodo
        red_bayesiana: objeto RedBayesiana
    Returns:
        conjunto de nodos en el manto de Markov
    """
    manto = set()
    
    # Agregar padres
    padres = red_bayesiana.estructura.get(nodo, [])
    manto.update(padres)
    
    # Agregar hijos
    hijos = [n for n, pads in red_bayesiana.estructura.items() if nodo in pads]
    manto.update(hijos)
    
    # Agregar co-padres (otros padres de los hijos)
    for hijo in hijos:
        co_padres = red_bayesiana.estructura.get(hijo, [])
        manto.update(co_padres)
    
    # Remover el nodo mismo
    manto.discard(nodo)
    
    return manto

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

# --- Función de ayuda para crear la red de ejemplo ---
def crear_red_alarma():
    red = RedBayesiana()
    red.agregar_nodo('Robo', [], {})
    red.agregar_nodo('Terremoto', [], {})
    red.agregar_nodo('Alarma', ['Robo', 'Terremoto'], {})
    red.agregar_nodo('Juan', ['Alarma'], {})
    red.agregar_nodo('Maria', ['Alarma'], {})
    return red

if __name__ == "__main__":
    print("=== 9. Manto de Markov ===\n")
    
    # Red: Robo -> Alarma <- Terremoto
    #      Alarma -> Juan
    #      Alarma -> Maria
    
    red = crear_red_alarma()
    
    manto_alarma = manto_markov('Alarma', red)
    print(f"   Manto de Markov de 'Alarma': {manto_alarma}")
    print("   (Padres: Robo, Terremoto; Hijos: Juan, Maria; Co-Padres: Ninguno)\n")

    manto_robo = manto_markov('Robo', red)
    print(f"   Manto de Markov de 'Robo': {manto_robo}")
    print("   (Padres: Ninguno; Hijos: Alarma; Co-Padres: Terremoto)\n")