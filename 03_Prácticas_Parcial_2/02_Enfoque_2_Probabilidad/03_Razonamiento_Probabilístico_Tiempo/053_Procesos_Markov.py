# ============================================================================
# 16. HIPÓTESIS DE MARKOV: PROCESOS DE MARKOV
# ============================================================================

class ProcesoMarkov:
    """
    Proceso de Markov de primer orden (Cadena de Markov)
    """
    def __init__(self, estados, transiciones, dist_inicial):
        """
        Args:
            estados: lista de estados posibles
            transiciones: dict {(s, s'): P(s'|s)}
            dist_inicial: dict {estado: probabilidad}
        """
        self.estados = estados
        self.transiciones = transiciones
        self.dist_actual = dist_inicial
    
    def avanzar(self):
        """Avanza un paso de tiempo"""
        nueva_dist = {}
        
        for s_nuevo in self.estados:
            # P(s_nuevo en t) = Suma_s [ P(s_nuevo | s) * P(s en t-1) ]
            prob = sum(
                self.dist_actual.get(s, 0) * self.transiciones.get((s, s_nuevo), 0)
                for s in self.estados
            )
            nueva_dist[s_nuevo] = prob
        
        self.dist_actual = nueva_dist
        return nueva_dist
    
    def predecir(self, pasos):
        """Predice distribución después de n pasos"""
        dist_temporal = dict(self.dist_actual)
        for _ in range(pasos):
            dist_temporal = self.avanzar() # Re-usar avanzar
            self.dist_actual = dist_temporal # Actualizar estado interno
        return self.dist_actual


def verificar_propiedad_markov(secuencia, transiciones):
    """
    Verifica si una secuencia cumple la propiedad de Markov
    P(X_t|X_0,...,X_{t-1}) = P(X_t|X_{t-1})
    Args:
        secuencia: lista de estados observados
        transiciones: probabilidades de transición
    Returns:
        True si satisface la propiedad (simplificado)
    """
    # En práctica, esto se verificaría con tests estadísticos
    # Aquí verificamos que las transiciones observadas sean "posibles"
    
    for i in range(1, len(secuencia)):
        estado_prev = secuencia[i-1]
        estado_actual = secuencia[i]
        
        # Verificar que la transición exista y tenga prob > 0
        if transiciones.get((estado_prev, estado_actual), 0) == 0:
            print(f"Transición {estado_prev}->{estado_actual} no es posible.")
            return False
    
    return True

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 16. Procesos de Markov ===\n")

    estados_clima = ['sol', 'lluvia']
    transiciones_clima = {
        ('sol', 'sol'): 0.8,
        ('sol', 'lluvia'): 0.2,
        ('lluvia', 'sol'): 0.4,
        ('lluvia', 'lluvia'): 0.6
    }
    inicial_clima = {'sol': 1.0, 'lluvia': 0.0} # Empezar en sol
    
    pm = ProcesoMarkov(estados_clima, transiciones_clima, inicial_clima)
    
    print(f"   Distribución inicial (t=0): {pm.dist_actual}")
    
    pm.avanzar()
    print(f"   Distribución (t=1): {pm.dist_actual}")
    
    pm.avanzar()
    print(f"   Distribución (t=2): {pm.dist_actual}")
    
    # Predecir 5 pasos más
    pm.predecir(5)
    print(f"   Distribución (t=7): {pm.dist_actual}")
    print("   (Nótese cómo converge a la dist. estacionaria [0.667, 0.333])\n")
    
    # Verificar propiedad
    secuencia_valida = ['sol', 'sol', 'lluvia', 'sol']
    print(f"   ¿Secuencia {secuencia_valida} es Markoviana? {verificar_propiedad_markov(secuencia_valida, transiciones_clima)}")