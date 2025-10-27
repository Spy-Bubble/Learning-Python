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
# 9. MANTO DE MARKOV (DEPENDENCIA)
# ============================================================================
def manto_markov(nodo, red_bayesiana):
    manto = set()
    padres = red_bayesiana.estructura.get(nodo, [])
    manto.update(padres)
    hijos = [n for n, pads in red_bayesiana.estructura.items() if nodo in pads]
    manto.update(hijos)
    for hijo in hijos:
        co_padres = red_bayesiana.estructura.get(hijo, [])
        manto.update(co_padres)
    manto.discard(nodo)
    return manto

# ============================================================================
# 14. MONTE CARLO PARA CADENAS DE MARKOV (MCMC)
# ============================================================================

def mcmc_gibbs_sampling(query, evidencia, red_bayesiana, variables, dominios, 
                        num_muestras=1000, burn_in=100):
    """
    MCMC usando Gibbs Sampling
    Args:
        query: variable (string) a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables
        dominios: dict de dominios
        num_muestras: muestras a recolectar
        burn_in: muestras iniciales a descartar
    Returns:
        distribución aproximada
    """
    # Lista de variables no-evidencia
    vars_no_evidencia = [v for v in variables if v not in evidencia]
    
    # Inicializar estado (estado actual de la cadena)
    estado = {}
    for var in variables:
        if var in evidencia:
            estado[var] = evidencia[var]
        else:
            estado[var] = random.choice(dominios[var])
    
    muestras_recolectadas = []
    
    # Generar muestras
    for i in range(num_muestras + burn_in):
        # Muestrear cada variable no observada
        for var in vars_no_evidencia:
            
            # Calcular P(var | Manto de Markov)
            probs = []
            for valor in dominios[var]:
                # Asignar temporalmente el valor a la variable
                estado_temp = dict(estado)
                estado_temp[var] = valor
                
                # P(var | padres)
                padres = red_bayesiana.estructura.get(var, [])
                valores_padres = {p: estado_temp[p] for p in padres}
                prob = red_bayesiana.prob_dado_padres(var, valor, valores_padres)
                
                # Multiplicar por P(hijo | padres_hijo) para cada hijo
                hijos = [n for n, pads in red_bayesiana.estructura.items() 
                         if var in pads]
                for hijo in hijos:
                    padres_hijo = red_bayesiana.estructura[hijo]
                    valores_padres_hijo = {p: estado_temp[p] for p in padres_hijo}
                    prob *= red_bayesiana.prob_dado_padres(hijo, estado_temp[hijo], 
                                                          valores_padres_hijo)
                
                probs.append(prob)
            
            # Normalizar y muestrear
            total = sum(probs)
            if total > 0:
                probs_norm = [p/total for p in probs]
                estado[var] = random.choices(dominios[var], weights=probs_norm, k=1)[0]
            # (Si total es 0, mantener el valor actual de estado[var])
        
        # Guardar muestra (después del burn-in)
        if i >= burn_in:
            muestras_recolectadas.append(dict(estado))
    
    # Contar frecuencias de la variable query
    conteos = defaultdict(int)
    for muestra in muestras_recolectadas:
        conteos[muestra[query]] += 1
    
    # Normalizar
    total_conteos = sum(conteos.values())
    if total_conteos == 0:
        return {}
    
    return {k: v/total_conteos for k, v in conteos.items()}

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
    print("=== 14. MCMC (Gibbs Sampling) ===\n")
    
    red, variables, dominios = crear_red_alarma()
    
    print("Calculando P(Robo | Juan=True, Maria=True)...")
    evidencia = {'Juan': True, 'Maria': True}
    
    resultado_mcmc = mcmc_gibbs_sampling('Robo', evidencia, red, variables, dominios, 
                                         num_muestras=5000, burn_in=500)
    
    print(f"   P(Robo|Juan=True, Maria=True):")
    for valor, prob in resultado_mcmc.items():
        print(f"      Robo={valor}: {prob:.4f}")