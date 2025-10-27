import random
import math

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def gaussiana(x, media, varianza):
    """Densidad de probabilidad gaussiana"""
    if varianza <= 0: return 0 # Evitar división por cero o log de negativo
    denominador = math.sqrt(2 * math.pi * varianza)
    exponente = -0.5 * ((x - media) ** 2) / varianza
    return (1.0 / denominador) * math.exp(exponente)

# ============================================================================
# 25. ALGORITMO EM (EXPECTATION-MAXIMIZATION)
# ============================================================================

def algoritmo_em_gaussiano(datos, num_componentes, max_iter=100, tolerancia=0.001):
    """
    EM para mezcla de gaussianas (1D)
    Args:
        datos: lista de puntos (1D)
        num_componentes: número de gaussianas en la mezcla
        max_iter: iteraciones máximas
        tolerancia: criterio de convergencia
    Returns:
        (medias, varianzas, pesos) de las gaussianas
    """
    n = len(datos)
    if n == 0: return [], [], []
    
    # Inicialización aleatoria (mejoras posibles: k-means)
    min_d, max_d = min(datos), max(datos)
    medias = [min_d + (max_d - min_d) * random.random() for _ in range(num_componentes)]
    varianzas = [1.0] * num_componentes
    pesos = [1.0/num_componentes] * num_componentes
    
    log_likelihood_old = -float('inf')

    for iteracion in range(max_iter):
        # --- E-step: calcular responsabilidades ---
        # responsabilidades[i][k] = P(componente k | dato i)
        responsabilidades = [[0.0] * num_componentes for _ in range(n)]
        log_likelihood_new = 0

        for i in range(n):
            x = datos[i]
            probs_no_norm = []
            for k in range(num_componentes):
                # P(x | componente k) * P(componente k)
                prob = pesos[k] * gaussiana(x, medias[k], varianzas[k])
                probs_no_norm.append(prob)
            
            suma_probs = sum(probs_no_norm)
            log_likelihood_new += math.log(suma_probs) if suma_probs > 0 else -float('inf')

            if suma_probs > 0:
                for k in range(num_componentes):
                    responsabilidades[i][k] = probs_no_norm[k] / suma_probs
        
        # --- M-step: actualizar parámetros ---
        medias_nuevas = [0.0] * num_componentes
        varianzas_nuevas = [0.0] * num_componentes
        pesos_nuevos = [0.0] * num_componentes
        
        for k in range(num_componentes):
            # Peso efectivo N_k
            n_k = sum(responsabilidades[i][k] for i in range(n))
            
            if n_k > 1e-6: # Evitar división por cero
                # Nueva Media
                media_k = sum(responsabilidades[i][k] * datos[i] for i in range(n)) / n_k
                medias_nuevas[k] = media_k
                
                # Nueva Varianza
                varianza_k = sum(responsabilidades[i][k] * (datos[i] - media_k)**2 for i in range(n)) / n_k
                varianzas_nuevas[k] = max(varianza_k, 1e-6) # Evitar varianza 0
                
                # Nuevo Peso
                pesos_nuevos[k] = n_k / n
            else: # Si un componente colapsa, re-inicializar (o mantener)
                medias_nuevas[k] = medias[k]
                varianzas_nuevas[k] = varianzas[k]
                pesos_nuevos[k] = 0.0

        # Renormalizar pesos por si acaso
        suma_pesos = sum(pesos_nuevos)
        if suma_pesos > 0:
             pesos_nuevos = [p / suma_pesos for p in pesos_nuevos]

        # Verificar convergencia (usando log-likelihood)
        if abs(log_likelihood_new - log_likelihood_old) < tolerancia:
            break
        
        medias = medias_nuevas
        varianzas = varianzas_nuevas
        pesos = pesos_nuevos
        log_likelihood_old = log_likelihood_new
        
    return medias, varianzas, pesos

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 25. Algoritmo EM (Mezcla de Gaussianas) ===\n")
    
    # Generar datos de dos gaussianas
    datos1 = [random.gauss(2, 1) for _ in range(50)]
    datos2 = [random.gauss(8, 1.5) for _ in range(50)]
    datos_mezcla = datos1 + datos2
    random.shuffle(datos_mezcla)

    print(f"   Datos generados de dos gaussianas (media ~2 y ~8)")
    
    num_componentes = 2
    medias, varianzas, pesos = algoritmo_em_gaussiano(datos_mezcla, num_componentes, max_iter=50)
    
    print(f"\n   Parámetros estimados por EM para {num_componentes} componentes:")
    for k in range(num_componentes):
        print(f"      Componente {k+1}: Media={medias[k]:.2f}, Varianza={varianzas[k]:.2f}, Peso={pesos[k]:.2f}")