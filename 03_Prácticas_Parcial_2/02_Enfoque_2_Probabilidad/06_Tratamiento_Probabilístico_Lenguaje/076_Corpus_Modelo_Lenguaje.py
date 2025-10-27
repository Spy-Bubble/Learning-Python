import math
import re
from collections import Counter

# ============================================================================
# 39. MODELO PROBABILÍSTICO DEL LENGUAJE: CORPUS
# ============================================================================

class Corpus:
    """
    Representa un corpus de texto para modelos de lenguaje
    """
    def __init__(self):
        self.documentos_tokens = [] # Lista de listas de tokens
        self.vocabulario = set()
        self.frecuencias_tokens = Counter()
        self.num_tokens_total = 0

    def tokenizar(self, texto):
        """Tokeniza texto en palabras (minúsculas, solo alfanuméricos)"""
        texto = texto.lower()
        # Encuentra secuencias de caracteres alfanuméricos
        tokens = re.findall(r'\b\w+\b', texto)
        return tokens

    def agregar_documento(self, texto):
        """Agrega un documento al corpus"""
        tokens = self.tokenizar(texto)
        if not tokens: return # No agregar documentos vacíos

        self.documentos_tokens.append(tokens)
        self.vocabulario.update(tokens)
        self.frecuencias_tokens.update(tokens)
        self.num_tokens_total += len(tokens)

    def estadisticas(self):
        """Retorna estadísticas del corpus"""
        return {
            'num_documentos': len(self.documentos_tokens),
            'tam_vocabulario': len(self.vocabulario),
            'num_tokens_total': self.num_tokens_total,
            'num_tokens_unicos': len(self.frecuencias_tokens)
        }


def modelo_unigramas(corpus):
    """
    Crea modelo de lenguaje de unigramas P(palabra)
    Args:
        corpus: objeto Corpus
    Returns:
        dict {palabra: probabilidad}
    """
    total_tokens = corpus.num_tokens_total
    if total_tokens == 0:
        return {}

    probabilidades = {}
    for palabra, freq in corpus.frecuencias_tokens.items():
        probabilidades[palabra] = freq / total_tokens

    return probabilidades


def perplexity(modelo_unigrama, texto_prueba, corpus, oov_prob=1e-6):
    """
    Calcula perplejidad de un modelo de unigramas sobre un texto de prueba.
    (Menor perplejidad es mejor).
    Args:
        modelo_unigrama: dict {palabra: probabilidad}
        texto_prueba: string del texto a evaluar
        corpus: objeto Corpus (usado para tokenizar igual)
        oov_prob: probabilidad asignada a palabras fuera de vocabulario (OOV)
    Returns:
        perplejidad
    """
    tokens = corpus.tokenizar(texto_prueba)
    N = len(tokens)
    if N == 0:
        return float('inf') # Perplejidad infinita para texto vacío

    log_prob_total = 0
    for token in tokens:
        # Usar probabilidad OOV si la palabra no está en el modelo
        prob = modelo_unigrama.get(token, oov_prob)
        # Evitar log(0) si oov_prob es 0 o negativo
        if prob <= 0:
             prob = 1e-10
        log_prob_total += math.log(prob)

    # Perplejidad = exp(- (1/N) * Suma(log P(token_i)))
    #             = ( Producto( P(token_i) ) ) ^ (-1/N)
    cross_entropy = -log_prob_total / N
    perplexity_val = math.exp(cross_entropy)
    return perplexity_val

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 39. Corpus y Modelo de Lenguaje (Unigramas) ===\n")

    # Crear y poblar corpus
    corpus = Corpus()
    corpus.agregar_documento("el gato come pescado")
    corpus.agregar_documento("el perro come carne")
    corpus.agregar_documento("el gato duerme mucho")

    # Mostrar estadísticas
    stats = corpus.estadisticas()
    print(f"   Estadísticas del corpus:")
    for k, v in stats.items():
        print(f"      {k}: {v}")

    # Crear modelo de unigramas
    modelo_uni = modelo_unigramas(corpus)
    print(f"\n   Probabilidades (Unigramas):")
    # Ordenar por probabilidad descendente
    top_palabras = sorted(modelo_uni.items(), key=lambda item: item[1], reverse=True)
    for palabra, prob in top_palabras:
        print(f"      P('{palabra}') = {prob:.3f}")

    # Calcular perplejidad
    texto_eval = "el perro duerme"
    perp = perplexity(modelo_uni, texto_eval, corpus)
    print(f"\n   Perplejidad del modelo en '{texto_eval}': {perp:.2f}")