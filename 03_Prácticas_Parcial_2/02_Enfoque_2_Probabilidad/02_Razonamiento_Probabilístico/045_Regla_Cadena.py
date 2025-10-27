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
    
    def prob_dado_padres(self, nodo, valor, valores_padres):
        tabla = self.nodos[nodo]['tabla']
        padres = self.nodos[nodo]['padres']
        if not padres:
            return tabla.get(valor, 0)
        clave_padres = tuple(valores_padres.get(p) for p in padres)
        clave_completa = (valor,) + clave_padres
        return tabla.get(clave_completa, 0)

# ============================================================================
# 8. REGLA DE LA CADENA
# ============================================================================

def regla_cadena(variables, red_bayesiana, valores):
    """
    Aplica regla de la cadena: P(X1,...,Xn) = ∏ P(Xi|padres(Xi))
    Args:
        variables: lista ordenada de variables
        red_bayesiana: objeto RedBayesiana
        valores: dict {variable: valor}
    Returns:
        probabilidad conjunta
    """
    prob_conjunta = 1.0
    
    for var in variables:
        padres = red_bayesiana.estructura.get(var, [])
        # Asegurarse de que los valores de los padres existen en el dict
        valores_padres = {p: valores.get(p) for p in padres}
        
        prob = red_bayesiana.prob_dado_padres(var, valores[var], valores_padres)
        prob_conjunta *= prob
    
    return prob_conjunta


def factorizacion_cadena(variables, dependencias):
    """
    Genera la factorización según la regla de la cadena
    Args:
        variables: lista de variables en orden
        dependencias: dict {var: [padres]}
    Returns:
        string con la factorización
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

# --- Función de ayuda para crear la red de ejemplo ---
def crear_red_alarma():
    red = RedBayesiana()
    red.agregar_nodo('Robo', [], {True: 0.001, False: 0.999})
    red.agregar_nodo('Terremoto', [], {True: 0.002, False: 0.998})
    red.agregar_nodo('Alarma', ['Robo', 'Terremoto'], {
        (True, True, True): 0.95, (False, True, True): 0.05,
        (True, True, False): 0.94, (False, True, False): 0.06,
        (True, False, True): 0.29, (False, False, True): 0.71,
        (True, False, False): 0.001, (False, False, False): 0.999,
    })
    red.agregar_nodo('Juan', ['Alarma'], {
        (True, True): 0.90, (False, True): 0.10,
        (True, False): 0.05, (False, False): 0.95,
    })
    red.agregar_nodo('Maria', ['Alarma'], {
        (True, True): 0.70, (False, True): 0.30,
        (True, False): 0.01, (False, False): 0.99,
    })
    return red

if __name__ == "__main__":
    print("=== 8. Regla de la Cadena ===\n")
    
    red = crear_red_alarma()
    variables = ['Robo', 'Terremoto', 'Alarma', 'Juan', 'Maria']
    
    print("Factorización de la red:")
    print(f"   P(R,T,A,J,M) = {factorizacion_cadena(variables, red.estructura)}\n")

    print("Cálculo de probabilidad conjunta:")
    valores = {
        'Robo': True,
        'Terremoto': False,
        'Alarma': True,
        'Juan': True,
        'Maria': True
    }
    prob_conjunta = regla_cadena(variables, red, valores)
    print(f"   P(Robo=T, Terremoto=F, Alarma=T, Juan=T, Maria=T)")
    print(f"   = P(R=T) * P(T=F) * P(A=T|R=T,T=F) * P(J=T|A=T) * P(M=T|A=T)")
    print(f"   = 0.001 * 0.998 * 0.94 * 0.90 * 0.70")
    print(f"   = {prob_conjunta:.8f}\n")