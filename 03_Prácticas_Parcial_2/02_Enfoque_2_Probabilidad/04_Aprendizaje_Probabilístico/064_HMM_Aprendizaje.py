import random

# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================

def inicializar_aleatorio(filas, columnas):
    """Inicializa matriz estocástica aleatoria (filas suman 1)"""
    matriz = []
    for _ in range(filas):
        fila = [random.random() for _ in range(columnas)]
        suma = sum(fila)
        if suma == 0: # Si todos son 0, hacer uniforme
             fila = [1.0 / columnas for _ in range(columnas)]
        else:
             fila = [x/suma for x in fila]
        matriz.append(fila)
    return matriz

# ============================================================================
# 27. MODELOS DE MARKOV OCULTOS (HMM con aprendizaje - Baum-Welch Conceptual)
# ============================================================================

def baum_welch(observaciones, num_estados, num_iteraciones=10):
    """
    Algoritmo Baum-Welch (EM para HMM) - Conceptual
    Aprende parámetros de HMM a partir de secuencias de observaciones.
    Args:
        observaciones: lista de secuencias de observaciones
        num_estados: número de estados ocultos
        num_iteraciones: iteraciones del algoritmo
    Returns:
        (transiciones, emisiones, inicial) aprendidos (simplificado)
    """
    print(f"Iniciando Baum-Welch (Conceptual) para {num_estados} estados...")
    
    # Obtener observaciones únicas (alfabeto)
    alfabeto = sorted(list(set(obs for seq in observaciones for obs in seq)))
    num_obs = len(alfabeto)
    obs_map = {obs: i for i, obs in enumerate(alfabeto)} # Mapeo obs -> índice
    
    # Inicialización aleatoria de parámetros
    print("   -> Inicializando parámetros aleatoriamente...")
    # trans[i][j] = P(estado j | estado i)
    transiciones = inicializar_aleatorio(num_estados, num_estados)
    # emis[i][k] = P(obs k | estado i)
    emisiones = inicializar_aleatorio(num_estados, num_obs)
    # inicial[i] = P(estado i al inicio)
    inicial_raw = [random.random() for _ in range(num_estados)]
    suma_inicial = sum(inicial_raw)
    inicial = [x/suma_inicial for x in inicial_raw]
    
    for iter_num in range(num_iteraciones):
        print(f"   Iteración {iter_num + 1}/{num_iteraciones}")
        
        # --- E-step (Conceptual) ---
        # Para cada secuencia de observación:
        #   Calcular alphas (forward) y betas (backward)
        #   Calcular gammas ( P(X_t=i | obs) ) y xis ( P(X_t=i, X_{t+1}=j | obs) )
        print("      -> E-Step: Calcular expectativas (alphas, betas, gammas, xis)")
        # (Implementación completa requiere forward_backward de 055)
        
        # --- M-step (Conceptual) ---
        # Actualizar parámetros basados en las expectativas acumuladas:
        #   inicial[i] = gamma_0(i) promedio
        #   trans[i][j] = Suma_t xi_t(i,j) / Suma_t gamma_t(i)
        #   emis[i][k] = Suma_{t donde obs=k} gamma_t(i) / Suma_t gamma_t(i)
        print("      -> M-Step: Maximizar parámetros (transiciones, emisiones, inicial)")
        # (Implementación completa requiere acumular y re-estimar)
        
        # Simular una pequeña actualización aleatoria para mostrar cambio
        transiciones = inicializar_aleatorio(num_estados, num_estados)
        emisiones = inicializar_aleatorio(num_estados, num_obs)

    print("Baum-Welch (Conceptual) finalizado.")
    return transiciones, emisiones, inicial

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 27. Aprendizaje de HMM (Baum-Welch Conceptual) ===\n")
    
    # Ejemplo: Moneda sesgada (quizás dos monedas)
    observaciones_moneda = [
        ['C', 'X', 'C', 'X', 'C'],
        ['X', 'X', 'C', 'C', 'X'],
        ['C', 'C', 'C', 'X', 'X'],
    ]
    
    num_estados_ocultos = 2 # Intentar descubrir si hay 2 monedas
    
    # Ejecutar Baum-Welch (conceptual)
    trans, emis, init = baum_welch(observaciones_moneda, num_estados_ocultos, num_iteraciones=3)
    
    print("\n   Parámetros 'aprendidos' (finales aleatorios en esta versión):")
    print(f"   Inicial: {[f'{p:.2f}' for p in init]}")
    print(f"   Transiciones:")
    for fila in trans: print(f"      {[f'{p:.2f}' for p in fila]}")
    print(f"   Emisiones:")
    for fila in emis: print(f"      {[f'{p:.2f}' for p in fila]}")