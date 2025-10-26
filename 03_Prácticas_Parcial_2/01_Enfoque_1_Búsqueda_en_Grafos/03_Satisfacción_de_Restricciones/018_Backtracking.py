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
# 18. BÚSQUEDA DE VUELTA ATRÁS (BACKTRACKING)
# ============================================================================

def backtracking(csp, asignacion=None):
    """
    Búsqueda recursiva con retroceso para resolver CSP
    Args:
        csp: objeto CSP
        asignacion: diccionario {variable: valor}
    Returns:
        asignación completa o None
    """
    if asignacion is None:
        asignacion = {}
    
    # Caso base: asignación completa
    if csp.asignacion_completa(asignacion):
        return asignacion
    
    # Seleccionar variable no asignada
    variable = next(v for v in csp.variables if v not in asignacion)
    
    # Probar cada valor del dominio
    for valor in csp.dominios[variable]:
        asignacion[variable] = valor
        
        # Verificar consistencia
        if csp.es_consistente(asignacion):
            resultado = backtracking(csp, asignacion)
            if resultado:
                return resultado
        
        # Retroceder
        del asignacion[variable]
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 18. Búsqueda de Vuelta Atrás (Backtracking) ===\n")
    
    # --- Ejemplo 1: Coloración de Grafo ---
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
    
    solucion = backtracking(csp)
    print(f"   Solución: {solucion}\n")

    # --- Ejemplo 2: 4-Reinas ---
    print("Ejemplo: Problema de 4-Reinas")
    n = 4
    variables_reinas = list(range(n)) # Columnas 0, 1, 2, 3
    # Dominio: {columna: [fila_posible_0, ...]}
    dominios_reinas = {i: list(range(n)) for i in range(n)}
    
    def no_ataque(asignacion):
        """Ninguna reina ataca a otra"""
        for i in asignacion: # i es la columna
            for j in asignacion: # j es la columna
                if i < j:
                    # Misma fila
                    if asignacion[i] == asignacion[j]:
                        return False
                    # Diagonal
                    if abs(asignacion[i] - asignacion[j]) == abs(i - j):
                        return False
        return True
    
    csp_reinas = CSP(variables_reinas, dominios_reinas, [no_ataque])
    
    solucion_reinas = backtracking(csp_reinas)
    print(f"   Solución 4-Reinas (col: fila): {solucion_reinas}")
    
    # Visualizar tablero
    if solucion_reinas:
        print("\n   Tablero:")
        for fila in range(n):
            linea = ""
            for col in range(n):
                if solucion_reinas.get(col) == fila:
                    linea += " Q "
                else:
                    linea += " . "
            print(f"   {linea}")