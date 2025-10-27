from itertools import product

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
# 8. REGLA DE LA CADENA (DEPENDENCIA)
# ============================================================================
def regla_cadena(variables, red_bayesiana, valores):
    prob_conjunta = 1.0
    for var in variables:
        padres = red_bayesiana.estructura.get(var, [])
        valores_padres = {p: valores.get(p) for p in padres}
        prob = red_bayesiana.prob_dado_padres(var, valores[var], valores_padres)
        prob_conjunta *= prob
    return prob_conjunta

# ============================================================================
# 10. INFERENCIA POR ENUMERACIÓN
# ============================================================================

def inferencia_enumeracion(query_var, evidencia, red_bayesiana, variables, dominios):
    """
    Calcula P(query|evidencia) por enumeración completa
    Args:
        query_var: variable (string) a consultar
        evidencia: dict {variable: valor} observado
        red_bayesiana: RedBayesiana
        variables: lista de todas las variables (en orden topológico)
        dominios: dict {variable: [valores posibles]}
    Returns:
        dict {valor_query: probabilidad_normalizada}
    """
    # Variables ocultas (no query ni evidencia)
    ocultas = [v for v in variables if v != query_var and v not in evidencia]
    
    resultados = {}
    
    # Para cada valor posible de la variable query
    for valor_query in dominios[query_var]:
        suma = 0
        asignacion_fija = {**evidencia, query_var: valor_query}
        
        # Generar todas las combinaciones de valores de variables ocultas
        valores_posibles_ocultas = [dominios[v] for v in ocultas]
        
        for valores_ocultas in product(*valores_posibles_ocultas):
            asignacion_completa = dict(asignacion_fija)
            asignacion_completa.update(zip(ocultas, valores_ocultas))
            
            # Calcular probabilidad conjunta con regla de la cadena
            prob = regla_cadena(variables, red_bayesiana, asignacion_completa)
            suma += prob
        
        resultados[valor_query] = suma
    
    # Normalizar
    total = sum(resultados.values())
    if total > 0:
        resultados_normalizados = {k: v/total for k, v in resultados.items()}
    else:
        # Si la evidencia es imposible, P(E)=0
        resultados_normalizados = {k: 0 for k in resultados}
        
    return resultados_normalizados

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
    print("=== 10. Inferencia por Enumeración ===\n")
    
    red = crear_red_alarma()
    variables = ['Robo', 'Terremoto', 'Alarma', 'Juan', 'Maria']
    dominios = {
        'Robo': [True, False], 'Terremoto': [True, False],
        'Alarma': [True, False], 'Juan': [True, False], 'Maria': [True, False]
    }
    
    print("Calculando P(Robo | Juan=True, Maria=True)...")
    # P(Robo | Juan=T, Maria=T)
    # Variables Ocultas: Terremoto, Alarma
    evidencia = {'Juan': True, 'Maria': True}
    query_var = 'Robo'
    
    resultado = inferencia_enumeracion(query_var, evidencia, red, variables, dominios)
    
    for valor, prob in resultado.items():
        print(f"   P(Robo={valor} | J=T, M=T) = {prob:.4f}")
    
    # (El resultado esperado es ~28.4% para Robo=True)