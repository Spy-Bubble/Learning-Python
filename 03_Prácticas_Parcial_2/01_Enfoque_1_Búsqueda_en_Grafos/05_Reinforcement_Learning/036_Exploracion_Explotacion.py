import random
import math

# ============================================================================
# 36. EXPLORACIÓN VS. EXPLOTACIÓN
# ============================================================================

def ucb1(Q, N, estado, acciones, c=2):
    """
    Upper Confidence Bound para balancear exploración/explotación
    Args:
        Q: Q-valores estimados {(estado, accion): valor}
        N: contador de visitas {(estado, accion): conteo}
        estado: estado actual
        acciones: acciones posibles
        c: constante de exploración
    Returns:
        acción seleccionada
    """
    # Total de visitas a este *estado* (sumando visitas a sus acciones)
    total_visitas_estado = sum(N.get((estado, a), 0) for a in acciones)
    
    if total_visitas_estado == 0:
        return random.choice(acciones) # Explorar si el estado es nuevo
    
    mejor_accion = None
    mejor_ucb = float('-inf')
    
    for a in acciones:
        n_a = N.get((estado, a), 0)
        
        if n_a == 0:
            return a  # Priorizar acciones no exploradas en este estado
        
        q_valor = Q.get((estado, a), 0)
        bonus_exploracion = c * math.sqrt(math.log(total_visitas_estado) / n_a)
        ucb = q_valor + bonus_exploracion
        
        if ucb > mejor_ucb:
            mejor_ucb = ucb
            mejor_accion = a
    
    return mejor_accion


def thompson_sampling(exitos, intentos, acciones):
    """
    Thompson Sampling para bandidos multi-brazo
    Args:
        exitos: dict {accion: num_exitos}
        intentos: dict {accion: num_intentos}
        acciones: lista de acciones
    Returns:
        acción seleccionada
    """
    mejor_accion = None
    mejor_muestra = -1
    
    for a in acciones:
        # Usar Beta(1, 1) como prior si no hay datos
        num_exitos = exitos.get(a, 0)
        num_fracasos = intentos.get(a, 0) - num_exitos
        
        alpha = num_exitos + 1
        beta = num_fracasos + 1
        
        # Muestrear de distribución Beta
        muestra = random.betavariate(alpha, beta)
        
        if muestra > mejor_muestra:
            mejor_muestra = muestra
            mejor_accion = a
    
    return mejor_accion


def epsilon_decreciente(episodio, epsilon_inicial=1.0, epsilon_final=0.01, decay=0.995):
    """
    Estrategia de exploración con epsilon decreciente
    Args:
        episodio: número de episodio actual
        epsilon_inicial: epsilon al inicio
        epsilon_final: epsilon mínimo
        decay: tasa de decaimiento
    Returns:
        epsilon actual
    """
    epsilon = epsilon_inicial * (decay ** episodio)
    return max(epsilon_final, epsilon)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 36. Estrategias de Exploración vs. Explotación ===\n")
    
    # Ejemplo de UCB1
    print("1. Upper Confidence Bound (UCB1):")
    Q_test = {((0, 0), 'derecha'): 5.0, ((0, 0), 'abajo'): 3.0}
    N_test = {((0, 0), 'derecha'): 10, ((0, 0), 'abajo'): 5}
    accion_ucb = ucb1(Q_test, N_test, (0, 0), ['arriba', 'abajo', 'izquierda', 'derecha'], c=2)
    print(f"   Q(derecha)=5 (N=10), Q(abajo)=3 (N=5)")
    print(f"   Acción seleccionada por UCB1: {accion_ucb}")
    print("   (Probablemente 'arriba' o 'izquierda' por N=0, o 'abajo' por bonus de exploración)\n")

    # Ejemplo de Thompson Sampling
    print("2. Thompson Sampling (Bandidos):")
    exitos = {'A': 80, 'B': 6, 'C': 40}
    intentos = {'A': 100, 'B': 10, 'C': 100}
    accion_ts = thompson_sampling(exitos, intentos, ['A', 'B', 'C'])
    print(f"   Tasas de éxito: A=80%, B=60%, C=40%")
    print(f"   Acción seleccionada (basada en muestreo Beta): {accion_ts}\n")

    # Ejemplo de Epsilon Decreciente
    print("3. Epsilon Decreciente:")
    print(f"   Epsilon en episodio 0: {epsilon_decreciente(0):.3f}")
    print(f"   Epsilon en episodio 100: {epsilon_decreciente(100):.3f}")
    print(f"   Epsilon en episodio 500: {epsilon_decreciente(500):.3f}")