# ============================================================================
# 25. REDES DE DECISIÓN
# ============================================================================

class RedDecision:
    """
    Representa una red de decisión (diagrama de influencia)
    """
    def __init__(self):
        self.nodos_azar = {}  # Nodos de probabilidad
        self.nodos_decision = []  # Nodos de decisión
        self.nodos_utilidad = {}  # Nodos de utilidad
    
    def agregar_nodo_azar(self, nombre, probabilidades):
        """Agrega nodo con incertidumbre"""
        self.nodos_azar[nombre] = probabilidades
    
    def agregar_nodo_decision(self, nombre, opciones):
        """Agrega nodo de decisión"""
        self.nodos_decision.append((nombre, opciones))
    
    def agregar_nodo_utilidad(self, nombre, funcion_utilidad):
        """Agrega nodo de utilidad"""
        self.nodos_utilidad[nombre] = funcion_utilidad
    
    def evaluar(self, decision):
        """
        Evalúa utilidad esperada de una decisión
        Args:
            decision: diccionario de decisiones
        Returns:
            utilidad esperada
        """
        # Nota: Esta es una evaluación simplificada.
        # Una red real necesitaría inferencia (ej. eliminación de variables)
        # para combinar azar y decisiones antes de la utilidad.
        
        utilidad_total = 0
        
        for nombre_util, func_util in self.nodos_utilidad.items():
            # Asumimos que la func_util puede calcular la utilidad
            # basándose en la decisión tomada.
            utilidad_total += func_util(decision)
        
        return utilidad_total

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 25. Redes de Decisión ===\n")
    
    # Ejemplo simple: ¿Llevar paraguas?
    red = RedDecision()
    
    # Decisión: D = {llevar, no_llevar}
    red.agregar_nodo_decision('Paraguas', ['llevar', 'no_llevar'])
    
    # Azar: Clima = {lluvia, sol}
    red.agregar_nodo_azar('Clima', {'lluvia': 0.3, 'sol': 0.7})
    
    # Utilidad: U(Clima, Paraguas)
    def calcular_utilidad(decision):
        paraguas = decision.get('Paraguas')
        
        # Simulación simplificada de utilidad esperada
        # (En una red real, P(Clima) influiría aquí)
        if paraguas == 'llevar':
            # P(lluvia)*U(lluvia, llevar) + P(sol)*U(sol, llevar)
            util_esperada = (0.3 * 70) + (0.7 * 80)
            return util_esperada
        else: # no_llevar
            # P(lluvia)*U(lluvia, no) + P(sol)*U(sol, no)
            util_esperada = (0.3 * 20) + (0.7 * 100)
            return util_esperada

    red.agregar_nodo_utilidad('Felicidad', calcular_utilidad)
    
    decision_1 = {'Paraguas': 'llevar'}
    decision_2 = {'Paraguas': 'no_llevar'}
    
    print(f"Utilidad esperada de 'llevar': {red.evaluar(decision_1)}")
    print(f"Utilidad esperada de 'no_llevar': {red.evaluar(decision_2)}")