"""
RAZONAMIENTO PROBABILÍSTICO
Algoritmos 7-14: Redes Bayesianas e inferencia
"""

import random
from collections import defaultdict
from itertools import product

# ============================================================================
# 7. RED BAYESIANA
# ============================================================================

class RedBayesiana:
    """
    Representa una Red Bayesiana (grafo dirigido acíclico con probabilidades)
    """
    def __init__(self):
        self.nodos = {}  # {nombre: Nodo}
        self.estructura = {}  # {hijo: [padres]}
    
    def agregar_nodo(self, nombre, padres, tabla_prob):
        """
        Agrega un nodo a la red
        Args:
            nombre: nombre del nodo
            padres: lista de nombres de nodos padres
            tabla_prob: dict con P(nodo|padres)
        """
        self.nodos[nombre] = {
            'padres': padres,
            'tabla': tabla_prob
        }
        self.estructura[nombre] = padres
    
    def prob_dado_padres(self, nodo, valor, valores_padres):
        """
        Obtiene P(nodo=valor|padres)
        Args:
            nodo: nombre del nodo
            valor: valor del nodo
            valores_padres: dict {padre: valor}
        Returns:
            probabilidad
        """
        tabla = self.nodos[nodo]['tabla']
        padres = self.nodos[nodo]['padres']
        
        # Sin padres
        if not padres:
            return tabla.get(valor, 0)
        
        # Con padres: buscar en tabla
        clave_padres = tuple(valores_padres.get(p) for p in padres)
        return tabla.get((valor, *clave_padres), 0)


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
        valores_padres = {p: valores[p] for p in padres}
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
# 10. INFERENCIA POR ENUMERACIÓN
# ============================================================================

def inferencia_enumeracion(query, evidencia, red_bayesiana, variables, dominios):
    """
    Calcula P(query|evidencia) por enumeración completa
    Args:
        query: dict {variable: valor} a consultar
        evidencia: dict {variable: valor} observado
        red_bayesiana: RedBayesiana
        variables: lista de todas las variables
        dominios: dict {variable: [valores posibles]}
    Returns:
        probabilidad normalizada
    """
    # Variables ocultas (no query ni evidencia)
    ocultas = [v for v in variables if v not in query and v not in evidencia]
    
    # Enumerar todas las asignaciones de variables ocultas
    resultados = {}
    
    for valor_query in dominios[list(query.keys())[0]]:
        suma = 0
        asignacion_fija = {**evidencia, **{list(query.keys())[0]: valor_query}}
        
        # Enumerar sobre variables ocultas
        for valores_ocultas in product(*[dominios[v] for v in ocultas]):
            asignacion_completa = dict(asignacion_fija)
            for v, val in zip(ocultas, valores_ocultas):
                asignacion_completa[v] = val
            
            # Calcular probabilidad conjunta con regla de la cadena
            prob = regla_cadena(variables, red_bayesiana, asignacion_completa)
            suma += prob
        
        resultados[valor_query] = suma
    
    # Normalizar
    total = sum(resultados.values())
    if total > 0:
        resultados = {k: v/total for k, v in resultados.items()}
    
    return resultados


# ============================================================================
# 11. ELIMINACIÓN DE VARIABLES
# ============================================================================

def eliminacion_variables(query, evidencia, red_bayesiana, orden_eliminacion):
    """
    Inferencia más eficiente eliminando variables en orden
    Args:
        query: variable a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        orden_eliminacion: lista ordenada de variables a eliminar
    Returns:
        distribución de probabilidad
    """
    # Implementación simplificada
    # En práctica, se manipulan factores y se van eliminando variables
    
    factores = []
    
    # Crear factores iniciales de cada nodo
    for nodo in red_bayesiana.nodos:
        factores.append({
            'variables': [nodo] + red_bayesiana.estructura.get(nodo, []),
            'tabla': red_bayesiana.nodos[nodo]['tabla']
        })
    
    # Reducir factores con evidencia
    for var, valor in evidencia.items():
        factores = [reducir_factor(f, var, valor) for f in factores]
    
    # Eliminar variables en orden
    for var in orden_eliminacion:
        if var != query:
            factores = sumar_variable(factores, var)
    
    # El resultado es el factor final
    resultado = factores[0] if factores else {}
    
    return resultado


def reducir_factor(factor, variable, valor):
    """Reduce un factor fijando una variable a un valor"""
    # Simplificado
    return factor


def sumar_variable(factores, variable):
    """Suma (marginaliza) una variable de los factores"""
    # Simplificado
    return factores


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
            
            # Obtener distribución condicional
            probs = []
            for valor in dominios[var]:
                prob = red_bayesiana.prob_dado_padres(var, valor, valores_padres)
                probs.append(prob)
            
            # Muestrear
            muestra[var] = random.choices(dominios[var], weights=probs, k=1)[0]
        
        muestras.append(muestra)
    
    return muestras


def muestreo_rechazo(query, evidencia, red_bayesiana, variables, dominios, num_muestras=10000):
    """
    Muestreo con rechazo: generar muestras y rechazar las inconsistentes
    Args:
        query: variable a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables
        dominios: dict de dominios
        num_muestras: muestras a generar
    Returns:
        distribución aproximada
    """
    muestras_validas = []
    
    # Generar muestras
    muestras = muestreo_directo(red_bayesiana, variables, dominios, num_muestras)
    
    # Filtrar muestras consistentes con evidencia
    for muestra in muestras:
        consistente = all(muestra.get(var) == val for var, val in evidencia.items())
        if consistente:
            muestras_validas.append(muestra)
    
    # Contar frecuencias de query
    conteos = defaultdict(int)
    for muestra in muestras_validas:
        conteos[muestra[query]] += 1
    
    # Normalizar
    total = sum(conteos.values())
    if total == 0:
        return {}
    
    return {k: v/total for k, v in conteos.items()}


# ============================================================================
# 13. PONDERACIÓN DE VEROSIMILITUD
# ============================================================================

def ponderacion_verosimilitud(query, evidencia, red_bayesiana, variables, dominios, num_muestras=1000):
    """
    Muestreo ponderado: cada muestra tiene un peso según evidencia
    Args:
        query: variable a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables
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
                probs = [red_bayesiana.prob_dado_padres(var, val, valores_padres) 
                        for val in dominios[var]]
                muestra[var] = random.choices(dominios[var], weights=probs, k=1)[0]
        
        # Agregar al conteo ponderado
        conteos_ponderados[muestra[query]] += peso
    
    # Normalizar
    total = sum(conteos_ponderados.values())
    if total == 0:
        return {}
    
    return {k: v/total for k, v in conteos_ponderados.items()}


# ============================================================================
# 14. MONTE CARLO PARA CADENAS DE MARKOV (MCMC)
# ============================================================================

def mcmc_gibbs_sampling(query, evidencia, red_bayesiana, variables, dominios, 
                        num_muestras=1000, burn_in=100):
    """
    MCMC usando Gibbs Sampling
    Args:
        query: variable a consultar
        evidencia: dict de evidencia
        red_bayesiana: RedBayesiana
        variables: lista de variables
        dominios: dict de dominios
        num_muestras: muestras a recolectar
        burn_in: muestras iniciales a descartar
    Returns:
        distribución aproximada
    """
    # Inicializar estado con valores aleatorios
    estado = {}
    for var in variables:
        if var in evidencia:
            estado[var] = evidencia[var]
        else:
            estado[var] = random.choice(dominios[var])
    
    muestras = []
    
    # Generar muestras
    for i in range(num_muestras + burn_in):
        # Para cada variable no observada
        for var in variables:
            if var not in evidencia:
                # Calcular P(var|manto_markov)
                manto = manto_markov(var, red_bayesiana)
                
                probs = []
                for valor in dominios[var]:
                    # Calcular probabilidad condicional
                    estado_temp = dict(estado)
                    estado_temp[var] = valor
                    
                    # Prob basada en padres
                    padres = red_bayesiana.estructura.get(var, [])
                    valores_padres = {p: estado_temp[p] for p in padres}
                    prob = red_bayesiana.prob_dado_padres(var, valor, valores_padres)
                    
                    # Prob basada en hijos
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
                    probs = [p/total for p in probs]
                    estado[var] = random.choices(dominios[var], weights=probs, k=1)[0]
        
        # Guardar muestra (después del burn-in)
        if i >= burn_in:
            muestras.append(dict(estado))
    
    # Contar frecuencias
    conteos = defaultdict(int)
    for muestra in muestras:
        conteos[muestra[query]] += 1
    
    # Normalizar
    total = sum(conteos.values())
    if total == 0:
        return {}
    
    return {k: v/total for k, v in conteos.items()}


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== RAZONAMIENTO PROBABILÍSTICO ===\n")
    
    # Crear una red bayesiana simple: Alarma
    # Robo → Alarma ← Terremoto
    # Alarma → LlamadaJuan
    # Alarma → LlamadaMaria
    
    print("7. Red Bayesiana:")
    red = RedBayesiana()
    
    # Nodos sin padres
    red.agregar_nodo('Robo', [], {
        True: 0.001,
        False: 0.999
    })
    
    red.agregar_nodo('Terremoto', [], {
        True: 0.002,
        False: 0.998
    })
    
    # Alarma depende de Robo y Terremoto
    red.agregar_nodo('Alarma', ['Robo', 'Terremoto'], {
        (True, True, True): 0.95,
        (False, True, True): 0.05,
        (True, True, False): 0.94,
        (False, True, False): 0.06,
        (True, False, True): 0.29,
        (False, False, True): 0.71,
        (True, False, False): 0.001,
        (False, False, False): 0.999,
    })
    
    # Juan llama si hay alarma
    red.agregar_nodo('Juan', ['Alarma'], {
        (True, True): 0.90,
        (False, True): 0.10,
        (True, False): 0.05,
        (False, False): 0.95,
    })
    
    # Maria llama si hay alarma
    red.agregar_nodo('Maria', ['Alarma'], {
        (True, True): 0.70,
        (False, True): 0.30,
        (True, False): 0.01,
        (False, False): 0.99,
    })
    
    print("   Red creada con 5 nodos\n")
    
    # Ejemplo 8: Regla de la cadena
    print("8. Regla de la Cadena:")
    variables = ['Robo', 'Terremoto', 'Alarma', 'Juan', 'Maria']
    valores = {
        'Robo': True,
        'Terremoto': False,
        'Alarma': True,
        'Juan': True,
        'Maria': True
    }
    prob_conjunta = regla_cadena(variables, red, valores)
    print(f"   P(Robo=T, Terremoto=F, Alarma=T, Juan=T, Maria=T)")
    print(f"   = {prob_conjunta:.6f}\n")
    
    # Ejemplo 9: Manto de Markov
    print("9. Manto de Markov:")
    manto = manto_markov('Alarma', red)
    print(f"   Manto de Markov de 'Alarma': {manto}\n")
    
    # Ejemplo 12: Muestreo directo
    print("12. Muestreo Directo:")
    dominios = {
        'Robo': [True, False],
        'Terremoto': [True, False],
        'Alarma': [True, False],
        'Juan': [True, False],
        'Maria': [True, False]
    }
    
    muestras = muestreo_directo(red, variables, dominios, num_muestras=1000)
    
    # Estimar P(Robo=True)
    robos = sum(1 for m in muestras if m['Robo'] == True)
    print(f"   P(Robo=True) ≈ {robos/len(muestras):.4f}")
    print(f"   (valor real: 0.001)\n")
    
    # Ejemplo 13: Ponderación de verosimilitud
    print("13. Ponderación de Verosimilitud:")
    evidencia = {'Juan': True, 'Maria': True}
    resultado = ponderacion_verosimilitud('Robo', evidencia, red, variables, dominios, 5000)
    print(f"   P(Robo|Juan=True, Maria=True):")
    for valor, prob in resultado.items():
        print(f"      Robo={valor}: {prob:.4f}")
    print()
    
    # Ejemplo 14: MCMC
    print("14. MCMC (Gibbs Sampling):")
    resultado_mcmc = mcmc_gibbs_sampling('Alarma', evidencia, red, variables, dominios, 
                                         num_muestras=1000, burn_in=100)
    print(f"   P(Alarma|Juan=True, Maria=True):")
    for valor, prob in resultado_mcmc.items():
        print(f"      Alarma={valor}: {prob:.4f}")