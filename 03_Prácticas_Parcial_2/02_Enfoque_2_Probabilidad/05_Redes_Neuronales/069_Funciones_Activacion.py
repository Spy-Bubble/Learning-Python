import math
import numpy as np # Útil para softmax y operaciones vectoriales

# ============================================================================
# 32. FUNCIONES DE ACTIVACIÓN
# ============================================================================

def funcion_escalon(x):
    """Función escalón (step function)"""
    return 1 if x >= 0 else 0


def funcion_sigmoide(x):
    """Función sigmoide (logística)"""
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0 if x < 0 else 1


def derivada_sigmoide(x):
    """Derivada de la función sigmoide"""
    s = funcion_sigmoide(x)
    return s * (1 - s)


def funcion_tanh(x):
    """Función tangente hiperbólica"""
    return math.tanh(x)


def derivada_tanh(x):
    """Derivada de tanh"""
    t = math.tanh(x)
    return 1 - t**2


def funcion_relu(x):
    """Rectified Linear Unit"""
    return max(0, x)


def derivada_relu(x):
    """Derivada de ReLU"""
    return 1 if x > 0 else 0


def funcion_leaky_relu(x, alpha=0.01):
    """Leaky ReLU"""
    return x if x > 0 else alpha * x


def derivada_leaky_relu(x, alpha=0.01):
     """Derivada de Leaky ReLU"""
     return 1 if x > 0 else alpha


def funcion_softmax(vector):
    """
    Función softmax para clasificación multiclase
    Args:
        vector: lista o array numpy de valores (logits)
    Returns:
        lista de probabilidades normalizadas
    """
    # Usar numpy para estabilidad numérica
    vector_np = np.array(vector)
    # Restar el máximo para evitar overflow en exp()
    exp_vals = np.exp(vector_np - np.max(vector_np))
    suma = np.sum(exp_vals)
    return (exp_vals / suma).tolist()

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 32. Funciones de Activación ===\n")
    
    x_vals = [-2, -1, 0, 1, 2]
    print(f"   Valores de entrada (x): {x_vals}\n")
    
    print("--- Salidas ---")
    print(f"   Escalón: {[funcion_escalon(x) for x in x_vals]}")
    print(f"   Sigmoide: {[f'{funcion_sigmoide(x):.3f}' for x in x_vals]}")
    print(f"   Tanh:     {[f'{funcion_tanh(x):.3f}' for x in x_vals]}")
    print(f"   ReLU:     {[funcion_relu(x) for x in x_vals]}")
    print(f"   Leaky ReLU: {[f'{funcion_leaky_relu(x):.3f}' for x in x_vals]}\n")
    
    print("--- Derivadas (evaluadas en x) ---")
    print(f"   d(Sigmoide)/dx: {[f'{derivada_sigmoide(x):.3f}' for x in x_vals]}")
    print(f"   d(Tanh)/dx:     {[f'{derivada_tanh(x):.3f}' for x in x_vals]}")
    print(f"   d(ReLU)/dx:     {[derivada_relu(x) for x in x_vals]}")
    print(f"   d(Leaky ReLU)/dx: {[f'{derivada_leaky_relu(x):.3f}' for x in x_vals]}\n")
    
    print("--- Softmax ---")
    logits = [1.0, 2.0, 0.5]
    probs = funcion_softmax(logits)
    print(f"   Logits: {logits}")
    print(f"   Probabilidades Softmax: {[f'{p:.3f}' for p in probs]}")
    print(f"   Suma: {sum(probs):.1f}")