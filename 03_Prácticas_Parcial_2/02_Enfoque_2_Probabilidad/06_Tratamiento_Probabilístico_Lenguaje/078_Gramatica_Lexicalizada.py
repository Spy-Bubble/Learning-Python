import random
from collections import defaultdict

# ============================================================================
# 41. GRAMÁTICAS PROBABILÍSTICAS LEXICALIZADAS
# ============================================================================

class GramaticaLexicalizada:
    """
    Gramática probabilística lexicalizada (simplificada)
    Cada regla A(cabeza_A) -> B(cabeza_B) C(cabeza_C) tiene palabras cabeza asociadas.
    """
    def __init__(self):
        # { (LHS_simbolo, cabeza_LHS): [(expansion_tupla, probabilidad)] }
        # expansion_tupla = ((simbolo_RHS1, cabeza_RHS1), (simbolo_RHS2, cabeza_RHS2), ...)
        self.reglas = defaultdict(list)
        self.simbolo_inicial = 'S' # Asumir un símbolo inicial

    def agregar_regla(self, simbolo_lhs, cabeza_lhs, expansion_rhs, probabilidad):
        """
        Agrega regla lexicalizada A(h_a) -> B(h_b) C(h_c) [prob]
        Args:
            simbolo_lhs: no terminal (ej: 'VP')
            cabeza_lhs: palabra cabeza (ej: 'comer')
            expansion_rhs: lista de tuplas [(símbolo, cabeza), ...]
                           o lista de [palabra_terminal] para reglas A(h) -> h
            probabilidad: P(expansion | simbolo_lhs, cabeza_lhs)
        """
        clave = (simbolo_lhs, cabeza_lhs)
        # Convertir expansión a tupla para consistencia
        expansion_tupla = tuple(expansion_rhs)
        self.reglas[clave].append((expansion_tupla, probabilidad))

    def generar_con_cabeza(self, simbolo, cabeza):
        """Genera expansión (lista de palabras) dada una cabeza lexical"""
        clave = (simbolo, cabeza)

        # Si la clave no está (o si la cabeza es el único elemento) -> terminal
        if clave not in self.reglas:
            # Asumimos que si no hay regla, la cabeza es la palabra terminal
            return [cabeza]

        # Elegir una expansión basada en probabilidades
        expansiones_posibles = self.reglas[clave]
        expansiones_lista = [exp[0] for exp in expansiones_posibles]
        probs_lista = [exp[1] for exp in expansiones_posibles]

        suma_p = sum(probs_lista)
        if suma_p == 0: return [f"<{simbolo}({cabeza})_ERROR>"]
        if abs(suma_p - 1.0) > 1e-6: probs_lista = [p/suma_p for p in probs_lista]

        expansion_elegida = random.choices(expansiones_lista, weights=probs_lista, k=1)[0]

        # Expandir recursivamente
        resultado_final = []
        # Verificar si la expansión es de terminales o no terminales
        if expansion_elegida and isinstance(expansion_elegida[0], tuple):
             # Es una expansión de (símbolo, cabeza)
             for sub_simbolo, sub_cabeza in expansion_elegida:
                 resultado_final.extend(self.generar_con_cabeza(sub_simbolo, sub_cabeza))
        else:
             # Es una expansión directa a terminales (ej: A(h) -> h)
             resultado_final.extend(expansion_elegida)


        return resultado_final

    def generar_oracion(self, simbolo_inicial_cabeza=None):
         """Genera una oración completa (requiere regla inicial con cabeza)"""
         # Necesitamos saber la cabeza inicial para empezar
         # Esto es una simplificación, la generación podría ser más compleja
         if simbolo_inicial_cabeza:
             return self.generar_con_cabeza(self.simbolo_inicial, simbolo_inicial_cabeza)
         else:
             # Buscar una regla S(cabeza) -> ... y elegir una al azar
             reglas_s = [k for k in self.reglas if k[0] == self.simbolo_inicial]
             if not reglas_s: return ["<ERROR_NO_S_RULE>"]
             simbolo, cabeza_inicial = random.choice(reglas_s)
             print(f"   (Iniciando generación con cabeza: {cabeza_inicial})")
             return self.generar_con_cabeza(simbolo, cabeza_inicial)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 41. Gramáticas Probabilísticas Lexicalizadas ===\n")

    gramatica_lex = GramaticaLexicalizada()
    gramatica_lex.simbolo_inicial = 'S'

    # S(ver) -> NP(Juan) VP(ver) [1.0]
    gramatica_lex.agregar_regla('S', 'ver', [('NP', 'Juan'), ('VP', 'ver')], 1.0)

    # VP(ver) -> V(ver) NP(película) [0.8]
    gramatica_lex.agregar_regla('VP', 'ver', [('V', 'ver'), ('NP', 'película')], 0.8)
    # VP(ver) -> V(ver) [0.2]
    gramatica_lex.agregar_regla('VP', 'ver', [('V', 'ver')], 0.2)

    # NP(Juan) -> N(Juan) [1.0] (Regla A(h) -> h implícita si no se define)
    # NP(película) -> Det(la) N(película) [1.0]
    gramatica_lex.agregar_regla('NP', 'película', [('Det', 'la'), ('N', 'película')], 1.0)

    # Reglas terminales implícitas (V(ver)->'ver', N(Juan)->'Juan', etc.)

    print("Generando oración con gramática lexicalizada:")
    # Necesitamos especificar una cabeza inicial para 'S' o modificar generar_oracion
    oracion = gramatica_lex.generar_oracion(simbolo_inicial_cabeza='ver')
    print(f"   Oración generada: {' '.join(oracion)}")

    # Ejemplo de estructura esperada de reglas:
    # print("\nEstructura interna de reglas:")
    # print(gramatica_lex.reglas)