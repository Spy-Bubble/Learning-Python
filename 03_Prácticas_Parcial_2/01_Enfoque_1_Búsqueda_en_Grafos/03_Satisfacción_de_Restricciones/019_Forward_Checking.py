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
# 19. COMPROBACIÓN HACIA DELANTE
# ============================================================================

def forward_checking(csp, asignacion=None, dominios=None):
    """
    Backtracking con poda de dominios adelantada
    Args:
        csp: objeto CSP
        asignacion: diccionario de asignaciones
        dominios: dominios actuales (se modifican)
    Returns:
        asignación completa o None
    """
    if asignacion is None:
        asignacion = {}
    if dominios is None:
        # Copia profunda de los dominios para no alterar el CSP original
        dominios = {v: list(d) for v, d in csp.dominios.items()}
    
    if csp.asignacion_completa(asignacion):
        return asignacion
    
    variable = next(v for v in csp.variables if v not in asignacion)
    
    for valor in list(dominios[variable]): # Iterar sobre una copia
        asignacion[variable] = valor
        
        # Guardar dominios antes de podar
        dominios_guardados = {v: list(d) for v, d in dominios.items()}
        
        # Podar dominios de variables no asignadas
        fallo = False
        for v in csp.variables:
            if v not in asignacion:
                # Filtrar dominio de v
                dominios[v] = [val for val in dominios[v] 
                               if csp.es_consistente({**asignacion, v: val})]
                if not dominios[v]:
                    fallo = True
                    break
        
        if not fallo:
            resultado = forward_checking(csp, asignacion, dominios)
            if resultado:
                return resultado
        
        # Restaurar dominios (Backtrack)
        dominios.update(dominios_guardados)
        del asignacion[variable]
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 19. Comprobación Hacia Delante (Forward Checking) ===\n")
    
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
    
    solucion = forward_checking(csp)
    print(f"   Solución: {solucion}\n")