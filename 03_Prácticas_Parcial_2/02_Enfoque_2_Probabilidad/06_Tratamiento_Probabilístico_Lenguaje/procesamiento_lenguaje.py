"""
TRATAMIENTO PROBABILÍSTICO DEL LENGUAJE
Algoritmos 39-44: Modelos de lenguaje, gramáticas, recuperación de información
"""

import random
import math
from collections import defaultdict, Counter
import re

# ============================================================================
# 39. MODELO PROBABILÍSTICO DEL LENGUAJE: CORPUS
# ============================================================================

class Corpus:
    """
    Representa un corpus de texto
    """
    def __init__(self):
        self.documentos = []
        self.vocabulario = set()
        self.frecuencias = Counter()
    
    def agregar_documento(self, texto):
        """Agrega un documento al corpus"""
        tokens = self.tokenizar(texto)
        self.documentos.append(tokens)
        self.vocabulario.update(tokens)
        self.frecuencias.update(tokens)
    
    def tokenizar(self, texto):
        """Tokeniza texto en palabras"""
        # Convertir a minúsculas y dividir por espacios/puntuación
        texto = texto.lower()
        tokens = re.findall(r'\b\w+\b', texto)
        return tokens
    
    def estadisticas(self):
        """Retorna estadísticas del corpus"""
        num_tokens = sum(len(doc) for doc in self.documentos)
        return {
            'documentos': len(self.documentos),
            'vocabulario': len(self.vocabulario),
            'tokens_totales': num_tokens,
            'palabras_unicas': len(self.frecuencias)
        }


def modelo_unigramas(corpus):
    """
    Crea modelo de lenguaje de unigramas P(palabra)
    Args:
        corpus: objeto Corpus
    Returns:
        dict {palabra: probabilidad}
    """
    total = sum(corpus.frecuencias.values())
    
    probabilidades = {}
    for palabra, freq in corpus.frecuencias.items():
        probabilidades[palabra] = freq / total
    
    return probabilidades


def perplexity(modelo, texto_prueba, corpus):
    """
    Calcula perplejidad del modelo (medida de qué tan bien predice)
    Args:
        modelo: dict de probabilidades
        texto_prueba: texto a evaluar
        corpus: corpus para tokenizar
    Returns:
        perplejidad (menor es mejor)
    """
    tokens = corpus.tokenizar(texto_prueba)
    N = len(tokens)
    
    log_prob_total = 0
    for token in tokens:
        prob = modelo.get(token, 1e-10)  # Suavizado simple
        log_prob_total += math.log(prob)
    
    perplexity = math.exp(-log_prob_total / N)
    return perplexity


# ============================================================================
# 40. GRAMÁTICAS PROBABILÍSTICAS INDEPENDIENTES DEL CONTEXTO (PCFG)
# ============================================================================

class PCFG:
    """
    Probabilistic Context-Free Grammar
    """
    def __init__(self):
        self.reglas = defaultdict(list)  # {símbolo: [(expansión, probabilidad)]}
        self.simbolo_inicial = 'S'
    
    def agregar_regla(self, simbolo, expansion, probabilidad):
        """
        Agrega una regla de producción
        Args:
            simbolo: símbolo no terminal (ej: 'S', 'NP')
            expansion: lista de símbolos (ej: ['NP', 'VP'])
            probabilidad: P(expansión|símbolo)
        """
        self.reglas[simbolo].append((expansion, probabilidad))
    
    def generar_oracion(self, simbolo=None):
        """
        Genera oración aleatoria según la gramática
        Args:
            simbolo: símbolo inicial (por defecto S)
        Returns:
            lista de palabras
        """
        if simbolo is None:
            simbolo = self.simbolo_inicial
        
        # Si es terminal (palabra), retornar
        if simbolo not in self.reglas:
            return [simbolo]
        
        # Elegir expansión según probabilidades
        expansiones = self.reglas[simbolo]
        expansion, _ = random.choices(expansiones, 
                                     weights=[p for _, p in expansiones])[0]
        
        # Expandir recursivamente
        resultado = []
        for sub_simbolo in expansion:
            resultado.extend(self.generar_oracion(sub_simbolo))
        
        return resultado
    
    def probabilidad_oracion(self, arbol_parseado):
        """
        Calcula probabilidad de un árbol de parseo
        Args:
            arbol_parseado: estructura (símbolo, hijos)
        Returns:
            probabilidad
        """
        simbolo, hijos = arbol_parseado
        
        # Si es terminal
        if not hijos:
            return 1.0
        
        # Buscar regla correspondiente
        expansion = [h[0] if isinstance(h, tuple) else h for h in hijos]
        
        prob_regla = 0
        for exp, p in self.reglas[simbolo]:
            if exp == expansion:
                prob_regla = p
                break
        
        # Multiplicar por probabilidades de subárboles
        prob_total = prob_regla
        for hijo in hijos:
            if isinstance(hijo, tuple):
                prob_total *= self.probabilidad_oracion(hijo)
        
        return prob_total


def algoritmo_cky(pcfg, oracion):
    """
    Algoritmo CKY para parseo probabilístico
    Args:
        pcfg: gramática PCFG
        oracion: lista de palabras
    Returns:
        probabilidad máxima y árbol de parseo
    """
    n = len(oracion)
    # Tabla dinámica: tabla[i][j][simbolo] = (prob, backpointer)
    tabla = [[{} for _ in range(n)] for _ in range(n)]
    
    # Llenar diagonal (palabras individuales)
    for i in range(n):
        palabra = oracion[i]
        for simbolo, expansiones in pcfg.reglas.items():
            for expansion, prob in expansiones:
                if expansion == [palabra]:
                    tabla[i][i][simbolo] = (prob, None)
    
    # Llenar tabla (bottom-up)
    for longitud in range(2, n + 1):
        for i in range(n - longitud + 1):
            j = i + longitud - 1
            
            for simbolo, expansiones in pcfg.reglas.items():
                mejor_prob = 0
                mejor_split = None
                
                for expansion, prob_regla in expansiones:
                    if len(expansion) == 2:
                        B, C = expansion
                        
                        # Probar todos los splits
                        for k in range(i, j):
                            if B in tabla[i][k] and C in tabla[k+1][j]:
                                prob_B = tabla[i][k][B][0]
                                prob_C = tabla[k+1][j][C][0]
                                prob_total = prob_regla * prob_B * prob_C
                                
                                if prob_total > mejor_prob:
                                    mejor_prob = prob_total
                                    mejor_split = (k, B, C)
                
                if mejor_prob > 0:
                    tabla[i][j][simbolo] = (mejor_prob, mejor_split)
    
    # Retornar resultado para símbolo inicial
    if pcfg.simbolo_inicial in tabla[0][n-1]:
        return tabla[0][n-1][pcfg.simbolo_inicial]
    
    return (0, None)


# ============================================================================
# 41. GRAMÁTICAS PROBABILÍSTICAS LEXICALIZADAS
# ============================================================================

class GramaticaLexicalizada:
    """
    Gramática probabilística lexicalizada (cada regla tiene palabra cabeza)
    """
    def __init__(self):
        self.reglas = defaultdict(list)
    
    def agregar_regla(self, simbolo, cabeza, expansion, probabilidad):
        """
        Agrega regla lexicalizada
        Args:
            simbolo: no terminal (ej: 'VP')
            cabeza: palabra cabeza (ej: 'comer')
            expansion: [(símbolo, cabeza), ...]
            probabilidad: P(regla|símbolo, cabeza)
        """
        clave = (simbolo, cabeza)
        self.reglas[clave].append((expansion, probabilidad))
    
    def generar_con_cabeza(self, simbolo, cabeza):
        """Genera expansión dada cabeza lexical"""
        clave = (simbolo, cabeza)
        
        if clave not in self.reglas:
            return [cabeza]
        
        expansiones = self.reglas[clave]
        expansion, _ = random.choices(expansiones,
                                     weights=[p for _, p in expansiones])[0]
        
        resultado = []
        for sub_simbolo, sub_cabeza in expansion:
            resultado.extend(self.generar_con_cabeza(sub_simbolo, sub_cabeza))
        
        return resultado


# ============================================================================
# 42. RECUPERACIÓN DE DATOS
# ============================================================================

class ModeloVectorial:
    """
    Modelo vectorial para recuperación de información
    """
    def __init__(self):
        self.documentos = []
        self.vocabulario = set()
        self.idf = {}  # Inverse Document Frequency
    
    def agregar_documento(self, doc_id, texto):
        """Agrega documento al índice"""
        tokens = self.tokenizar(texto)
        self.documentos.append((doc_id, tokens))
        self.vocabulario.update(tokens)
    
    def tokenizar(self, texto):
        """Tokeniza y normaliza texto"""
        texto = texto.lower()
        return re.findall(r'\b\w+\b', texto)
    
    def calcular_idf(self):
        """Calcula IDF para cada término"""
        N = len(self.documentos)
        
        # Contar en cuántos documentos aparece cada término
        df = Counter()
        for _, tokens in self.documentos:
            df.update(set(tokens))
        
        # Calcular IDF
        for termino in self.vocabulario:
            self.idf[termino] = math.log(N / (df[termino] + 1))
    
    def vector_tfidf(self, tokens):
        """
        Calcula vector TF-IDF
        Args:
            tokens: lista de términos
        Returns:
            dict {término: peso_tfidf}
        """
        # TF (Term Frequency)
        tf = Counter(tokens)
        total_terms = len(tokens)
        
        # TF-IDF
        vector = {}
        for termino, freq in tf.items():
            tf_norm = freq / total_terms
            idf = self.idf.get(termino, 0)
            vector[termino] = tf_norm * idf
        
        return vector
    
    def similitud_coseno(self, vec1, vec2):
        """Calcula similitud coseno entre dos vectores"""
        # Producto punto
        producto = sum(vec1.get(t, 0) * vec2.get(t, 0) 
                      for t in set(vec1.keys()) | set(vec2.keys()))
        
        # Magnitudes
        mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        return producto / (mag1 * mag2)
    
    def buscar(self, consulta, top_k=5):
        """
        Busca documentos relevantes
        Args:
            consulta: texto de consulta
            top_k: número de resultados
        Returns:
            lista de (doc_id, score)
        """
        self.calcular_idf()
        
        # Vector de consulta
        tokens_consulta = self.tokenizar(consulta)
        vec_consulta = self.vector_tfidf(tokens_consulta)
        
        # Calcular similitud con cada documento
        scores = []
        for doc_id, tokens in self.documentos:
            vec_doc = self.vector_tfidf(tokens)
            similitud = self.similitud_coseno(vec_consulta, vec_doc)
            scores.append((doc_id, similitud))
        
        # Ordenar por score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores[:top_k]


# ============================================================================
# 43. EXTRACCIÓN DE INFORMACIÓN
# ============================================================================

def extraccion_entidades_patrones(texto, patrones):
    """
    Extracción de entidades usando patrones regex
    Args:
        texto: texto a analizar
        patrones: dict {tipo_entidad: regex_pattern}
    Returns:
        dict {tipo: [entidades_encontradas]}
    """
    entidades = defaultdict(list)
    
    for tipo, patron in patrones.items():
        matches = re.finditer(patron, texto, re.IGNORECASE)
        for match in matches:
            entidades[tipo].append(match.group())
    
    return dict(entidades)


def extraccion_relaciones(texto, patrones_relacion):
    """
    Extrae relaciones entre entidades
    Args:
        texto: texto a analizar
        patrones_relacion: lista de (patrón, tipo_relación)
    Returns:
        lista de tuplas (sujeto, relación, objeto)
    """
    relaciones = []
    
    for patron, tipo_rel in patrones_relacion:
        matches = re.finditer(patron, texto)
        for match in matches:
            grupos = match.groups()
            if len(grupos) >= 2:
                relaciones.append((grupos[0], tipo_rel, grupos[1]))
    
    return relaciones


class ExtractorNER:
    """
    Extractor simple de Entidades Nombradas (NER)
    """
    def __init__(self):
        # Diccionarios de entidades conocidas
        self.personas = set()
        self.lugares = set()
        self.organizaciones = set()
    
    def entrenar(self, textos_anotados):
        """
        Entrena con textos anotados
        Args:
            textos_anotados: lista de (texto, anotaciones)
        """
        for texto, anotaciones in textos_anotados:
            for tipo, entidad in anotaciones:
                if tipo == 'PERSONA':
                    self.personas.add(entidad.lower())
                elif tipo == 'LUGAR':
                    self.lugares.add(entidad.lower())
                elif tipo == 'ORGANIZACION':
                    self.organizaciones.add(entidad.lower())
    
    def extraer(self, texto):
        """Extrae entidades de texto nuevo"""
        palabras = texto.split()
        entidades = []
        
        for palabra in palabras:
            palabra_lower = palabra.lower()
            
            if palabra_lower in self.personas:
                entidades.append(('PERSONA', palabra))
            elif palabra_lower in self.lugares:
                entidades.append(('LUGAR', palabra))
            elif palabra_lower in self.organizaciones:
                entidades.append(('ORGANIZACION', palabra))
            # Heurísticas adicionales
            elif palabra[0].isupper() and len(palabra) > 1:
                # Palabra capitalizada puede ser entidad
                entidades.append(('POSIBLE_ENTIDAD', palabra))
        
        return entidades


# ============================================================================
# 44. TRADUCCIÓN AUTOMÁTICA ESTADÍSTICA
# ============================================================================

class ModeloTraduccion:
    """
    Modelo simple de traducción estadística basado en tabla de frases
    """
    def __init__(self):
        self.tabla_traduccion = {}  # {frase_origen: [(frase_destino, prob)]}
        self.modelo_lenguaje = {}  # Unigramas del idioma destino
    
    def entrenar(self, corpus_paralelo):
        """
        Entrena con corpus paralelo
        Args:
            corpus_paralelo: lista de (frase_origen, frase_destino)
        """
        # Construir tabla de traducción
        conteos = defaultdict(lambda: defaultdict(int))
        
        for frase_orig, frase_dest in corpus_paralelo:
            conteos[frase_orig][frase_dest] += 1
        
        # Calcular probabilidades
        for frase_orig, traducciones in conteos.items():
            total = sum(traducciones.values())
            self.tabla_traduccion[frase_orig] = [
                (frase_dest, count / total)
                for frase_dest, count in traducciones.items()
            ]
            # Ordenar por probabilidad
            self.tabla_traduccion[frase_orig].sort(key=lambda x: x[1], reverse=True)
        
        # Modelo de lenguaje del destino
        todas_dest = [dest for _, dest in corpus_paralelo]
        total_frases = len(todas_dest)
        freq_dest = Counter(todas_dest)
        self.modelo_lenguaje = {f: c/total_frases for f, c in freq_dest.items()}
    
    def traducir_frase(self, frase):
        """
        Traduce una frase
        Args:
            frase: frase en idioma origen
        Returns:
            mejor traducción
        """
        if frase in self.tabla_traduccion:
            # Retornar traducción más probable
            return self.tabla_traduccion[frase][0][0]
        
        return frase  # Si no hay traducción, retornar original
    
    def traducir_oracion(self, oracion):
        """
        Traduce oración palabra por palabra o por frases
        Args:
            oracion: texto en idioma origen
        Returns:
            traducción
        """
        palabras = oracion.split()
        traduccion = []
        
        i = 0
        while i < len(palabras):
            # Intentar frases de longitud decreciente
            encontrado = False
            for longitud in range(min(5, len(palabras) - i), 0, -1):
                frase = ' '.join(palabras[i:i+longitud])
                
                if frase in self.tabla_traduccion:
                    traduccion.append(self.traducir_frase(frase))
                    i += longitud
                    encontrado = True
                    break
            
            if not encontrado:
                traduccion.append(palabras[i])
                i += 1
        
        return ' '.join(traduccion)
    
    def decodificar_beam_search(self, frase, beam_width=3):
        """
        Decodificación con beam search
        Args:
            frase: frase a traducir
            beam_width: ancho del beam
        Returns:
            mejores traducciones
        """
        if frase not in self.tabla_traduccion:
            return [(frase, 1.0)]
        
        candidatos = self.tabla_traduccion[frase][:beam_width]
        
        # Combinar con modelo de lenguaje
        scored_candidates = []
        for traduccion, prob_trad in candidatos:
            prob_lm = self.modelo_lenguaje.get(traduccion, 0.001)
            score = prob_trad * prob_lm
            scored_candidates.append((traduccion, score))
        
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        
        return scored_candidates


def alineamiento_palabra(oracion_origen, oracion_destino):
    """
    Alineamiento simple de palabras entre dos idiomas
    Args:
        oracion_origen: lista de palabras
        oracion_destino: lista de palabras
    Returns:
        lista de alineamientos (índice_origen, índice_destino)
    """
    # Alineamiento simple basado en similitud de longitud
    # (en práctica se usaría IBM Models o similar)
    alineamientos = []
    
    len_orig = len(oracion_origen)
    len_dest = len(oracion_destino)
    
    for i in range(len_orig):
        # Mapeo proporcional
        j = int((i / len_orig) * len_dest)
        if j < len_dest:
            alineamientos.append((i, j))
    
    return alineamientos


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== TRATAMIENTO PROBABILÍSTICO DEL LENGUAJE ===\n")
    
    # Ejemplo 39: Corpus y modelo de lenguaje
    print("39. Modelo de Lenguaje - Corpus:")
    corpus = Corpus()
    corpus.agregar_documento("el gato come pescado")
    corpus.agregar_documento("el perro come carne")
    corpus.agregar_documento("el gato duerme mucho")
    
    stats = corpus.estadisticas()
    print(f"   Estadísticas del corpus:")
    for k, v in stats.items():
        print(f"      {k}: {v}")
    
    modelo_uni = modelo_unigramas(corpus)
    print(f"\n   Probabilidades (top 5):")
    top_palabras = sorted(modelo_uni.items(), key=lambda x: x[1], reverse=True)[:5]
    for palabra, prob in top_palabras:
        print(f"      P('{palabra}') = {prob:.3f}")
    print()
    
    # Ejemplo 40: PCFG
    print("40. Gramática Probabilística:")
    pcfg = PCFG()
    # S -> NP VP
    pcfg.agregar_regla('S', ['NP', 'VP'], 1.0)
    # NP -> Det N
    pcfg.agregar_regla('NP', ['Det', 'N'], 0.6)
    pcfg.agregar_regla('NP', ['N'], 0.4)
    # VP -> V NP
    pcfg.agregar_regla('VP', ['V', 'NP'], 0.7)
    pcfg.agregar_regla('VP', ['V'], 0.3)
    # Terminales
    pcfg.agregar_regla('Det', ['el'], 0.5)
    pcfg.agregar_regla('Det', ['la'], 0.5)
    pcfg.agregar_regla('N', ['gato'], 0.5)
    pcfg.agregar_regla('N', ['perro'], 0.5)
    pcfg.agregar_regla('V', ['come'], 0.6)
    pcfg.agregar_regla('V', ['duerme'], 0.4)
    
    oracion_generada = pcfg.generar_oracion()
    print(f"   Oración generada: {' '.join(oracion_generada)}")
    print()
    
    # Ejemplo 42: Recuperación de información
    print("42. Recuperación de Información (TF-IDF):")
    modelo_vec = ModeloVectorial()
    modelo_vec.agregar_documento(1, "gato come pescado fresco")
    modelo_vec.agregar_documento(2, "perro come carne jugosa")
    modelo_vec.agregar_documento(3, "gato duerme en el sofá")
    
    resultados = modelo_vec.buscar("gato pescado", top_k=2)
    print(f"   Consulta: 'gato pescado'")
    print(f"   Resultados:")
    for doc_id, score in resultados:
        print(f"      Documento {doc_id}: score = {score:.3f}")
    print()
    
    # Ejemplo 43: Extracción de entidades
    print("43. Extracción de Información:")
    texto_ejemplo = "Juan vive en Madrid y trabaja en Google"
    
    patrones = {
        'PERSONA': r'\b[A-Z][a-z]+\b',
        'LUGAR': r'\b(Madrid|Barcelona|Londres)\b',
        'EMPRESA': r'\b(Google|Microsoft|Apple)\b'
    }
    
    entidades = extraccion_entidades_patrones(texto_ejemplo, patrones)
    print(f"   Texto: '{texto_ejemplo}'")
    print(f"   Entidades extraídas:")
    for tipo, lista in entidades.items():
        print(f"      {tipo}: {lista}")
    print()
    
    # Ejemplo 44: Traducción estadística
    print("44. Traducción Automática Estadística:")
    traductor = ModeloTraduccion()
    
    corpus_paralelo = [
        ('hello', 'hola'),
        ('world', 'mundo'),
        ('hello world', 'hola mundo'),
        ('goodbye', 'adiós'),
        ('thank you', 'gracias'),
    ]
    
    traductor.entrenar(corpus_paralelo)
    
    frase_en = 'hello world'
    traduccion = traductor.traducir_oracion(frase_en)
    print(f"   Inglés: '{frase_en}'")
    print(f"   Español: '{traduccion}'")