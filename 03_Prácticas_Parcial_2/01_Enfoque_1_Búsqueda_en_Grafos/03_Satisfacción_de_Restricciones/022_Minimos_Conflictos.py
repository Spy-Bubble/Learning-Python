import random

# ============================================================================
# 17. PROBLEMAS DE SATISFACCIÓN DE RESTRICCIONES (CSP) - DEPENDENCIA
# ============================================================================

class CSP:
    def __init__(self, variables, dominios, restricciones):
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
    
    def es_consistente(self, asignacion):
        """Verifica si la asignación PARCIAL O COMPLETA es consistente"""
        for restriccion in self.restricciones:
            if not restriccion(asignacion):
                return False
        return True

    def asignacion_completa(self, asignacion):
        return len(asignacion) == len(self.variables)
        
    def contar_conflictos(self, asignacion):
        """Cuenta cuántas restricciones se violan"""
        count = 0
        for r in self.restricciones:
            if not r(asignacion):
                count += 1
        return count

# ============================================================================
# 22. BÚSQUEDA LOCAL: MÍNIMOS-CONFLICTOS
# ============================================================================

def minimos_conflictos(csp, max_pasos=1000):
    """
    Algoritmo de búsqueda local para CSP
    Args:
        csp: objeto CSP
        max_pasos: iteraciones máximas
    Returns:
        asignación completa o None
    """
    # Asignación inicial aleatoria (completa)
    asignacion = {v: random.choice(csp.dominios[v]) for v in csp.variables}
    
    for _ in range(max_pasos):
        conflictos_totales = csp.contar_conflictos(asignacion)
        if conflictos_totales == 0:
            return asignacion # Solución encontrada
        
        # Seleccionar variable aleatoria en conflicto
        variables_conflicto = [v for v in csp.variables 
                               if csp.contar_conflictos(asignacion) > 0] 
        # (Nota: Esta lógica de selección es simplificada; idealmente
        # se selecciona una variable que *participa* en un conflicto)
        if not variables_conflicto:
            continue
            
        variable = random.choice(variables_conflicto)
        
        # Encontrar valor que minimiza conflictos
        min_conflictos = float('inf')
        mejor_valor = asignacion[variable] # Mantener actual si no hay mejora
        
        for valor in csp.dominios[variable]:
            asignacion[variable] = valor
            conflictos = csp.contar_conflictos(asignacion)
            
            if conflictos < min_conflictos:
                min_conflictos = conflictos
                mejor_valor = valor
        
        # Asignar el mejor valor encontrado
        asignacion[variable] = mejor_valor
    
    return None # No se encontró solución

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 22. Búsqueda Local Mínimos-Conflictos ===\n")
    
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
    
    solucion = minimos_conflictos(csp, max_pasos=100)
    print(f"   Solución: {solucion}\n")

    # --- Ejemplo 2: 8-Reinas (mejor para mín-conflictos) ---
    print("Ejemplo: Problema de 8-Reinas")
    n = 8
    variables_reinas = list(range(n))
    dominios_reinas = {i: list(range(n)) for i in range(n)}
    
    def no_ataque(asignacion):
        for i in asignacion:
            for j in asignacion:
                if i < j:
                    if asignacion[i] == asignacion[j]:
                        return False
                    if abs(asignacion[i] - asignacion[j]) == abs(i - j):
                        return False
        return True
    
    csp_reinas = CSP(variables_reinas, dominios_reinas, [no_ataque])
    
    solucion_reinas = minimos_conflictos(csp_reinas, max_pasos=2000)
    print(f"   Solución 8-Reinas (col: fila): {solucion_reinas}\n")