import math
import re
from collections import Counter

# ============================================================================
# 42. RECUPERACIÓN DE DATOS (Modelo Vectorial TF-IDF)
# ============================================================================

class ModeloVectorial:
    """
    Modelo vectorial simple para recuperación de información usando TF-IDF.
    """
    def __init__(self):
        self.documentos = {} # {doc_id: lista_tokens}
        self.vocabulario = set()
        self.idf = {}       # Inverse Document Frequency {termino: idf_score}
        self._idf_calculado = False

    def tokenizar(self, texto):
        """Tokeniza y normaliza texto (minúsculas, alfanumérico)"""
        texto = texto.lower()
        # Encuentra secuencias de caracteres alfanuméricos
        tokens = re.findall(r'\b\w+\b', texto)
        # Opcional: añadir stemming o lematización aquí
        return tokens

    def agregar_documento(self, doc_id, texto):
        """Agrega documento al índice"""
        tokens = self.tokenizar(texto)
        if not tokens: return # No agregar documentos vacíos
        
        if doc_id in self.documentos:
             print(f"Advertencia: Sobrescribiendo documento con ID '{doc_id}'")

        self.documentos[doc_id] = tokens
        self.vocabulario.update(tokens)
        self._idf_calculado = False # Marcar IDF como obsoleto

    def calcular_idf(self):
        """Calcula IDF para cada término en el vocabulario."""
        N = len(self.documentos) # Número total de documentos
        if N == 0: return

        # Contar en cuántos documentos aparece cada término (DF - Document Frequency)
        df = Counter()
        for doc_id, tokens in self.documentos.items():
            df.update(set(tokens)) # Usar set para contar solo una vez por documento

        # Calcular IDF = log(N / (df + 1)) (usar +1 para suavizado)
        self.idf = {}
        for termino in self.vocabulario:
            df_termino = df.get(termino, 0)
            self.idf[termino] = math.log(N / (df_termino + 1.0)) # Usar log natural

        self._idf_calculado = True

    def vector_tfidf(self, tokens):
        """
        Calcula el vector TF-IDF para una lista de tokens (documento o consulta).
        Args:
            tokens: lista de términos
        Returns:
            dict {término: peso_tfidf}
        """
        if not self._idf_calculado:
            self.calcular_idf() # Asegurarse que IDF esté calculado

        n_tokens_doc = len(tokens)
        if n_tokens_doc == 0: return {}

        # TF (Term Frequency) - Frecuencia normalizada
        tf = Counter(tokens)
        tf_norm = {termino: freq / n_tokens_doc for termino, freq in tf.items()}

        # Calcular TF-IDF
        vector = {}
        norma = 0.0 # Para normalización L2 (opcional pero común)
        for termino, tf_val in tf_norm.items():
            idf_val = self.idf.get(termino, 0) # IDF es 0 si no está en vocabulario
            tfidf_val = tf_val * idf_val
            vector[termino] = tfidf_val
            norma += tfidf_val ** 2

        # Normalizar vector (L2 norm) - opcional
        norma = math.sqrt(norma)
        if norma > 0:
            vector = {termino: val / norma for termino, val in vector.items()}

        return vector

    def similitud_coseno(self, vec1, vec2):
        """Calcula similitud coseno entre dos vectores TF-IDF (dicts)."""
        # Intersección de términos
        terminos_comunes = set(vec1.keys()) & set(vec2.keys())

        # Producto punto
        producto_punto = sum(vec1[t] * vec2[t] for t in terminos_comunes)

        # Magnitudes (Normas L2) - Si los vectores ya están normalizados, esto es 1
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))

        # Evitar división por cero
        if mag1 == 0 or mag2 == 0:
            return 0.0

        return producto_punto / (mag1 * mag2)

    def buscar(self, consulta, top_k=5):
        """
        Busca documentos relevantes para una consulta usando similitud coseno.
        Args:
            consulta: texto de consulta (string)
            top_k: número máximo de resultados a devolver
        Returns:
            lista ordenada de (doc_id, score_similitud)
        """
        if not self.documentos: return []

        # Calcular IDF si no está actualizado
        if not self._idf_calculado:
            self.calcular_idf()

        # Vectorizar la consulta
        tokens_consulta = self.tokenizar(consulta)
        vec_consulta = self.vector_tfidf(tokens_consulta)

        # Calcular similitud con cada documento
        scores = []
        for doc_id, tokens_doc in self.documentos.items():
            vec_doc = self.vector_tfidf(tokens_doc) # TF-IDF del documento
            similitud = self.similitud_coseno(vec_consulta, vec_doc)
            if similitud > 0: # Solo considerar documentos con alguna similitud
                scores.append((doc_id, similitud))

        # Ordenar por score descendente
        scores.sort(key=lambda item: item[1], reverse=True)

        return scores[:top_k]

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 42. Recuperación de Información (TF-IDF y Coseno) ===\n")

    modelo_vec = ModeloVectorial()
    modelo_vec.agregar_documento("doc1", "el gato negro come pescado fresco y bueno")
    modelo_vec.agregar_documento("doc2", "el perro marrón come carne jugosa")
    modelo_vec.agregar_documento("doc3", "el gato blanco duerme en el sofá cómodo")
    modelo_vec.agregar_documento("doc4", "pescado fresco para el gato")

    # Calcular IDF (se hace automáticamente en buscar, pero podemos verlo)
    modelo_vec.calcular_idf()
    print("   IDF (Inverse Document Frequency) calculado para términos:")
    # print(modelo_vec.idf) # Descomentar para ver todos los IDFs

    # Realizar una búsqueda
    consulta = "gato come pescado"
    resultados = modelo_vec.buscar(consulta, top_k=3)

    print(f"\n   Consulta: '{consulta}'")
    print(f"   Resultados (Top {len(resultados)}):")
    for doc_id, score in resultados:
        print(f"      Documento '{doc_id}': Similitud = {score:.4f}")

    # Ver vector TF-IDF de un documento
    # vec_doc1 = modelo_vec.vector_tfidf(modelo_vec.documentos['doc1'])
    # print("\n   Vector TF-IDF (normalizado) para doc1:")
    # for term, weight in sorted(vec_doc1.items()): print(f"      '{term}': {weight:.3f}")