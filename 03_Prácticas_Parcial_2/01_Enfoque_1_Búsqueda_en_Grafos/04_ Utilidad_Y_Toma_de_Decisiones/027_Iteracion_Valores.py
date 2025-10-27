# ============================================================================
# 27. ITERACIÓN DE VALORES
# ============================================================================

def iteracion_valores(estados, acciones, transiciones, recompensas, gamma=0.9, epsilon=0.01):
    """
    Algoritmo de iteración de valores para MDP
    Args:
        estados: lista de estados
        acciones: lista de acciones
        transiciones: dict {(s, a, s'): probabilidad}
        recompensas: dict {(s, a): recompensa}
        gamma: factor de descuento
        epsilon: umbral de convergencia
    Returns:
        valores óptimos de cada estado
    """
    # Inicializar valores
    V = {s: 0 for s in estados}
    
    while True:
        delta = 0
        V_nuevo = {}
        
        for s in estados:
            # Calcular valor para cada acción
            valores_acciones = []
            
            for a in acciones:
                # Recompensa inmediata por (s, a)
                # Nota: Las recompensas a veces se definen R(s,a,s') o R(s)
                # Aquí asumimos R(s,a)
                valor = recompensas.get((s, a), 0)
                
                # Sumar valores esperados de estados siguientes
                for s_prima in estados:
                    prob = transiciones.get((s, a, s_prima), 0)
                    valor += gamma * prob * V[s_prima]
                
                valores_acciones.append(valor)
            
            # Mejor valor para este estado (Ecuación de Bellman)
            V_nuevo[s] = max(valores_acciones) if valores_acciones else 0
            delta = max(delta, abs(V_nuevo[s] - V[s]))
        
        V = V_nuevo
        
        # Convergencia
        if delta < epsilon * (1 - gamma) / gamma: # Condición de parada más estricta
            break
    
    return V

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 27. Iteración de Valores (MDP) ===\n")
    
    # Ejemplo: MDP simple (robot en grid)
    estados = ['s1', 's2', 's3', 'meta']
    acciones = ['ir_derecha', 'quedarse']
    
    # Transiciones: P(s'|s,a)
    transiciones = {
        ('s1', 'ir_derecha', 's2'): 0.8,
        ('s1', 'ir_derecha', 's1'): 0.2, # Resbala
        ('s2', 'ir_derecha', 's3'): 0.8,
        ('s2', 'ir_derecha', 's2'): 0.2,
        ('s3', 'ir_derecha', 'meta'): 1.0,
        ('s1', 'quedarse', 's1'): 1.0,
        ('s2', 'quedarse', 's2'): 1.0,
        ('s3', 'quedarse', 's3'): 1.0,
        ('meta', 'ir_derecha', 'meta'): 1.0, # Terminal
        ('meta', 'quedarse', 'meta'): 1.0, # Terminal
    }
    
    # Recompensas: R(s,a)
    recompensas = {
        ('s1', 'ir_derecha'): -1,
        ('s2', 'ir_derecha'): -1,
        ('s3', 'ir_derecha'): 10,
        ('meta', 'ir_derecha'): 0,
        ('s1', 'quedarse'): -1,
        ('s2', 'quedarse'): -1,
        ('s3', 'quedarse'): -1,
        ('meta', 'quedarse'): 0,
    }

    valores = iteracion_valores(estados, acciones, transiciones, recompensas, gamma=0.9)
    print("Valores óptimos (V*) por estado:")
    for s, v in valores.items():
        print(f"   V({s}): {v:.2f}")