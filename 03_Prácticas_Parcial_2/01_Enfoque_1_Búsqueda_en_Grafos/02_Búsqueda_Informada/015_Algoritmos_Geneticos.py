import random

# ============================================================================
# 15. ALGORITMOS GENÉTICOS
# ============================================================================

def algoritmo_genetico(funcion_fitness, tam_poblacion=50, tam_cromosoma=10, 
                       generaciones=100, prob_mutacion=0.01, prob_cruce=0.7):
    """
    Evolución de población mediante selección, cruce y mutación
    Args:
        funcion_fitness: función de aptitud a maximizar
        tam_poblacion: tamaño de la población
        tam_cromosoma: longitud de cada cromosoma (lista binaria)
        generaciones: número de generaciones
        prob_mutacion: probabilidad de mutación
        prob_cruce: probabilidad de cruce
    Returns:
        mejor cromosoma encontrado
    """
    # Generar población inicial aleatoria
    poblacion = [[random.randint(0, 1) for _ in range(tam_cromosoma)] 
                 for _ in range(tam_poblacion)]
    
    for _ in range(generaciones):
        # Evaluar fitness (asegurarse que los pesos no sean negativos)
        fitness_scores = [funcion_fitness(cromosoma) for cromosoma in poblacion]
        min_fitness = min(fitness_scores)
        # Ajustar pesos para que sean >= 0
        fitness_pesos = [(f - min_fitness) + 1e-6 for f in fitness_scores]

        # Selección por torneo/ruleta
        nueva_poblacion = []
        for _ in range(tam_poblacion):
            # Seleccionar 2 padres
            padres = random.choices(poblacion, weights=fitness_pesos, k=2)
            
            # Cruce
            if random.random() < prob_cruce:
                punto_cruce = random.randint(1, tam_cromosoma - 1)
                hijo = padres[0][:punto_cruce] + padres[1][punto_cruce:]
            else:
                hijo = padres[0][:]
            
            # Mutación
            for i in range(tam_cromosoma):
                if random.random() < prob_mutacion:
                    hijo[i] = 1 - hijo[i]
            
            nueva_poblacion.append(hijo)
        
        poblacion = nueva_poblacion
    
    # Retornar el mejor individuo
    return max(poblacion, key=funcion_fitness)

# ============================================================================
# EJEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("15. Algoritmo Genético:")
    
    # Fitness: contar número de 1s en cromosoma (problema "OneMax")
    def fitness_onemax(cromosoma):
        return sum(cromosoma)
    
    mejor = algoritmo_genetico(fitness_onemax, tam_poblacion=20, tam_cromosoma=10, 
                               generaciones=50)
    print(f"   Problema OneMax (maximizar 1s):")
    print(f"   Mejor cromosoma: {mejor}")
    print(f"   Fitness: {fitness_onemax(mejor)}")