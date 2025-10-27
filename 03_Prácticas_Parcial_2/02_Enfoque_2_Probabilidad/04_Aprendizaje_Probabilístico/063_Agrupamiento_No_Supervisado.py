import math

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def distancia_euclidiana(p1, p2):
    """Distancia euclidiana entre dos puntos (listas o tuplas)"""
    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def distancia_clusters(datos, indices_cluster1, indices_cluster2, linkage='average'):
    """Calcula distancia entre dos clusters"""
    distancias = []
    for i in indices_cluster1:
        for j in indices_cluster2:
            p1 = datos[i]
            p2 = datos[j]
            # Simplificado para 1D o N-D
            dist = abs(p1 - p2) if isinstance(p1, (int, float)) else distancia_euclidiana(p1, p2)
            distancias.append(dist)
    
    if not distancias: return float('inf')

    if linkage == 'average':
        return sum(distancias) / len(distancias)
    elif linkage == 'single':
        return min(distancias)
    elif linkage == 'complete':
        return max(distancias)
    else: # Default a average
        return sum(distancias) / len(distancias)

# ============================================================================
# 26. AGRUPAMIENTO NO SUPERVISADO (Jerárquico)
# ============================================================================

def agrupamiento_jerarquico(datos, num_clusters, linkage='average'):
    """
    Clustering jerárquico aglomerativo
    Args:
        datos: lista de puntos (1D o N-D)
        num_clusters: número de clusters deseados
        linkage: tipo de enlace ('single', 'complete', 'average')
    Returns:
        asignación de clusters (lista de IDs de cluster)
    """
    n = len(datos)
    if n == 0: return []
    
    # Inicializar cada punto como su propio cluster (índices)
    clusters = [[i] for i in range(n)]
    
    while len(clusters) > num_clusters:
        # Encontrar par de clusters más cercanos
        min_dist = float('inf')
        merge_idx = (-1, -1)
        
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = distancia_clusters(datos, clusters[i], clusters[j], linkage)
                if dist < min_dist:
                    min_dist = dist
                    merge_idx = (i, j)
        
        # Fusionar clusters
        i, j = merge_idx
        clusters[i].extend(clusters[j])
        del clusters[j]
    
    # Crear asignación final
    asignacion = [0] * n
    for cluster_id, cluster_indices in enumerate(clusters):
        for punto_idx in cluster_indices:
            asignacion[punto_idx] = cluster_id
            
    return asignacion

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 26. Agrupamiento Jerárquico ===\n")
    
    # Datos 1D
    datos_1d = [1, 2, 3, 8, 9, 10, 15, 16]
    print(f"   Datos 1D: {datos_1d}")
    
    asignacion_1d = agrupamiento_jerarquico(datos_1d, num_clusters=3, linkage='average')
    print(f"   Asignación (k=3, average linkage): {asignacion_1d}\n")
    
    # Datos 2D
    datos_2d = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]
    print(f"   Datos 2D: {datos_2d}")
    
    asignacion_2d = agrupamiento_jerarquico(datos_2d, num_clusters=2, linkage='single')
    print(f"   Asignación (k=2, single linkage): {asignacion_2d}")