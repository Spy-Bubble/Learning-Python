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
# 20. PROPAGACIÓN DE RESTRICCIONES (AC-3)
# ============================================================================

def ac3(csp, dominios_originales):
    """
    Algoritmo AC-3 para consistencia de arcos
    Modifica el diccionario 'dominios'
    Args:
        csp: objeto CSP
        dominios_originales: dict de dominios a podar
    Returns:
        True si hay solución posible, False si inconsistencia detectada
    """
    # Copia para trabajar
    dominios = dominios_originales 
    
    # Cola de arcos (pares de variables relacionadas)
    # Asumimos que todas las variables están relacionadas
    cola = [(v1, v2) for v1 in csp.variables for v2 in csp.variables if v1 != v2]
    
    while cola:
        (xi, xj) = cola.pop(0)
        
        if revisar(csp, dominios, xi, xj):
            if not dominios[xi]:
                return False  # Dominio vacío, no hay solución
            
            # Agregar arcos relacionados a la cola
            for xk in csp.variables:
                if xk != xi and xk != xj:
                    cola.append((xk, xi))
    
    return True


def revisar(csp, dominios, xi, xj):
    """
    Revisa la consistencia del arco (xi, xj)
    Elimina valores de xi que no tienen soporte en xj
    """
    revisado = False
    for valor_i in dominios[xi][:]:
        # Verificar si existe algún valor en xj que sea consistente
        tiene_soporte = False
        for valor_j in dominios[xj]:
            asignacion = {xi: valor_i, xj: valor_j}
            if csp.es_consistente(asignacion):
                tiene_soporte = True
                break
        
        if not tiene_soporte:
            dominios[xi].remove(valor_i)
            revisado = True
    
    return revisado

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 20. Propagación de Restricciones (AC-3) ===\n")
    
    # Ejemplo: A, B, C con dominios limitados
    # A != B, B != C, A != C
    variables = ['A', 'B', 'C']
    dominios = {
        'A': ['rojo', 'verde'],
        'B': ['rojo'],
        'C': ['rojo', 'verde']
    }
    
    def r_ab(a):
        return 'A' not in a or 'B' not in a or a['A'] != a['B']
    def r_bc(a):
        return 'B' not in a or 'C' not in a or a['B'] != a['C']
    def r_ac(a):
        return 'A' not in a or 'C' not in a or a['A'] != a['C']
        
    restricciones = [r_ab, r_bc, r_ac]
    
    csp = CSP(variables, dominios, restricciones)
    
    # Copiamos los dominios para que AC-3 los modifique
    dominios_a_podar = {v: list(d) for v, d in csp.dominios.items()}
    
    print(f"Dominios ANTES de AC-3: {dominios_a_podar}")
    
    es_consistente = ac3(csp, dominios_a_podar)
    
    print(f"\n¿Consistente? {es_consistente}")
    print(f"Dominios DESPUÉS de AC-3: {dominios_a_podar}")
    # (Esperado: A={'verde'}, B={'rojo'}, C={'verde'})