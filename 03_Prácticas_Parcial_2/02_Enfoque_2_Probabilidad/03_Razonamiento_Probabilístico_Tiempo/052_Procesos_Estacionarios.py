import numpy as np # Importado en el original, aunque no se usa en estas funciones

# ============================================================================
# 15. PROCESOS ESTACIONARIOS
# ============================================================================

def es_proceso_estacionario(transiciones):
    """
    Verifica si un proceso tiene probabilidades de transición constantes
    Args:
        transiciones: dict {tiempo: {(estado, estado'): prob}}
    Returns:
        True si es estacionario
    """
    # Verificar que las transiciones no cambien con el tiempo
    tiempos = list(transiciones.keys())
    if len(tiempos) < 2:
        return True
    
    referencia = transiciones[tiempos[0]]
    
    for t in tiempos[1:]:
        if transiciones[t] != referencia:
            return False
    
    return True


def distribucion_estacionaria(matriz_transicion, epsilon=0.001, max_iter=1000):
    """
    Encuentra la distribución estacionaria de una cadena de Markov
    Args:
        matriz_transicion: dict {(estado_i, estado_j): probabilidad}
        epsilon: tolerancia de convergencia
        max_iter: iteraciones máximas
    Returns:
        distribución estacionaria
    """
    # Obtener estados únicos
    estados = set()
    for (s1, s2) in matriz_transicion.keys():
        estados.add(s1)
        estados.add(s2)
    estados = sorted(list(estados))
    
    if not estados:
        return {}
        
    # Inicializar distribución uniforme
    n = len(estados)
    dist = {s: 1.0/n for s in estados}
    
    for _ in range(max_iter):
        nueva_dist = {}
        
        # Aplicar transición: π' = π · P
        for s_j in estados:
            nueva_dist[s_j] = sum(
                dist[s_i] * matriz_transicion.get((s_i, s_j), 0)
                for s_i in estados
            )
        
        # Verificar convergencia
        cambio = sum(abs(nueva_dist[s] - dist[s]) for s in estados)
        dist = nueva_dist
        
        if cambio < epsilon:
            break
    
    return dist

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 15. Procesos Estacionarios ===\n")
    
    # Ejemplo 1: Es estacionario
    trans_t = {
        1: {('A', 'A'): 0.5, ('A', 'B'): 0.5},
        2: {('A', 'A'): 0.5, ('A', 'B'): 0.5}
    }
    print(f"   ¿Proceso 1 es estacionario? {es_proceso_estacionario(trans_t)}")
    
    # Ejemplo 2: No es estacionario
    trans_t_no_est = {
        1: {('A', 'A'): 0.5, ('A', 'B'): 0.5},
        2: {('A', 'A'): 0.4, ('A', 'B'): 0.6}
    }
    print(f"   ¿Proceso 2 es estacionario? {es_proceso_estacionario(trans_t_no_est)}\n")
    
    
    # Ejemplo 3: Distribución Estacionaria
    print("Distribución Estacionaria (Clima):")
    transiciones_clima = {
        ('sol', 'sol'): 0.8,
        ('sol', 'lluvia'): 0.2,
        ('lluvia', 'sol'): 0.4,
        ('lluvia', 'lluvia'): 0.6
    }
    dist_est = distribucion_estacionaria(transiciones_clima)
    print(f"   Distribución estacionaria del clima:")
    for estado, prob in dist_est.items():
        print(f"      {estado}: {prob:.3f}")
    # (Esperado: sol=0.667, lluvia=0.333)