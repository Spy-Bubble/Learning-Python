import random
from math import comb # comb (combinatoria) es necesaria para binomial

# ============================================================================
# 4. DISTRIBUCIÓN DE PROBABILIDAD
# ============================================================================

class DistribucionProbabilidad:
    """
    Representa una distribución de probabilidad discreta
    """
    def __init__(self, valores, probabilidades):
        """
        Args:
            valores: lista de valores posibles
            probabilidades: probabilidades correspondientes
        """
        if len(valores) != len(probabilidades):
            raise ValueError("Valores y probabilidades deben tener la misma longitud")
            
        total = sum(probabilidades)
        if total == 0:
             # Si se inicializa con [0, 0], crear uniforme
            num_val = len(valores)
            self.distribucion = {v: 1.0/num_val for v in valores}
        else:
            # Normalizar automáticamente
            self.distribucion = {
                v: p/total for v, p in zip(valores, probabilidades)
            }
    
    def prob(self, valor):
        """Obtiene probabilidad de un valor"""
        return self.distribucion.get(valor, 0)
    
    def muestra(self):
        """Genera una muestra aleatoria de la distribución"""
        valores = list(self.distribucion.keys())
        probs = list(self.distribucion.values())
        return random.choices(valores, weights=probs, k=1)[0]
    
    def esperanza(self):
        """Calcula el valor esperado (media)"""
        # Asegurarse de que los valores sean numéricos
        try:
            return sum(v * p for v, p in self.distribucion.items())
        except TypeError:
            print("Advertencia: No se puede calcular la esperanza de valores no numéricos.")
            return None
    
    def varianza(self):
        """Calcula la varianza"""
        media = self.esperanza()
        if media is None:
            return None
        return sum(p * (v - media)**2 for v, p in self.distribucion.items())


def distribucion_binomial(n, p, k):
    """
    Probabilidad binomial: P(X=k) en n intentos con probabilidad p
    Args:
        n: número de intentos
        p: probabilidad de éxito
        k: número de éxitos deseados
    Returns:
        probabilidad
    """
    if not (0 <= p <= 1):
        raise ValueError("p (probabilidad) debe estar entre 0 y 1")
    if k < 0 or k > n:
        return 0 # Es imposible
    
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 4. Distribución de Probabilidad ===\n")
    
    # Ejemplo 1: Clase DistribucionProbabilidad (dado cargado)
    # Se inicializa con pesos [1, 1, 1, 1, 1, 5] -> P(6) = 5/10 = 0.5
    dist_dado_cargado = DistribucionProbabilidad(
        [1, 2, 3, 4, 5, 6], 
        [1, 1, 1, 1, 1, 5]
    )
    print("Distribución de un dado cargado (pesos [1,1,1,1,1,5]):")
    print(f"   P(3) = {dist_dado_cargado.prob(3):.3f}")
    print(f"   P(6) = {dist_dado_cargado.prob(6):.3f}")
    print(f"   Valor esperado: {dist_dado_cargado.esperanza():.2f}")
    print(f"   Muestra aleatoria: {dist_dado_cargado.muestra()}\n")
    
    # Ejemplo 2: Distribución Binomial
    print("Distribución Binomial:")
    # Probabilidad de 3 caras (k=3) en 5 lanzamientos (n=5)
    p_3_caras = distribucion_binomial(n=5, p=0.5, k=3)
    print(f"   P(3 caras en 5 lanzamientos) = {p_3_caras:.3f}")