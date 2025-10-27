import random

# ============================================================================
# 27. ITERACIÓN DE VALORES (DEPENDENCIA)
# ============================================================================

def iteracion_valores(estados, acciones, transiciones, recompensas, gamma=0.9, epsilon=0.01):
    V = {s: 0 for s in estados}
    while True:
        delta = 0
        V_nuevo = {}
        for s in estados:
            valores_acciones = []
            for a in acciones:
                valor = recompensas.get((s, a), 0)
                for s_prima in estados:
                    prob = transiciones.get((s, a, s_prima), 0)
                    valor += gamma * prob * V[s_prima]
                valores_acciones.append(valor)
            V_nuevo[s] = max(valores_acciones) if valores_acciones else 0
            delta = max(delta, abs(V_nuevo[s] - V[s]))
        V = V_nuevo
        if delta < epsilon * (1 - gamma) / gamma:
            break
    return V

# ============================================================================
# 28. ITERACIÓN DE POLÍTICAS (DEPENDENCIA)
# ============================================================================

def iteracion_politicas(estados, acciones, transiciones, recompensas, gamma=0.9):
    politica = {s: random.choice(acciones) for s in estados}
    while True:
        V = evaluar_politica(estados, politica, transiciones, recompensas, gamma)
        politica_estable = True
        for s in estados:
            accion_vieja = politica[s]
            mejor_accion = None
            mejor_valor = float('-inf')
            for a in acciones:
                valor = recompensas.get((s, a), 0)
                for s_prima in estados:
                    prob = transiciones.get((s, a, s_prima), 0)
                    valor += gamma * prob * V[s_prima]
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_accion = a
            politica[s] = mejor_accion
            if accion_vieja != mejor_accion:
                politica_estable = False
        if politica_estable:
            break
    return politica

def evaluar_politica(estados, politica, transiciones, recompensas, gamma, epsilon=0.01):
    V = {s: 0 for s in estados}
    while True:
        delta = 0
        V_nuevo = {}
        for s in estados:
            a = politica[s]
            valor = recompensas.get((s, a), 0)
            for s_prima in estados:
                prob = transiciones.get((s, a, s_prima), 0)
                valor += gamma * prob * V[s_prima]
            V_nuevo[s] = valor
            delta = max(delta, abs(V_nuevo[s] - V[s]))
        V = V_nuevo
        if delta < epsilon * (1 - gamma) / gamma:
            break
    return V

# ============================================================================
# 29. PROCESO DE DECISIÓN DE MARKOV (MDP)
# ============================================================================

class MDP:
    """
    Clase para representar un Proceso de Decisión de Markov
    """
    def __init__(self, estados, acciones, transiciones, recompensas, gamma=0.9):
        """
        Args:
            estados: lista de estados
            acciones: lista de acciones
            transiciones: función o dict P(s'|s,a)
            recompensas: función o dict R(s,a)
            gamma: factor de descuento
        """
        self.estados = estados
        self.acciones = acciones
        self.transiciones = transiciones
        self.recompensas = recompensas
        self.gamma = gamma
    
    def resolver_iteracion_valores(self):
        """Resuelve el MDP usando iteración de valores"""
        return iteracion_valores(self.estados, self.acciones, 
                                 self.transiciones, self.recompensas, self.gamma)
    
    def resolver_iteracion_politicas(self):
        """Resuelve el MDP usando iteración de políticas"""
        return iteracion_politicas(self.estados, self.acciones,
                                   self.transiciones, self.recompensas, self.gamma)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 29. Clase Proceso de Decisión de Markov (MDP) ===\n")
    
    # Ejemplo: MDP simple (robot en grid)
    estados = ['s1', 's2', 's3', 'meta']
    acciones = ['ir_derecha', 'quedarse']
    
    transiciones = {
        ('s1', 'ir_derecha', 's2'): 0.8, ('s1', 'ir_derecha', 's1'): 0.2,
        ('s2', 'ir_derecha', 's3'): 0.8, ('s2', 'ir_derecha', 's2'): 0.2,
        ('s3', 'ir_derecha', 'meta'): 1.0,
        ('s1', 'quedarse', 's1'): 1.0, ('s2', 'quedarse', 's2'): 1.0,
        ('s3', 'quedarse', 's3'): 1.0, ('meta', 'ir_derecha', 'meta'): 1.0,
        ('meta', 'quedarse', 'meta'): 1.0,
    }
    recompensas = {
        ('s1', 'ir_derecha'): -1, ('s2', 'ir_derecha'): -1,
        ('s3', 'ir_derecha'): 10, ('meta', 'ir_derecha'): 0,
        ('s1', 'quedarse'): -1, ('s2', 'quedarse'): -1,
        ('s3', 'quedarse'): -1, ('meta', 'quedarse'): 0,
    }
    
    mdp = MDP(estados, acciones, transiciones, recompensas, gamma=0.9)
    
    print("Resolviendo con Iteración de Valores:")
    valores = mdp.resolver_iteracion_valores()
    print(f"   Valores óptimos: {valores}\n")
    
    print("Resolviendo con Iteración de Políticas:")
    politica = mdp.resolver_iteracion_politicas()
    print(f"   Política óptima: {politica}\n")