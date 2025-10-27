import random
import math

# ============================================================================
# 21. RED BAYESIANA DINÁMICA: FILTRADO DE PARTÍCULAS
# ============================================================================

def filtrado_particulas(observaciones, transicion_func, sensor_func, 
                        inicial_func, num_particulas=1000):
    """
    Filtrado de partículas (Sequential Monte Carlo)
    Args:
        observaciones: lista de observaciones
        transicion_func: función que muestrea nuevo estado dado estado previo
        sensor_func: función que da P(obs|estado)
        inicial_func: función que muestrea una partícula inicial
        num_particulas: número de partículas
    Returns:
        lista de conjuntos de partículas filtradas
    """
    # Inicializar partículas
    particulas = [{'estado': inicial_func(), 'peso': 1.0/num_particulas} 
                  for _ in range(num_particulas)]
    
    historia_particulas = [list(particulas)]
    
    for obs in observaciones:
        nuevas_particulas = []
        
        # 1. Predicción: mover partículas según modelo de transición
        for p in particulas:
            nuevo_estado = transicion_func(p['estado'])
            nuevas_particulas.append({'estado': nuevo_estado, 'peso': p['peso']})
        
        particulas = nuevas_particulas
        
        # 2. Actualización: ponderar por verosimilitud de observación
        suma_pesos = 0
        for p in particulas:
            p['peso'] *= sensor_func(obs, p['estado'])
            suma_pesos += p['peso']
        
        # 3. Normalizar pesos
        if suma_pesos > 0:
            for p in particulas:
                p['peso'] /= suma_pesos
        else:
             for p in particulas:
                p['peso'] = 1.0 / num_particulas # Resetear si pesos colapsan
        
        # 4. Re-muestreo (Resampling)
        # Calcular tamaño efectivo de muestra
        n_eff = 1.0 / sum(p['peso']**2 for p in particulas if p['peso'] > 0)
        
        if n_eff < num_particulas / 2:
            # Re-muestrear (muestreo de baja varianza o sistemático)
            estados = [p['estado'] for p in particulas]
            pesos = [p['peso'] for p in particulas]
            nuevos_estados = random.choices(estados, weights=pesos, k=num_particulas)
            particulas = [{'estado': e, 'peso': 1.0/num_particulas} 
                          for e in nuevos_estados]
        
        historia_particulas.append(list(particulas))
    
    return historia_particulas

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 21. Filtrado de Partículas ===\n")
    
    # Estimación de posición 1D (robot moviéndose a la derecha)
    
    def inicial_simple():
        """Muestrea estado inicial, ej. pos=0"""
        return random.gauss(0, 0.1) # Cerca de 0

    def transicion_simple(x):
        """Modelo de transición: x_t = x_{t-1} + 1 + ruido"""
        return x + 1.0 + random.gauss(0, 0.5)
    
    def sensor_simple(obs, estado):
        """Modelo de sensor: observación = estado + ruido"""
        # Verosimilitud gaussiana P(obs|estado)
        ruido_sensor = 1.0
        diff = obs - estado
        prob = math.exp(-0.5 * (diff**2) / (ruido_sensor**2))
        return prob + 1e-9 # Evitar prob 0
    
    # Observaciones ruidosas de un objeto moviéndose
    obs_particulas = [1.1, 1.9, 3.2, 4.0, 5.1]
    
    particulas_hist = filtrado_particulas(obs_particulas, transicion_simple, 
                                          sensor_simple, inicial_simple,
                                          num_particulas=1000)
    
    print(f"   Observaciones: {obs_particulas}")
    print(f"   Estimaciones (media ponderada de partículas):")
    
    for i, particulas in enumerate(particulas_hist):
        if i == 0:
            media = sum(p['estado'] * p['peso'] for p in particulas)
            print(f"   Tiempo {i} (Inicial): {media:.2f}")
        else:
            media = sum(p['estado'] * p['peso'] for p in particulas)
            print(f"   Tiempo {i} (Obs: {obs_particulas[i-1]}): {media:.2f}")