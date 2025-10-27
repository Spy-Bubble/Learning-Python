import random
from collections import defaultdict

# ============================================================================
# 40. GRAMÁTICAS PROBABILÍSTICAS INDEPENDIENTES DEL CONTEXTO (PCFG)
# ============================================================================

class PCFG:
    """
    Probabilistic Context-Free Grammar (PCFG)
    """
    def __init__(self, simbolo_inicial='S'):
        # {no_terminal: [(expansion_tupla, probabilidad)]}
        self.reglas = defaultdict(list)
        # Para búsqueda inversa rápida (terminal -> no_terminal)
        self.reglas_lexicales = defaultdict(list)
        self.simbolo_inicial = simbolo_inicial
        self._check_sum = True # Verificar que probabilidades sumen 1

    def agregar_regla(self, simbolo_lhs, expansion_rhs, probabilidad):
        """
        Agrega una regla de producción A -> B C [prob] o A -> terminal [prob]
        Args:
            simbolo_lhs: símbolo no terminal (string, ej: 'S', 'NP')
            expansion_rhs: lista de símbolos (ej: ['NP', 'VP'] o ['palabra'])
            probabilidad: P(expansion | simbolo_lhs)
        """
        if not isinstance(expansion_rhs, list):
             raise TypeError("La expansión debe ser una lista de símbolos.")
        if probabilidad < 0 or probabilidad > 1:
             raise ValueError("La probabilidad debe estar entre 0 y 1.")

        expansion_tupla = tuple(expansion_rhs) # Usar tuplas como clave
        self.reglas[simbolo_lhs].append((expansion_tupla, probabilidad))

        # Si es una regla lexical (A -> terminal), guardarla aparte
        if len(expansion_rhs) == 1 and expansion_rhs[0] not in self.reglas:
             terminal = expansion_rhs[0]
             self.reglas_lexicales[terminal].append((simbolo_lhs, probabilidad))

    def validar_probabilidades(self):
        """Verifica que las probabilidades para cada LHS sumen aproximadamente 1."""
        for lhs, expansiones in self.reglas.items():
            suma_prob = sum(prob for _, prob in expansiones)
            if abs(suma_prob - 1.0) > 1e-6:
                print(f"Advertencia: Probabilidades para '{lhs}' suman {suma_prob}, no 1.0")

    def generar_oracion(self, simbolo=None):
        """
        Genera oración aleatoria según la gramática (expansión recursiva)
        Args:
            simbolo: símbolo inicial (por defecto self.simbolo_inicial)
        Returns:
            lista de palabras (terminales)
        """
        if simbolo is None:
            simbolo = self.simbolo_inicial

        # Si es terminal (no está a la izquierda de ninguna regla)
        if simbolo not in self.reglas:
            return [simbolo]

        # Elegir expansión según probabilidades
        expansiones_posibles = self.reglas[simbolo]
        expansiones_lista = [exp[0] for exp in expansiones_posibles]
        probs_lista = [exp[1] for exp in expansiones_posibles]
        
        # Manejar caso de suma de probs != 1 si la validación está desactivada
        suma_p = sum(probs_lista)
        if suma_p == 0: return [f"<{simbolo}_ERROR>"] # No se puede expandir
        if abs(suma_p - 1.0) > 1e-6: probs_lista = [p/suma_p for p in probs_lista]
            
        expansion_elegida = random.choices(expansiones_lista, weights=probs_lista, k=1)[0]

        # Expandir recursivamente cada símbolo en la expansión elegida
        resultado_final = []
        for sub_simbolo in expansion_elegida:
            resultado_final.extend(self.generar_oracion(sub_simbolo))

        return resultado_final

    # (probabilidad_oracion y CKY se mueven a sus propias funciones)


def algoritmo_cky(pcfg, oracion):
    """
    Algoritmo CKY (Cocke-Kasami-Younger) para parseo probabilístico
    Asume que la PCFG está en Forma Normal de Chomsky (FNC) o se adapta.
    (A -> B C o A -> terminal)
    Args:
        pcfg: objeto PCFG
        oracion: lista de palabras (tokens)
    Returns:
        probabilidad máxima del parseo de la oración completa (o 0 si no es parseable)
        y la tabla de backpointers para reconstruir el árbol (simplificado).
    """
    n = len(oracion)
    # Tabla[longitud][inicio][simbolo] = probabilidad_maxima
    # Back[longitud][inicio][simbolo] = (split_k, simbolo_B, simbolo_C)
    tabla_prob = [[defaultdict(float) for _ in range(n)] for _ in range(n+1)]
    tabla_back = [[defaultdict(lambda: None) for _ in range(n)] for _ in range(n+1)]

    # --- Inicialización (longitud 1): Reglas A -> terminal ---
    for i in range(n):
        palabra = oracion[i]
        # Buscar reglas A -> palabra
        if palabra in pcfg.reglas_lexicales:
            for simbolo_A, prob in pcfg.reglas_lexicales[palabra]:
                 # Guardar P(A -> palabra)
                 tabla_prob[1][i][simbolo_A] = prob
                 # Backpointer indica que es terminal
                 tabla_back[1][i][simbolo_A] = palabra

    # --- Llenar tabla (bottom-up) ---
    for longitud in range(2, n + 1): # Longitud del span (2 a n)
        for i in range(n - longitud + 1): # Inicio del span (0 a n-longitud)
            j = i + longitud - 1 # Fin del span
            
            # Para cada posible split k (i <= k < j)
            for k in range(i, j):
                # Para cada regla A -> B C
                for simbolo_A, expansiones in pcfg.reglas.items():
                     for expansion, prob_regla in expansiones:
                         if len(expansion) == 2: # Solo reglas binarias A -> B C
                             simbolo_B, simbolo_C = expansion
                             
                             # Obtener P(B -> span i..k) y P(C -> span k+1..j)
                             prob_B = tabla_prob[k - i + 1][i].get(simbolo_B, 0)
                             prob_C = tabla_prob[j - (k + 1) + 1][k + 1].get(simbolo_C, 0)
                             
                             if prob_B > 0 and prob_C > 0:
                                 # Calcular P(A -> span i..j) a través de este split y regla
                                 prob_actual = prob_regla * prob_B * prob_C
                                 
                                 # Si es mejor que la probabilidad actual para A en este span
                                 if prob_actual > tabla_prob[longitud][i][simbolo_A]:
                                     tabla_prob[longitud][i][simbolo_A] = prob_actual
                                     tabla_back[longitud][i][simbolo_A] = (k, simbolo_B, simbolo_C)

    # --- Resultado final ---
    prob_final = tabla_prob[n][0].get(pcfg.simbolo_inicial, 0)
    backpointer_final = tabla_back[n][0].get(pcfg.simbolo_inicial)

    # (La reconstrucción del árbol a partir de backpointers se omite por brevedad)
    return prob_final #, tabla_back # Podrías devolver backpointers para reconstruir

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 40. PCFG y Algoritmo CKY ===\n")

    # Crear una PCFG simple (aproximadamente en FNC)
    pcfg = PCFG(simbolo_inicial='S')
    pcfg.agregar_regla('S', ['NP', 'VP'], 1.0)
    pcfg.agregar_regla('NP', ['Det', 'N'], 0.7)
    pcfg.agregar_regla('NP', ['gato'], 0.15) # A -> terminal
    pcfg.agregar_regla('NP', ['perro'], 0.15)# A -> terminal
    pcfg.agregar_regla('VP', ['V', 'NP'], 0.6)
    pcfg.agregar_regla('VP', ['duerme'], 0.4) # A -> terminal
    pcfg.agregar_regla('Det', ['el'], 1.0)     # A -> terminal
    pcfg.agregar_regla('N', ['gato'], 0.5)     # A -> terminal (duplicado N/NP)
    pcfg.agregar_regla('N', ['perro'], 0.5)    # A -> terminal (duplicado N/NP)
    pcfg.agregar_regla('V', ['come'], 1.0)     # A -> terminal

    pcfg.validar_probabilidades() # Chequear sumas

    # Generar oración
    print("Generación con PCFG:")
    oracion_generada = pcfg.generar_oracion()
    print(f"   Oración generada: {' '.join(oracion_generada)}\n")

    # Parsear con CKY
    print("Parseo con CKY:")
    oracion_parsear = ['el', 'gato', 'duerme']
    # Nota: CKY requiere FNC. Esta gramática no lo es estrictamente (NP->gato, N->gato).
    #       El algoritmo aquí es una adaptación simplificada.
    #       Para que funcione bien, necesitaríamos convertirla a FNC primero.
    
    prob_parseo = algoritmo_cky(pcfg, oracion_parsear)
    
    print(f"   Oración a parsear: {' '.join(oracion_parsear)}")
    print(f"   Probabilidad máxima del parseo (simplificado): {prob_parseo:.4f}")
    # (El resultado puede ser bajo o 0 si la gramática no cubre bien la oración
    #  o no está correctamente en FNC para este CKY simplificado).