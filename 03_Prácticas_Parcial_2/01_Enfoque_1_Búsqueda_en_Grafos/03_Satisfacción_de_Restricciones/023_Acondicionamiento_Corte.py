# ============================================================================
# 17. PROBLEMAS DE SATISFACCIÓN DE RESTRICCIONES (CSP) - DEPENDENCIA
# ============================================================================

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
    
    def es_consistente(self, asignacion):
        for restriccion in self.restricciones:
            if not restriccion(asignacion):
                return False
        return True
    
    def asignacion_completa(self, asignacion):
        return len(asignacion) == len(self.variables)

# ============================================================================
# 18. BÚSQUEDA DE VUELTA ATRÁS (BACKTRACKING) - DEPENDENCIA
# ============================================================================

def backtracking(csp, asignacion=None):
    if asignacion is None:
        asignacion = {}
    if csp.asignacion_completa(asignacion):
        return asignacion
    
    variable = next(v for v in csp.variables if v not in asignacion)
    
    for valor in csp.dominios[variable]:
        asignacion[variable] = valor
        if csp.es_consistente(asignacion):
            resultado = backtracking(csp, asignacion)
            if resultado:
                return resultado
        del asignacion[variable]
    return None

# ============================================================================
# 23. ACONDICIONAMIENTO DEL CORTE (Conceptual)
# ============================================================================

def tree_decomposition(csp):
    """
    Simplifica CSP organizándolo como árbol (versión conceptual)
    Args:
        csp: objeto CSP
    Returns:
        CSP reorganizado o solución
    """
    # Implementación simplificada: ordenar variables para formar árbol
    # En la práctica, esto requiere análisis de grafo de restricciones
    
    # El código original simplemente llama a backtracking,
    # asumiendo que el CSP ya está "acondicionado" por su orden.
    print("Ejecutando Acondicionamiento del Corte (Conceptual)")
    print("   -> (Resolviendo con backtracking estándar)")
    
    # Resolver usando el orden de árbol (o el orden dado)
    return backtracking(csp)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 23. Acondicionamiento del Corte (Conceptual) ===\n")
    
    # --- Ejemplo: Coloración de Grafo ---
    print("Ejemplo: Coloración de Grafo (A-B, B-C)")
    variables = ['A', 'B', 'C']
    dominios = {
        'A': ['rojo', 'verde', 'azul'],
        'B': ['rojo', 'verde', 'azul'],
        'C': ['rojo', 'verde', 'azul']
    }
    
    def restriccion_ab(asignacion):
        if 'A' in asignacion and 'B' in asignacion:
            return asignacion['A'] != asignacion['B']
        return True
    
    def restriccion_bc(asignacion):
        if 'B' in asignacion and 'C' in asignacion:
            return asignacion['B'] != asignacion['C']
        return True
    
    restricciones = [restriccion_ab, restriccion_bc]
    csp = CSP(variables, dominios, restricciones)
    
    solucion = tree_decomposition(csp)
    print(f"   Solución: {solucion}\n")