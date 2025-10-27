import random
import math

# ============================================================================
# FUNCIÓN AUXILIAR
# ============================================================================
def distancia_euclidiana(v1, v2):
    """Calcula distancia euclidiana entre dos vectores"""
    return math.sqrt(sum((a - b)**2 for a, b in zip(v1, v2)))

# ============================================================================
# 37. MAPAS AUTOORGANIZADOS DE KOHONEN (SOM)
# ============================================================================

class MapaKohonen:
    """
    Mapa autoorganizado de Kohonen (Self-Organizing Map - SOM)
    """
    def __init__(self, filas, columnas, dim_entrada, tasa_inicial=0.5, radio_inicial=None):
        self.filas = filas
        self.columnas = columnas
        self.dim_entrada = dim_entrada
        self.tasa_inicial = tasa_inicial
        # Radio inicial por defecto: mitad de la dimensión más grande del mapa
        self.radio_inicial = radio_inicial if radio_inicial is not None else max(filas, columnas) / 2.0
        
        # Inicializar pesos aleatoriamente (vector por cada neurona del mapa)
        self.pesos = [[[random.random() for _ in range(dim_entrada)] 
                       for _ in range(columnas)] 
                      for _ in range(filas)]
    
    def encontrar_bmu(self, entrada):
        """
        Encuentra la Best Matching Unit (BMU) - neurona ganadora
        Args:
            entrada: vector de entrada
        Returns:
            (fila, columna) de la BMU
        """
        min_dist = float('inf')
        bmu_coords = (0, 0)
        
        for i in range(self.filas):
            for j in range(self.columnas):
                dist = distancia_euclidiana(entrada, self.pesos[i][j])
                if dist < min_dist:
                    min_dist = dist
                    bmu_coords = (i, j)
        
        return bmu_coords
    
    def _funcion_vecindad_gaussiana(self, dist_mapa_sq, radio_sq):
        """Función de vecindad gaussiana (usa distancias al cuadrado)"""
        return math.exp(-dist_mapa_sq / (2 * radio_sq))
    
    def entrenar(self, datos, num_iteraciones):
        """
        Entrena el mapa autoorganizado
        Args:
            datos: lista de vectores de entrada
            num_iteraciones: iteraciones de entrenamiento
        """
        if not datos: return

        time_constant = num_iteraciones / math.log(self.radio_inicial) if self.radio_inicial > 0 else num_iteraciones

        for iteracion in range(num_iteraciones):
            # Decaimiento exponencial de parámetros
            tasa = self.tasa_inicial * math.exp(-iteracion / num_iteraciones)
            radio = self.radio_inicial * math.exp(-iteracion / time_constant)
            radio_sq = radio**2
            
            # Tomar muestra aleatoria de los datos
            entrada = random.choice(datos)
            
            # Encontrar BMU
            bmu_i, bmu_j = self.encontrar_bmu(entrada)
            
            # Actualizar pesos de las neuronas en la vecindad de la BMU
            for i in range(self.filas):
                for j in range(self.columnas):
                    # Distancia a BMU en el mapa (al cuadrado)
                    dist_mapa_sq = (i - bmu_i)**2 + (j - bmu_j)**2
                    
                    # Calcular influencia (si está dentro del radio efectivo)
                    if radio_sq > 0 and dist_mapa_sq < (radio * 3)**2: # Optimización
                        influencia = self._funcion_vecindad_gaussiana(dist_mapa_sq, radio_sq)
                        
                        # Actualizar pesos W = W + tasa * influencia * (Entrada - W)
                        peso_actual = self.pesos[i][j]
                        for k in range(self.dim_entrada):
                            delta = tasa * influencia * (entrada[k] - peso_actual[k])
                            self.pesos[i][j][k] += delta
    
    def mapear(self, entrada):
        """Mapea una entrada a una posición (coordenadas) en el mapa"""
        return self.encontrar_bmu(entrada)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 37. Mapas Autoorganizados de Kohonen (SOM) ===\n")
    
    # Ejemplo: Agrupar colores (RGB)
    # Datos: colores aleatorios (vectores RGB entre 0 y 1)
    datos_colores = [[random.random(), random.random(), random.random()] 
                     for _ in range(100)]
    
    mapa_filas = 5
    mapa_cols = 5
    dim_entrada = 3 # R, G, B
    
    som = MapaKohonen(mapa_filas, mapa_cols, dim_entrada, tasa_inicial=0.6)
    
    print(f"   Creando SOM de {mapa_filas}x{mapa_cols} para datos de {dim_entrada} dimensiones.")
    print("   Entrenando SOM (puede tardar unos segundos)...")
    
    som.entrenar(datos_colores, num_iteraciones=1000)
    
    print("   Entrenamiento completado.\n")
    
    # Mapear algunos colores de prueba
    color_rojo = [1.0, 0.0, 0.0]
    color_verde = [0.0, 1.0, 0.0]
    color_azul = [0.0, 0.0, 1.0]
    color_blanco = [1.0, 1.0, 1.0]
    
    map_rojo = som.mapear(color_rojo)
    map_verde = som.mapear(color_verde)
    map_azul = som.mapear(color_azul)
    map_blanco = som.mapear(color_blanco)
    
    print("   Mapeo de colores en el SOM:")
    print(f"      Rojo ({color_rojo}) -> Neurona BMU: {map_rojo}")
    print(f"      Verde ({color_verde}) -> Neurona BMU: {map_verde}")
    print(f"      Azul ({color_azul}) -> Neurona BMU: {map_azul}")
    print(f"      Blanco ({color_blanco}) -> Neurona BMU: {map_blanco}")
    
    # (En una visualización, neuronas cercanas deberían tener colores similares)