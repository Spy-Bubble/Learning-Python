import re
from collections import defaultdict

# ============================================================================
# 43. EXTRACCIÓN DE INFORMACIÓN
# ============================================================================

def extraccion_entidades_patrones(texto, patrones_regex):
    """
    Extracción simple de entidades usando patrones regex predefinidos.
    Args:
        texto: texto a analizar
        patrones_regex: dict {tipo_entidad: string_regex}
    Returns:
        dict {tipo_entidad: [lista_de_menciones]}
    """
    entidades_encontradas = defaultdict(list)

    for tipo_entidad, patron in patrones_regex.items():
        # Usar re.finditer para encontrar todas las ocurrencias no solapadas
        try:
            matches = re.finditer(patron, texto, re.IGNORECASE)
            for match in matches:
                entidades_encontradas[tipo_entidad].append(match.group(0)) # group(0) es el match completo
        except re.error as e:
             print(f"Error en regex para '{tipo_entidad}': {e}")

    return dict(entidades_encontradas)


def extraccion_relaciones_patrones(texto, patrones_relacion):
    """
    Extrae relaciones (sujeto, relacion, objeto) usando regex con grupos.
    Args:
        texto: texto a analizar
        patrones_relacion: lista de tuplas (string_regex_con_grupos, tipo_relacion)
                           El regex debe capturar sujeto y objeto en grupos.
    Returns:
        lista de tuplas (sujeto, relacion, objeto)
    """
    relaciones_encontradas = []

    for patron, tipo_relacion in patrones_relacion:
        try:
            matches = re.finditer(patron, texto, re.IGNORECASE | re.DOTALL)
            for match in matches:
                grupos = match.groups()
                # Asumir que el primer grupo es sujeto, segundo es objeto
                if len(grupos) >= 2:
                    sujeto = grupos[0].strip()
                    objeto = grupos[1].strip()
                    relaciones_encontradas.append((sujeto, tipo_relacion, objeto))
        except re.error as e:
            print(f"Error en regex para relación '{tipo_relacion}': {e}")
        except IndexError:
             print(f"Error: Regex para '{tipo_relacion}' no capturó suficientes grupos.")


    return relaciones_encontradas


class ExtractorNER_SimpleGazetteer:
    """
    Extractor simple de Entidades Nombradas (NER) basado en diccionarios (gazetteers).
    """
    def __init__(self):
        # Diccionarios de entidades conocidas (gazetteers)
        self.gazetteers = defaultdict(set)
        # Ejemplo: self.gazetteers['PERSONA'] = {'juan', 'maria', ...}

    def agregar_entidad(self, tipo_entidad, nombre_entidad):
        """Agrega una entidad conocida al diccionario"""
        self.gazetteers[tipo_entidad].add(nombre_entidad.lower())

    def entrenar(self, textos_anotados):
        """
        'Entrena' poblando los gazetteers desde datos anotados.
        Args:
            textos_anotados: lista de (texto, lista_anotaciones)
                             donde lista_anotaciones es [(tipo, entidad_texto), ...]
        """
        print("   (Entrenando ExtractorNER: Poblando diccionarios...)")
        for _texto, anotaciones in textos_anotados:
            for tipo, entidad in anotaciones:
                self.agregar_entidad(tipo.upper(), entidad)

    def extraer(self, texto):
        """Extrae entidades buscando menciones exactas en los diccionarios."""
        entidades_encontradas = []
        # Tokenizar simple (podría mejorarse)
        tokens = re.findall(r'\b\w+\b', texto)

        # Buscar coincidencias exactas (esto es muy básico)
        # Enfoques más avanzados usan longest match, etc.
        for i, token in enumerate(tokens):
            token_lower = token.lower()
            for tipo_entidad, nombres_conocidos in self.gazetteers.items():
                if token_lower in nombres_conocidos:
                    entidades_encontradas.append((tipo_entidad, token))
                    # Podríamos añadir heurísticas aquí (ej. si token[0].isupper())
                    break # Asumir que un token pertenece a una sola entidad

        return entidades_encontradas

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 43. Extracción de Información ===\n")

    texto_ejemplo = "Juan Pérez vive en Madrid y trabaja para Acme Corp. desde 2023. Su email es juan.perez@email.com"

    # 1. Extracción de Entidades con Patrones Regex
    print("1. Extracción de Entidades (Regex):")
    patrones_entidad = {
        'PERSONA': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', # Nombre Apellido
        'LUGAR': r'\b(Madrid|Barcelona|Londres)\b',
        'ORGANIZACION': r'\b[A-Z][a-z]+ (Corp|Inc|Ltd)\b',
        'EMAIL': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        'AÑO': r'\b(19|20)\d{2}\b'
    }
    entidades_regex = extraccion_entidades_patrones(texto_ejemplo, patrones_entidad)
    print(f"   Texto: '{texto_ejemplo}'")
    print(f"   Entidades extraídas (Regex):")
    for tipo, lista in entidades_regex.items():
        print(f"      {tipo}: {lista}")
    print()

    # 2. Extracción de Relaciones con Patrones Regex
    print("2. Extracción de Relaciones (Regex):")
    patrones_relacion = [
        (r'(\w+ \w+) vive en (\w+)', 'VIVE_EN'),
        (r'(\w+ \w+) trabaja para ([\w\s]+Corp)', 'TRABAJA_EN')
    ]
    relaciones_regex = extraccion_relaciones_patrones(texto_ejemplo, patrones_relacion)
    print(f"   Relaciones extraídas (Regex):")
    for rel in relaciones_regex:
        print(f"      {rel}")
    print()

    # 3. Extracción de Entidades Nombradas (NER) con Gazetteer
    print("3. Extracción NER (Gazetteer Simple):")
    ner_extractor = ExtractorNER_SimpleGazetteer()
    # Poblar gazetteer (simulando entrenamiento)
    ner_extractor.agregar_entidad('PERSONA', 'Juan Pérez') # Necesitaría manejar multi-token
    ner_extractor.agregar_entidad('LUGAR', 'Madrid')
    ner_extractor.agregar_entidad('ORGANIZACION', 'Acme Corp') # Necesitaría manejar multi-token

    # Adaptación para buscar tokens individuales
    ner_extractor_token = ExtractorNER_SimpleGazetteer()
    ner_extractor_token.agregar_entidad('PERSONA', 'Juan')
    ner_extractor_token.agregar_entidad('LUGAR', 'Madrid')
    ner_extractor_token.agregar_entidad('ORGANIZACION', 'Acme') # Solo la primera parte

    entidades_ner = ner_extractor_token.extraer(texto_ejemplo)
    print(f"   Entidades extraídas (Gazetteer): {entidades_ner}")