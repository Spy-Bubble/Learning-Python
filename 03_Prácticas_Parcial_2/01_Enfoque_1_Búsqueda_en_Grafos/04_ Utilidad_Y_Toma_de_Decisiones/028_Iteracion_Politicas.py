import random

# ============================================================================
# 28. ITERACIÓN DE POLÍTICAS
# ============================================================================

def iteracion_politicas(estados, acciones, transiciones, recompensas, gamma=0.9):
    """
    Algoritmo de iteración de políticas para MDP
    Args:
        estados: lista de estados
        acciones: lista de acciones
        transiciones: dict {(s, a, s'): probabilidad}
        recompensas: dict {(s, a): recompensa}
        gamma: factor de descuento
    Returns:
        política óptima {estado: accion}
    """
    # Política inicial aleatoria
    politica = {s: random.choice(acciones) for s in estados}
    
    while True:
        # 1. Evaluación de política (calcula V(s) para la política actual)
        V = evaluar_politica(estados, politica, transiciones, recompensas, gamma)
        
        # 2. Mejora de política
        politica_estable = True
        
        for s in estados:
            accion_vieja = politica[s]
            
            # Encontrar mejor acción (mirando un paso adelante)
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
    """Evalúa el valor de una política dada (V_pi)"""
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
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 28. Iteración de Políticas (MDP) ===\n")

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

    politica = iteracion_politicas(estados, acciones, transiciones, recompensas, gamma=0.9)
    print("Política óptima (pi*) por estado:")
    for s, a in politica.items():
        print(f"   pi({s}): {a}")