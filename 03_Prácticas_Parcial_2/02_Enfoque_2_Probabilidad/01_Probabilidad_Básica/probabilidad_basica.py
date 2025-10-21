"""
PROBABILIDAD BÁSICA
Algoritmos 1-6: Fundamentos de probabilidad e incertidumbre
"""

import random
from collections import defaultdict
from fractions import Fraction

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
    import math
    entropia = 0
    for prob in distribucion.values():
        if prob > 0:
            entropia -= prob * math.log2(prob)
    return entropia


# ============================================================================
# 2. PROBABILIDAD A PRIORI
# ============================================================================

def probabilidad_priori(evento, espacio_muestral):
    """
    Calcula probabilidad a priori (sin información adicional)
    Args:
        evento: conjunto de resultados favorables
        espacio_muestral: conjunto de todos los resultados posibles
    Returns:
        probabilidad del evento
    """
    # P(A) = |A| / |Ω|
    if len(espacio_muestral) == 0:
        return 0
    
    # Contar elementos del evento que están en el espacio muestral
    favorables = len(set(evento) & set(espacio_muestral))
    total = len(espacio_muestral)
    
    return favorables / total


def probabilidad_uniforme(num_resultados):
    """
    Distribución uniforme (todos igualmente probables)
    Args:
        num_resultados: número de resultados posibles
    Returns:
        probabilidad de cada resultado
    """
    return 1.0 / num_resultados


# ============================================================================
# 3. PROBABILIDAD CONDICIONADA Y NORMALIZACIÓN
# ============================================================================

def probabilidad_condicionada(p_ab, p_b):
    """
    Calcula P(A|B) = P(A∩B) / P(B)
    Args:
        p_ab: P(A∩B) - probabilidad de A y B juntos
        p_b: P(B) - probabilidad de B
    Returns:
        P(A|B) - probabilidad de A dado B
    """
    if p_b == 0:
        raise ValueError("P(B) no puede ser 0")
    
    return p_ab / p_b


def normalizar_distribucion(valores):
    """
    Normaliza una distribución para que sume 1
    Args:
        valores: lista o dict de valores no normalizados
    Returns:
        distribución normalizada
    """
    if isinstance(valores, dict):
        total = sum(valores.values())
        return {k: v/total for k, v in valores.items()}
    else:
        total = sum(valores)
        return [v/total for v in valores]


def probabilidad_conjunta_a_condicional(p_conjunta, variables):
    """
    Convierte probabilidad conjunta P(A,B) a condicional P(A|B)
    Args:
        p_conjunta: dict {(a, b): probabilidad}
        variables: lista de variables ['A', 'B']
    Returns:
        dict de probabilidades condicionales
    """
    # Calcular marginales
    marginales = defaultdict(float)
    for (a, b), prob in p_conjunta.items():
        marginales[b] += prob
    
    # Calcular condicionales
    condicionales = {}
    for (a, b), prob in p_conjunta.items():
        if marginales[b] > 0:
            condicionales[(a, b)] = prob / marginales[b]
    
    return condicionales


# ============================================================================
# 4. DISTRIBUCIÓN DE PROBABILIDAD
# ============================================================================

class DistribucionProbabilidad:
    """
    Representa una distribución de probabilidad discreta
    """
    def __init__(self, valores, probabilidades):
        """
        Args:
            valores: lista de valores posibles
            probabilidades: probabilidades correspondientes
        """
        # Normalizar automáticamente
        total = sum(probabilidades)
        self.distribucion = {
            v: p/total for v, p in zip(valores, probabilidades)
        }
    
    def prob(self, valor):
        """Obtiene probabilidad de un valor"""
        return self.distribucion.get(valor, 0)
    
    def muestra(self):
        """Genera una muestra aleatoria de la distribución"""
        valores = list(self.distribucion.keys())
        probs = list(self.distribucion.values())
        return random.choices(valores, weights=probs, k=1)[0]
    
    def esperanza(self):
        """Calcula el valor esperado (media)"""
        return sum(v * p for v, p in self.distribucion.items())
    
    def varianza(self):
        """Calcula la varianza"""
        media = self.esperanza()
        return sum(p * (v - media)**2 for v, p in self.distribucion.items())


def distribucion_binomial(n, p, k):
    """
    Probabilidad binomial: P(X=k) en n intentos con probabilidad p
    Args:
        n: número de intentos
        p: probabilidad de éxito
        k: número de éxitos deseados
    Returns:
        probabilidad
    """
    from math import comb
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))


# ============================================================================
# 5. INDEPENDENCIA CONDICIONAL
# ============================================================================

def son_independientes(p_a, p_b, p_ab, tolerancia=0.001):
    """
    Verifica si A y B son independientes: P(A∩B) = P(A)·P(B)
    Args:
        p_a: P(A)
        p_b: P(B)
        p_ab: P(A∩B)
        tolerancia: margen de error
    Returns:
        True si son independientes
    """
    return abs(p_ab - (p_a * p_b)) < tolerancia


def independencia_condicional(p_a_dado_c, p_b_dado_c, p_ab_dado_c, tolerancia=0.001):
    """
    Verifica independencia condicional: P(A,B|C) = P(A|C)·P(B|C)
    Args:
        p_a_dado_c: P(A|C)
        p_b_dado_c: P(B|C)
        p_ab_dado_c: P(A,B|C)
        tolerancia: margen de error
    Returns:
        True si A y B son condicionalmente independientes dado C
    """
    return abs(p_ab_dado_c - (p_a_dado_c * p_b_dado_c)) < tolerancia


def factorizar_por_independencia(variables, dependencias):
    """
    Factoriza una distribución conjunta usando independencias
    Args:
        variables: lista de variables
        dependencias: dict {var: lista de padres}
    Returns:
        factorización como string
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
# 6. REGLA DE BAYES
# ============================================================================

def regla_bayes(p_b_dado_a, p_a, p_b):
    """
    Calcula P(A|B) usando: P(A|B) = P(B|A)·P(A) / P(B)
    Args:
        p_b_dado_a: P(B|A) - verosimilitud
        p_a: P(A) - probabilidad a priori
        p_b: P(B) - evidencia
    Returns:
        P(A|B) - probabilidad a posteriori
    """
    if p_b == 0:
        raise ValueError("P(B) no puede ser 0")
    
    return (p_b_dado_a * p_a) / p_b


def regla_bayes_multiple(p_b_dado_ai, p_ai):
    """
    Regla de Bayes con múltiples hipótesis
    Args:
        p_b_dado_ai: lista de P(B|Ai) para cada hipótesis
        p_ai: lista de P(Ai) para cada hipótesis
    Returns:
        lista de P(Ai|B) - posteriores normalizadas
    """
    # Calcular numeradores
    numeradores = [p_b_dado_ai[i] * p_ai[i] for i in range(len(p_ai))]
    
    # Calcular P(B) = suma de todos los numeradores
    p_b = sum(numeradores)
    
    if p_b == 0:
        return [0] * len(p_ai)
    
    # Calcular posteriores
    posteriores = [num / p_b for num in numeradores]
    
    return posteriores


def actualizar_creencia_bayes(prior, verosimilitud, evidencia):
    """
    Actualización bayesiana de creencias
    Args:
        prior: dict {hipótesis: probabilidad_previa}
        verosimilitud: dict {hipótesis: P(evidencia|hipótesis)}
        evidencia: nombre de la evidencia observada
    Returns:
        dict {hipótesis: probabilidad_posterior}
    """
    # Calcular numeradores
    numeradores = {}
    for hipotesis in prior.keys():
        numeradores[hipotesis] = prior[hipotesis] * verosimilitud[hipotesis]
    
    # Normalizar
    total = sum(numeradores.values())
    
    if total == 0:
        return prior  # No cambio si evidencia imposible
    
    posterior = {h: num/total for h, num in numeradores.items()}
    
    return posterior


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== PROBABILIDAD BÁSICA ===\n")
    
    # Ejemplo 1: Incertidumbre
    print("1. Modelar Incertidumbre:")
    clima = ['soleado', 'nublado', 'lluvioso']
    probs_clima = [0.6, 0.3, 0.1]
    dist_clima = manejar_incertidumbre(clima, probs_clima)
    print(f"   Distribución del clima: {dist_clima}")
    entropia = calcular_entropia(dist_clima)
    print(f"   Entropía (incertidumbre): {entropia:.3f} bits\n")
    
    # Ejemplo 2: Probabilidad a priori
    print("2. Probabilidad A Priori:")
    dado = [1, 2, 3, 4, 5, 6]
    evento_par = [2, 4, 6]
    p_par = probabilidad_priori(evento_par, dado)
    print(f"   P(número par) = {p_par:.3f}\n")
    
    # Ejemplo 3: Probabilidad condicionada
    print("3. Probabilidad Condicionada:")
    # P(lluvia y paraguas) = 0.08
    # P(paraguas) = 0.1
    p_lluvia_dado_paraguas = probabilidad_condicionada(0.08, 0.1)
    print(f"   P(lluvia|paraguas) = {p_lluvia_dado_paraguas:.2f}\n")
    
    # Ejemplo 4: Distribución de probabilidad
    print("4. Distribución de Probabilidad:")
    dist = DistribucionProbabilidad([1, 2, 3, 4, 5, 6], [1, 1, 1, 1, 1, 1])
    print(f"   P(3) = {dist.prob(3):.3f}")
    print(f"   Valor esperado: {dist.esperanza():.2f}")
    print(f"   Muestra aleatoria: {dist.muestra()}\n")
    
    # Ejemplo 5: Independencia
    print("5. Independencia:")
    # Lanzar moneda y dado
    p_cara = 0.5
    p_seis = 1/6
    p_cara_y_seis = 0.5 * (1/6)
    son_indep = son_independientes(p_cara, p_seis, p_cara_y_seis)
    print(f"   ¿Cara y seis son independientes? {son_indep}\n")
    
    # Ejemplo 6: Regla de Bayes
    print("6. Regla de Bayes:")
    # Test médico
    # P(positivo|enfermo) = 0.95
    # P(enfermo) = 0.01
    # P(positivo) = 0.05
    p_enfermo_dado_positivo = regla_bayes(0.95, 0.01, 0.05)
    print(f"   P(enfermo|test positivo) = {p_enfermo_dado_positivo:.3f}")
    print(f"   Interpretación: Solo 19% de probabilidad real de estar enfermo\n")
    
    # Ejemplo con actualización de creencias
    print("   Actualización Bayesiana:")
    prior = {'H1': 0.6, 'H2': 0.4}
    verosim = {'H1': 0.8, 'H2': 0.3}
    posterior = actualizar_creencia_bayes(prior, verosim, 'evidencia')
    print(f"   Prior: {prior}")
    print(f"   Posterior: {posterior}")