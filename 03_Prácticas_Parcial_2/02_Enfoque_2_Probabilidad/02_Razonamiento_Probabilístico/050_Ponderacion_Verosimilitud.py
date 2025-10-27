import random
from collections import defaultdict

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
# 13. PONDERACIÓN DE VEROSIMILITUD
# ============================================================================

def ponderacion_verosimilitud(query, evidencia, red_bayesiana, variables, dominios, num_muestras=1000):
    """
    Muestreo ponderado: cada muestra tiene un peso según evidencia
    Args:
        query: variable (string) a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables (orden topológico)
        dominios: dict de dominios
        num_muestras: número de muestras
    Returns:
        distribución aproximada
    """
    conteos_ponderados = defaultdict(float)
    
    for _ in range(num_muestras):
        muestra = {}
        peso = 1.0
        
        for var in variables:
            padres = red_bayesiana.estructura.get(var, [])
            valores_padres = {p: muestra[p] for p in padres}
            
            if var in evidencia:
                # Variable observada: fijar valor y actualizar peso
                valor = evidencia[var]
                muestra[var] = valor
                prob = red_bayesiana.prob_dado_padres(var, valor, valores_padres)
                peso *= prob
            else:
                # Variable no observada: muestrear normalmente
                valores_posibles = dominios[var]
                probs = [red_bayesiana.prob_dado_padres(var, val, valores_padres) 
                         for val in valores_posibles]
                muestra[var] = random.choices(valores_posibles, weights=probs, k=1)[0]
        
        # Agregar al conteo ponderado
        conteos_ponderados[muestra[query]] += peso
    
    # Normalizar
    total = sum(conteos_ponderados.values())
    if total == 0:
        return {}
    
    return {k: v/total for k, v in conteos_ponderados.items()}

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
    variables = ['Robo', 'Terremoto', 'Alarma', 'Juan', 'Maria']
    dominios = {
        'Robo': [True, False], 'Terremoto': [True, False],
        'Alarma': [True, False], 'Juan': [True, False], 'Maria': [True, False]
    }
    return red, variables, dominios

if __name__ == "__main__":
    print("=== 13. Ponderación de Verosimilitud ===\n")
    
    red, variables, dominios = crear_red_alarma()

    print("Calculando P(Robo | Juan=True, Maria=True)...")
    evidencia = {'Juan': True, 'Maria': True}
    resultado = ponderacion_verosimilitud('Robo', evidencia, red, variables, dominios, 10000)
    
    print(f"   P(Robo|Juan=True, Maria=True):")
    for valor, prob in resultado.items():
        print(f"      Robo={valor}: {prob:.4f}")
    
    # (El resultado esperado es ~28.4% para Robo=True)