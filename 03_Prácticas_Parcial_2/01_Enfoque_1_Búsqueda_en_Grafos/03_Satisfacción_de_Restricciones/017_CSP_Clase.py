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
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 17. Definición de Clase CSP ===\n")
    
    # Ejemplo: Problema de coloración de grafo
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
    
    # Instanciar el objeto CSP
    csp_mapa = CSP(variables, dominios, restricciones)
    
    print("Objeto CSP creado exitosamente.")
    print(f"Variables: {csp_mapa.variables}")
    print(f"Dominios de 'A': {csp_mapa.dominios['A']}")