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
# 21. SALTO ATRÁS DIRIGIDO POR CONFLICTOS (Conceptual)
# ============================================================================
# Nota: La implementación proporcionada es una versión simplificada
# que identifica conflictos pero no implementa el "salto" real.
# Es más un backtracking que registra conflictos.

def conflict_directed_backjumping(csp, asignacion=None, conjunto_conflicto=None):
    """
    Backtracking que salta a la variable que causó el conflicto (Conceptual)
    Args:
        csp: objeto CSP
        asignacion: asignaciones actuales
        conjunto_conflicto: diccionario de conjuntos de conflicto
    Returns:
        asignación o None
    """
    if asignacion is None:
        asignacion = {}
    if conjunto_conflicto is None:
        conjunto_conflicto = {v: set() for v in csp.variables}
    
    if csp.asignacion_completa(asignacion):
        return asignacion
    
    variable = next(v for v in csp.variables if v not in asignacion)
    
    for valor in csp.dominios[variable]:
        asignacion[variable] = valor
        
        if csp.es_consistente(asignacion):
            resultado = conflict_directed_backjumping(csp, asignacion, conjunto_conflicto)
            if resultado:
                return resultado
        else:
            # Registrar variables en conflicto
            for v in asignacion:
                if v != variable:
                    # Si 'v' ya estaba asignada, contribuyó a este conflicto
                    conjunto_conflicto[variable].add(v)
            
        del asignacion[variable]
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 21. Salto Atrás Dirigido por Conflictos (Conceptual) ===\n")
    
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
    
    conjuntos_conflicto_global = {v: set() for v in csp.variables}
    
    solucion = conflict_directed_backjumping(csp, conjunto_conflicto=conjuntos_conflicto_global)
    
    print(f"   Solución: {solucion}\n")
    # print(f"   Conjuntos de conflicto (informativo): {conjuntos_conflicto_global}")