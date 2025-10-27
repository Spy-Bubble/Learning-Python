# ============================================================================
# 32. TEORÍA DE JUEGOS: EQUILIBRIOS Y MECANISMOS
# ============================================================================

def equilibrio_nash_puro(matriz_pagos_j1, matriz_pagos_j2):
    """
    Encuentra equilibrios de Nash en estrategias puras
    Args:
        matriz_pagos_j1: matriz (lista de listas) de pagos del jugador 1
        matriz_pagos_j2: matriz (lista de listas) de pagos del jugador 2
    Returns:
        lista de equilibrios (fila, columna)
    """
    equilibrios = []
    filas = len(matriz_pagos_j1)
    columnas = len(matriz_pagos_j1[0])
    
    for i in range(filas):
        for j in range(columnas):
            # Obtener pago de J1 en (i, j)
            pago_j1 = matriz_pagos_j1[i][j]
            
            # Verificar si J1 no quiere desviarse de fila i (dada columna j)
            es_mejor_j1 = True
            for k in range(filas):
                if matriz_pagos_j1[k][j] > pago_j1:
                    es_mejor_j1 = False
                    break
            
            if not es_mejor_j1:
                continue
                
            # Obtener pago de J2 en (i, j)
            pago_j2 = matriz_pagos_j2[i][j]
            
            # Verificar si J2 no quiere desviarse de columna j (dada fila i)
            es_mejor_j2 = True
            for k in range(columnas):
                if matriz_pagos_j2[i][k] > pago_j2:
                    es_mejor_j2 = False
                    break
            
            if es_mejor_j1 and es_mejor_j2:
                equilibrios.append((i, j))
    
    return equilibrios


def estrategia_minimax(matriz_pagos_j1):
    """
    Encuentra estrategia minimax para juegos de suma cero (Punto de silla)
    Args:
        matriz_pagos_j1: matriz de pagos del jugador maximizador (J1)
                       (Se asume que el pago de J2 es -pago de J1)
    Returns:
        (mejor_fila, mejor_columna, valor) o None si no hay punto de silla
    """
    filas = len(matriz_pagos_j1)
    columnas = len(matriz_pagos_j1[0])
    
    # 1. Encontrar los mínimos de cada fila (lo peor para J1 en cada opción)
    minimos_fila = []
    for i in range(filas):
        minimos_fila.append(min(matriz_pagos_j1[i]))
    
    # 2. Encontrar los máximos de cada columna (lo peor para J2 en cada opción)
    maximos_columna = []
    for j in range(columnas):
        max_en_columna = max(matriz_pagos_j1[i][j] for i in range(filas))
        maximos_columna.append(max_en_columna)
        
    # 3. J1 elige el "maximin"
    max_min = max(minimos_fila)
    
    # 4. J2 elige el "minimax"
    min_max = min(maximos_columna)
    
    # Si coinciden, hay un punto de silla (equilibrio)
    if max_min == min_max:
        fila = minimos_fila.index(max_min)
        columna = maximos_columna.index(min_max)
        return (fila, columna, max_min)
    
    return None

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 32. Teoría de Juegos ===\n")
    
    print("1. Equilibrio de Nash (Dilema del Prisionero):")
    # J1: 0=Cooperar, 1=Traicionar
    # J2: 0=Cooperar, 1=Traicionar
    
    # Pagos J1:
    #      J2(C)  J2(T)
    # J1(C) [ 3 ,   0 ]
    # J1(T) [ 5 ,   1 ]
    pagos_j1 = [
        [3, 0],
        [5, 1]
    ]
    
    # Pagos J2:
    #      J2(C)  J2(T)
    # J1(C) [ 3 ,   5 ]
    # J1(T) [ 0 ,   1 ]
    pagos_j2 = [
        [3, 5],
        [0, 1]
    ]
    
    equilibrios = equilibrio_nash_puro(pagos_j1, pagos_j2)
    print(f"   Equilibrios de Nash (fila, col): {equilibrios}")
    print("   (1,1) = (Traicionar, Traicionar)\n")

    print("2. Estrategia Minimax (Juego de suma cero):")
    # Pagos para J1 (Filas)
    pagos_minimax = [
        [ 3, -1,  2],
        [ 1,  2,  4],
        [-2,  0,  1]
    ]
    
    resultado = estrategia_minimax(pagos_minimax)
    if resultado:
        print(f"   Punto de silla encontrado en (fila, col): ({resultado[0]}, {resultado[1]})")
        print(f"   Valor del juego: {resultado[2]}")
    else:
        print("   No se encontró punto de silla (requiere estrategias mixtas).")