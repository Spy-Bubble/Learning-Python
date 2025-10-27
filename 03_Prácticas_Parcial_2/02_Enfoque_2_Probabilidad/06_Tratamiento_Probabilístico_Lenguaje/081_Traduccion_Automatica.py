import random
import math
from collections import defaultdict, Counter

# ============================================================================
# 44. TRADUCCIÓN AUTOMÁTICA ESTADÍSTICA (SMT) - Simplificado
# ============================================================================

class ModeloTraduccionSimple:
    """
    Modelo simple de traducción estadística (SMT) basado en tabla de frases
    y modelo de lenguaje unigrama para el destino.
    """
    def __init__(self):
        # {frase_origen_tuple: [(frase_destino_tuple, prob_t), ...]}
        self.tabla_traduccion_frase = defaultdict(list)
        # {palabra_destino: prob_lm}
        self.modelo_lenguaje_destino = defaultdict(lambda: 1e-6) # Prob por defecto baja
        self.max_long_frase = 1 # Longitud máxima de frase a considerar

    def _tokenizar(self, texto):
        # Simple split, podría mejorarse
        return tuple(texto.lower().split())

    def entrenar(self, corpus_paralelo, max_long_frase=3):
        """
        Entrena modelos de traducción y lenguaje desde un corpus paralelo.
        Args:
            corpus_paralelo: lista de tuplas (oracion_origen_str, oracion_destino_str)
            max_long_frase: longitud máxima de frase a extraer
        """
        self.max_long_frase = max_long_frase
        
        conteos_frase = defaultdict(lambda: defaultdict(int))
        conteos_origen = defaultdict(int)
        corpus_destino_tokens = []

        print(f"   (SMT: Extrayendo frases hasta longitud {max_long_frase}...)")
        # --- Extracción y conteo de frases (simplificado, sin alineamiento real) ---
        for oracion_orig_str, oracion_dest_str in corpus_paralelo:
            tokens_orig = self._tokenizar(oracion_orig_str)
            tokens_dest = self._tokenizar(oracion_dest_str)
            corpus_destino_tokens.extend(tokens_dest)

            # Extraer todas las sub-frases y asumir que se alinean 1:1 (muy simplista)
            len_o, len_d = len(tokens_orig), len(tokens_dest)
            for l in range(1, self.max_long_frase + 1):
                if l <= len_o and l <= len_d: # Simplificación: misma longitud
                    for i in range(len_o - l + 1):
                         frase_o = tuple(tokens_orig[i:i+l])
                         # Asumir alineamiento simple con la frase en la misma posición
                         if i < len_d - l + 1:
                              frase_d = tuple(tokens_dest[i:i+l])
                              conteos_frase[frase_o][frase_d] += 1
                              conteos_origen[frase_o] += 1

        # --- Calcular probabilidades de traducción P(destino | origen) ---
        print("   (SMT: Calculando probabilidades de traducción...)")
        self.tabla_traduccion_frase = defaultdict(list)
        for frase_o, traducciones in conteos_frase.items():
            total_o = conteos_origen[frase_o]
            if total_o > 0:
                lista_probs = []
                for frase_d, count in traducciones.items():
                    prob_t = count / total_o
                    lista_probs.append((frase_d, prob_t))
                # Ordenar por probabilidad descendente
                lista_probs.sort(key=lambda x: x[1], reverse=True)
                self.tabla_traduccion_frase[frase_o] = lista_probs

        # --- Calcular modelo de lenguaje (unigrama) del idioma destino ---
        print("   (SMT: Calculando modelo de lenguaje destino...)")
        total_tokens_dest = len(corpus_destino_tokens)
        if total_tokens_dest > 0:
            freq_dest = Counter(corpus_destino_tokens)
            self.modelo_lenguaje_destino = defaultdict(lambda: 1e-6) # Suavizado
            for palabra, count in freq_dest.items():
                self.modelo_lenguaje_destino[palabra] = count / total_tokens_dest

    def _score_traduccion(self, traduccion_tokens):
        """Puntúa una traducción usando el modelo de lenguaje (log prob)"""
        score = 0.0
        for token in traduccion_tokens:
            prob = self.modelo_lenguaje_destino[token] # Usa prob suavizada
            score += math.log(prob)
        return score

    def traducir_oracion_decodificador_simple(self, oracion_origen_str):
        """
        Traduce usando la mejor opción de frase localmente (decodificador voraz).
        Args:
            oracion_origen_str: texto en idioma origen
        Returns:
            traducción (string)
        """
        tokens_origen = self._tokenizar(oracion_origen_str)
        traduccion_tokens = []
        i = 0
        n = len(tokens_origen)

        while i < n:
            mejor_traduccion_local = None
            mejor_longitud = 0
            
            # Intentar encontrar la frase más larga posible que coincida
            for longitud in range(min(self.max_long_frase, n - i), 0, -1):
                frase_o = tuple(tokens_origen[i : i + longitud])
                if frase_o in self.tabla_traduccion_frase:
                    # Tomar la traducción más probable para esta frase
                    mejor_traduccion_local = self.tabla_traduccion_frase[frase_o][0][0]
                    mejor_longitud = longitud
                    break # Encontrada la más larga, usarla

            if mejor_traduccion_local:
                traduccion_tokens.extend(mejor_traduccion_local)
                i += mejor_longitud
            else:
                # Palabra desconocida o frase no encontrada, mantener original (o <UNK>)
                traduccion_tokens.append(tokens_origen[i])
                i += 1

        return ' '.join(traduccion_tokens)

    # (Beam Search es más complejo y se omite la implementación completa)
    def decodificar_beam_search(self, oracion_origen_str, beam_width=3):
         """Decodificación con Beam Search (Conceptual)"""
         print(f"   (Beam Search para '{oracion_origen_str}' - Conceptual)")
         # 1. Iniciar con hipótesis vacía.
         # 2. Expandir cada hipótesis generando posibles siguientes frases/traducciones.
         # 3. Calcular score (log P_trad + log P_lm).
         # 4. Mantener solo las 'beam_width' mejores hipótesis.
         # 5. Repetir hasta cubrir toda la oración origen.
         # 6. Devolver la mejor hipótesis completa.
         # (Implementación requiere manejar estados, scores acumulados, etc.)
         
         # Devolver resultado del decodificador simple como placeholder
         return self.traducir_oracion_decodificador_simple(oracion_origen_str)


def alineamiento_palabra_simple(tokens_origen, tokens_destino):
    """
    Alineamiento simple 1:1 basado en orden (muy básico).
    Args:
        tokens_origen: lista de palabras
        tokens_destino: lista de palabras
    Returns:
        lista de tuplas de índices alineados (idx_origen, idx_destino)
    """
    alineamientos = []
    len_o, len_d = len(tokens_origen), len(tokens_destino)
    
    # Asumir alineamiento monótono simple
    ptr_o, ptr_d = 0, 0
    while ptr_o < len_o and ptr_d < len_d:
         alineamientos.append((ptr_o, ptr_d))
         ptr_o += 1
         ptr_d += 1
         # Podrían añadirse heurísticas más complejas
         
    return alineamientos


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 44. Traducción Automática Estadística (SMT Simple) ===\n")

    traductor = ModeloTraduccionSimple()

    # Corpus paralelo muy pequeño (Inglés -> Español)
    corpus_par = [
        ("hello world", "hola mundo"),
        ("hello friend", "hola amigo"),
        ("world", "mundo"),
        ("goodbye friend", "adiós amigo"),
        ("good morning", "buenos días"),
        ("good day", "buen día"),
        ("hello", "hola"),
    ]

    print("Entrenando modelo SMT...")
    traductor.entrenar(corpus_par, max_long_frase=2)
    print("Entrenamiento completado.\n")

    # Ver parte de la tabla de frases
    # print("Tabla de traducción (ejemplo):")
    # print(traductor.tabla_traduccion_frase.get(('hello',)))
    # print(traductor.tabla_traduccion_frase.get(('good',)))

    # Traducir
    oracion_en = "hello world good day"
    traduccion_es = traductor.traducir_oracion_decodificador_simple(oracion_en)

    print(f"   Inglés: '{oracion_en}'")
    print(f"   Español (Decodificador Simple): '{traduccion_es}'\n")

    # Beam Search (conceptual)
    traduccion_beam = traductor.decodificar_beam_search(oracion_en, beam_width=2)
    print(f"   Español (Beam Search Conceptual): '{traduccion_beam}'\n")

    # Alineamiento
    print("Alineamiento Simple:")
    tokens_o = ['hello', 'world']
    tokens_d = ['hola', 'mundo']
    alineado = alineamiento_palabra_simple(tokens_o, tokens_d)
    print(f"   Origen: {tokens_o}")
    print(f"   Destino: {tokens_d}")
    print(f"   Alineamiento (índices): {alineado}")