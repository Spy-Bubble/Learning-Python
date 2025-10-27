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
# 12. MUESTREO DIRECTO Y POR RECHAZO
# ============================================================================

def muestreo_directo(red_bayesiana, variables, dominios, num_muestras=1000):
    """
    Genera muestras de la distribución conjunta
    Args:
        red_bayesiana: RedBayesiana
        variables: lista ordenada topológicamente
        dominios: dict {variable: [valores]}
        num_muestras: número de muestras
    Returns:
        lista de muestras (cada una es un dict)
    """
    muestras = []
    
    for _ in range(num_muestras):
        muestra = {}
        
        # Muestrear cada variable dado sus padres
        for var in variables:
            padres = red_bayesiana.estructura.get(var, [])
            valores_padres = {p: muestra[p] for p in padres}
            
            # Obtener distribución condicional P(Var | padres)
            probs = []
            valores_posibles = dominios[var]
            for valor in valores_posibles:
                prob = red_bayesiana.prob_dado_padres(var, valor, valores_padres)
                probs.append(prob)
            
            # Muestrear
            muestra[var] = random.choices(valores_posibles, weights=probs, k=1)[0]
        
        muestras.append(muestra)
    
    return muestras


def muestreo_rechazo(query, evidencia, red_bayesiana, variables, dominios, num_muestras=10000):
    """
    Muestreo con rechazo: generar muestras y rechazar las inconsistentes
    Args:
        query: variable (string) a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables
        dominios: dict de dominios
        num_muestras: muestras a generar
    Returns:
        distribución aproximada
    """
    muestras_validas = []
    
    # 1. Generar muestras
    muestras = muestreo_directo(red_bayesiana, variables, dominios, num_muestras)
    
    # 2. Filtrar (rechazar) muestras inconsistentes con evidencia
    for muestra in muestras:
        consistente = all(muestra.get(var) == val for var, val in evidencia.items())
        if consistente:
            muestras_validas.append(muestra)
    
    # 3. Contar frecuencias de query en muestras válidas
    conteos = defaultdict(int)
    for muestra in muestras_validas:
        conteos[muestra[query]] += 1
    
    # 4. Normalizar
    total = sum(conteos.values())
    if total == 0:
        print(f"Advertencia: 0 muestras válidas de {num_muestras}. Aumente N.")
        return {}
    
    print(f"   (Muestreo por Rechazo usó {len(muestras_validas)} de {num_muestras} muestras)")
    return {k: v/total for k, v in conteos.items()}

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
    print("=== 12. Muestreo Directo y por Rechazo ===\n")
    
    red, variables, dominios = crear_red_alarma()
    
    print("Muestreo Directo:")
    muestras = muestreo_directo(red, variables, dominios, num_muestras=1000)
    # Estimar P(Robo=True)
    robos = sum(1 for m in muestras if m['Robo'] == True)
    print(f"   P(Robo=True) ≈ {robos/len(muestras):.4f} (real: 0.001)\n")
    
    print("Muestreo por Rechazo:")
    evidencia = {'Juan': True, 'Maria': True}
    resultado = muestreo_rechazo('Robo', evidencia, red, variables, dominios, 100000)
    print(f"   P(Robo|Juan=True, Maria=True):")
    for valor, prob in resultado.items():
        print(f"      Robo={valor}: {prob:.4f}")