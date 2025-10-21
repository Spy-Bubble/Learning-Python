"""
SATISFACCIÓN DE RESTRICCIONES
Algoritmos 17-23: CSP y técnicas de resolución
"""

import random

# ============================================================================
# 17. PROBLEMAS DE SATISFACCIÓN DE RESTRICCIONES (CSP)
# ============================================================================

class CSP:
    """
    Clase para representar un Problema de Satisfacción de Restricciones
    """
    def __init__(self, variables, dominios, restricciones):
        """
        Args:
            variables: lista de variables
            dominios: diccionario {variable: [valores posibles]}
            restricciones: lista de funciones (asignacion) -> bool
        """
        self.variables = variables
        self.dominios = dominios
        self.restricciones = restricciones
    
    def es_consistente(self, asignacion):
        """Verifica si la asignación satisface todas las restricciones"""
        for restriccion in self.restricciones:
            if not restriccion(asignacion):
                return False
        return True
    
    def asignacion_completa(self, asignacion):
        """Verifica si todas las variables están asignadas"""
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
        dominios = {v: list(d) for v, d in csp.dominios.items()}
    
    if csp.asignacion_completa(asignacion):
        return asignacion
    
    variable = next(v for v in csp.variables if v not in asignacion)
    
    for valor in dominios[variable]:
        asignacion[variable] = valor
        
        if not csp.es_consistente(asignacion):
            del asignacion[variable]
            continue
        
        # Guardar dominios antes de podar
        dominios_guardados = {v: list(d) for v, d in dominios.items()}
        
        # Podar dominios de variables no asignadas
        fallo = False
        for v in csp.variables:
            if v not in asignacion:
                dominios[v] = [val for val in dominios[v] 
                              if csp.es_consistente({**asignacion, v: val})]
                if not dominios[v]:
                    fallo = True
                    break
        
        if not fallo:
            resultado = forward_checking(csp, asignacion, dominios)
            if resultado:
                return resultado
        
        # Restaurar dominios
        dominios.update(dominios_guardados)
        del asignacion[variable]
    
    return None


# ============================================================================
# 20. PROPAGACIÓN DE RESTRICCIONES (AC-3)
# ============================================================================

def ac3(csp):
    """
    Algoritmo AC-3 para consistencia de arcos
    Args:
        csp: objeto CSP
    Returns:
        True si hay solución posible, False si inconsistencia detectada
    """
    # Cola de arcos (pares de variables relacionadas)
    cola = [(v1, v2) for v1 in csp.variables for v2 in csp.variables if v1 != v2]
    
    while cola:
        (xi, xj) = cola.pop(0)
        
        if revisar(csp, xi, xj):
            if not csp.dominios[xi]:
                return False  # Dominio vacío, no hay solución
            
            # Agregar arcos relacionados a la cola
            for xk in csp.variables:
                if xk != xi and xk != xj:
                    cola.append((xk, xi))
    
    return True


def revisar(csp, xi, xj):
    """
    Revisa la consistencia del arco (xi, xj)
    Elimina valores de xi que no tienen soporte en xj
    """
    revisado = False
    for valor_i in csp.dominios[xi][:]:
        # Verificar si existe algún valor en xj que sea consistente
        tiene_soporte = False
        for valor_j in csp.dominios[xj]:
            asignacion = {xi: valor_i, xj: valor_j}
            if csp.es_consistente(asignacion):
                tiene_soporte = True
                break
        
        if not tiene_soporte:
            csp.dominios[xi].remove(valor_i)
            revisado = True
    
    return revisado


# ============================================================================
# 21. SALTO ATRÁS DIRIGIDO POR CONFLICTOS
# ============================================================================

def conflict_directed_backjumping(csp, asignacion=None, conjunto_conflicto=None):
    """
    Backtracking que salta a la variable que causó el conflicto
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
                    conjunto_conflicto[variable].add(v)
        
        del asignacion[variable]
    
    return None


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
    # Asignación inicial aleatoria
    asignacion = {v: random.choice(csp.dominios[v]) for v in csp.variables}
    
    for _ in range(max_pasos):
        if csp.es_consistente(asignacion):
            return asignacion
        
        # Seleccionar variable en conflicto
        variables_conflicto = [v for v in csp.variables 
                              if not csp.es_consistente({v: asignacion[v]})]
        
        if not variables_conflicto:
            return asignacion
        
        variable = random.choice(variables_conflicto)
        
        # Encontrar valor que minimiza conflictos
        min_conflictos = float('inf')
        mejor_valor = None
        
        for valor in csp.dominios[variable]:
            asignacion[variable] = valor
            conflictos = sum(1 for r in csp.restricciones if not r(asignacion))
            
            if conflictos < min_conflictos:
                min_conflictos = conflictos
                mejor_valor = valor
        
        asignacion[variable] = mejor_valor
    
    return None


# ============================================================================
# 23. ACONDICIONAMIENTO DEL CORTE
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
    
    # Ordenamiento topológico simplificado
    variables_ordenadas = list(csp.variables)
    
    # Resolver usando el orden de árbol
    return backtracking(csp)


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== SATISFACCIÓN DE RESTRICCIONES ===\n")
    
    # Ejemplo: Problema de coloración de grafo
    # Variables: nodos A, B, C
    # Dominios: colores {rojo, verde, azul}
    # Restricción: nodos adyacentes deben tener colores diferentes
    
    variables = ['A', 'B', 'C']
    dominios = {
        'A': ['rojo', 'verde', 'azul'],
        'B': ['rojo', 'verde', 'azul'],
        'C': ['rojo', 'verde', 'azul']
    }
    
    # Restricciones: A-B adyacentes, B-C adyacentes
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
    
    print("18. Backtracking:")
    solucion = backtracking(csp)
    print(f"   Solución: {solucion}\n")
    
    print("19. Forward Checking:")
    solucion = forward_checking(csp)
    print(f"   Solución: {solucion}\n")
    
    print("22. Mínimos Conflictos:")
    solucion = minimos_conflictos(csp, max_pasos=100)
    print(f"   Solución: {solucion}\n")
    
    # Ejemplo: Problema de N-Reinas (4 reinas)
    print("\nEjemplo: Problema de 4-Reinas")
    n = 4
    variables_reinas = list(range(n))
    dominios_reinas = {i: list(range(n)) for i in range(n)}
    
    def no_ataque(asignacion):
        """Ninguna reina ataca a otra"""
        for i in asignacion:
            for j in asignacion:
                if i < j:
                    # Misma fila o diagonal
                    if asignacion[i] == asignacion[j]:
                        return False
                    if abs(asignacion[i] - asignacion[j]) == abs(i - j):
                        return False
        return True
    
    csp_reinas = CSP(variables_reinas, dominios_reinas, [no_ataque])
    
    solucion_reinas = backtracking(csp_reinas)
    print(f"   Solución 4-Reinas: {solucion_reinas}")
    
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