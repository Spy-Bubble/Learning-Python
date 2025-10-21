"""
PERCEPCIÓN
Algoritmos 45-52: Visión por computadora y procesamiento de imágenes
"""

import random
import math
import numpy as np
from collections import defaultdict

# ============================================================================
# 45. GRÁFICOS POR COMPUTADOR
# ============================================================================

class Punto3D:
    """Representa un punto en espacio 3D"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


def proyeccion_perspectiva(punto3d, distancia_focal=500):
    """
    Proyección de perspectiva de 3D a 2D
    Args:
        punto3d: Punto3D
        distancia_focal: distancia de la cámara
    Returns:
        (x_2d, y_2d)
    """
    if punto3d.z == 0:
        punto3d.z = 0.001  # Evitar división por cero
    
    factor = distancia_focal / (distancia_focal + punto3d.z)
    x_2d = punto3d.x * factor
    y_2d = punto3d.y * factor
    
    return (x_2d, y_2d)


def rotacion_3d(punto, angulo_x=0, angulo_y=0, angulo_z=0):
    """
    Aplica rotación en 3D
    Args:
        punto: Punto3D
        angulo_x, angulo_y, angulo_z: ángulos de rotación en radianes
    Returns:
        Punto3D rotado
    """
    x, y, z = punto.x, punto.y, punto.z
    
    # Rotación alrededor de X
    if angulo_x != 0:
        cos_x, sin_x = math.cos(angulo_x), math.sin(angulo_x)
        y_nuevo = y * cos_x - z * sin_x
        z_nuevo = y * sin_x + z * cos_x
        y, z = y_nuevo, z_nuevo
    
    # Rotación alrededor de Y
    if angulo_y != 0:
        cos_y, sin_y = math.cos(angulo_y), math.sin(angulo_y)
        x_nuevo = x * cos_y + z * sin_y
        z_nuevo = -x * sin_y + z * cos_y
        x, z = x_nuevo, z_nuevo
    
    # Rotación alrededor de Z
    if angulo_z != 0:
        cos_z, sin_z = math.cos(angulo_z), math.sin(angulo_z)
        x_nuevo = x * cos_z - y * sin_z
        y_nuevo = x * sin_z + y * cos_z
        x, y = x_nuevo, y_nuevo
    
    return Punto3D(x, y, z)


def ray_tracing_simple(origen, direccion, esfera_centro, esfera_radio):
    """
    Ray tracing simple para detectar intersección con esfera
    Args:
        origen: punto de origen del rayo
        direccion: vector de dirección
        esfera_centro: centro de la esfera
        esfera_radio: radio de la esfera
    Returns:
        True si hay intersección
    """
    # Vector del origen al centro
    L = [esfera_centro[i] - origen[i] for i in range(3)]
    
    # Proyección de L sobre la dirección
    tca = sum(L[i] * direccion[i] for i in range(3))
    
    if tca < 0:
        return False
    
    # Distancia al cuadrado del centro a la línea del rayo
    d2 = sum(L[i]**2 for i in range(3)) - tca**2
    
    if d2 > esfera_radio**2:
        return False
    
    return True


# ============================================================================
# 46. PREPROCESADO: FILTROS
# ============================================================================

class Imagen:
    """Representa una imagen en escala de grises"""
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.pixeles = [[0 for _ in range(ancho)] for _ in range(alto)]
    
    def get_pixel(self, x, y):
        """Obtiene valor de pixel con comprobación de límites"""
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            return self.pixeles[y][x]
        return 0
    
    def set_pixel(self, x, y, valor):
        """Establece valor de pixel"""
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = max(0, min(255, valor))


def filtro_media(imagen, tam_kernel=3):
    """
    Aplica filtro de media (promedio) para suavizado
    Args:
        imagen: objeto Imagen
        tam_kernel: tamaño del kernel (3x3, 5x5, etc)
    Returns:
        nueva Imagen suavizada
    """
    resultado = Imagen(imagen.ancho, imagen.alto)
    offset = tam_kernel // 2
    
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            suma = 0
            contador = 0
            
            # Promediar vecindad
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    valor = imagen.get_pixel(x + kx, y + ky)
                    suma += valor
                    contador += 1
            
            resultado.set_pixel(x, y, suma // contador)
    
    return resultado


def filtro_mediana(imagen, tam_kernel=3):
    """
    Aplica filtro de mediana (reduce ruido sal y pimienta)
    Args:
        imagen: objeto Imagen
        tam_kernel: tamaño del kernel
    Returns:
        nueva Imagen filtrada
    """
    resultado = Imagen(imagen.ancho, imagen.alto)
    offset = tam_kernel // 2
    
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            valores = []
            
            # Recolectar valores de vecindad
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    valores.append(imagen.get_pixel(x + kx, y + ky))
            
            # Calcular mediana
            valores.sort()
            mediana = valores[len(valores) // 2]
            resultado.set_pixel(x, y, mediana)
    
    return resultado


def filtro_gaussiano(imagen, sigma=1.0):
    """
    Aplica filtro gaussiano
    Args:
        imagen: objeto Imagen
        sigma: desviación estándar
    Returns:
        Imagen suavizada
    """
    # Crear kernel gaussiano
    tam = int(6 * sigma) | 1  # Tamaño impar
    offset = tam // 2
    kernel = []
    suma_kernel = 0
    
    for y in range(-offset, offset + 1):
        fila = []
        for x in range(-offset, offset + 1):
            valor = math.exp(-(x**2 + y**2) / (2 * sigma**2))
            fila.append(valor)
            suma_kernel += valor
        kernel.append(fila)
    
    # Normalizar kernel
    kernel = [[v / suma_kernel for v in fila] for fila in kernel]
    
    # Aplicar convolución
    resultado = Imagen(imagen.ancho, imagen.alto)
    
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            suma = 0
            
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    pixel_val = imagen.get_pixel(x + kx, y + ky)
                    kernel_val = kernel[ky + offset][kx + offset]
                    suma += pixel_val * kernel_val
            
            resultado.set_pixel(x, y, int(suma))
    
    return resultado


# ============================================================================
# 47. DETECCIÓN DE ARISTAS Y SEGMENTACIÓN
# ============================================================================

def detector_sobel(imagen):
    """
    Detector de bordes de Sobel
    Args:
        imagen: objeto Imagen
    Returns:
        Imagen con bordes detectados
    """
    # Kernels de Sobel
    sobel_x = [[-1, 0, 1],
               [-2, 0, 2],
               [-1, 0, 1]]
    
    sobel_y = [[-1, -2, -1],
               [ 0,  0,  0],
               [ 1,  2,  1]]
    
    resultado = Imagen(imagen.ancho, imagen.alto)
    
    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            # Calcular gradientes
            gx = 0
            gy = 0
            
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    pixel = imagen.get_pixel(x + kx, y + ky)
                    gx += pixel * sobel_x[ky + 1][kx + 1]
                    gy += pixel * sobel_y[ky + 1][kx + 1]
            
            # Magnitud del gradiente
            magnitud = math.sqrt(gx**2 + gy**2)
            resultado.set_pixel(x, y, int(magnitud))
    
    return resultado


def detector_canny(imagen, umbral_bajo=50, umbral_alto=150):
    """
    Detector de bordes de Canny (versión simplificada)
    Args:
        imagen: objeto Imagen
        umbral_bajo: umbral inferior
        umbral_alto: umbral superior
    Returns:
        Imagen con bordes
    """
    # 1. Suavizado gaussiano
    suavizada = filtro_gaussiano(imagen, sigma=1.0)
    
    # 2. Calcular gradientes
    gradientes = Imagen(imagen.ancho, imagen.alto)
    direcciones = [[0 for _ in range(imagen.ancho)] for _ in range(imagen.alto)]
    
    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            gx = (suavizada.get_pixel(x+1, y) - suavizada.get_pixel(x-1, y)) / 2
            gy = (suavizada.get_pixel(x, y+1) - suavizada.get_pixel(x, y-1)) / 2
            
            magnitud = math.sqrt(gx**2 + gy**2)
            gradientes.set_pixel(x, y, int(magnitud))
            
            # Dirección del gradiente
            if gx != 0:
                direcciones[y][x] = math.atan2(gy, gx)
    
    # 3. Supresión no-máxima (simplificada)
    # 4. Umbral de histéresis
    resultado = Imagen(imagen.ancho, imagen.alto)
    
    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            mag = gradientes.get_pixel(x, y)
            
            if mag > umbral_alto:
                resultado.set_pixel(x, y, 255)
            elif mag > umbral_bajo:
                # Verificar si está conectado a borde fuerte
                es_borde = False
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if gradientes.get_pixel(x+dx, y+dy) > umbral_alto:
                            es_borde = True
                            break
                    if es_borde:
                        break
                
                if es_borde:
                    resultado.set_pixel(x, y, 255)
    
    return resultado


def segmentacion_umbral(imagen, umbral=128):
    """
    Segmentación por umbral simple
    Args:
        imagen: objeto Imagen
        umbral: valor de umbral
    Returns:
        Imagen binaria segmentada
    """
    resultado = Imagen(imagen.ancho, imagen.alto)
    
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            valor = imagen.get_pixel(x, y)
            resultado.set_pixel(x, y, 255 if valor > umbral else 0)
    
    return resultado


def algoritmo_otsu(imagen):
    """
    Calcula umbral óptimo usando método de Otsu
    Args:
        imagen: objeto Imagen
    Returns:
        umbral óptimo
    """
    # Calcular histograma
    histograma = [0] * 256
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            histograma[imagen.get_pixel(x, y)] += 1
    
    # Total de píxeles
    total = imagen.ancho * imagen.alto
    
    # Calcular suma total
    suma_total = sum(i * histograma[i] for i in range(256))
    
    mejor_umbral = 0
    mejor_varianza = 0
    
    suma_fondo = 0
    peso_fondo = 0
    
    for umbral in range(256):
        peso_fondo += histograma[umbral]
        
        if peso_fondo == 0:
            continue
        
        peso_objeto = total - peso_fondo
        
        if peso_objeto == 0:
            break
        
        suma_fondo += umbral * histograma[umbral]
        
        media_fondo = suma_fondo / peso_fondo
        media_objeto = (suma_total - suma_fondo) / peso_objeto
        
        # Varianza entre clases
        varianza = peso_fondo * peso_objeto * (media_fondo - media_objeto) ** 2
        
        if varianza > mejor_varianza:
            mejor_varianza = varianza
            mejor_umbral = umbral
    
    return mejor_umbral


# ============================================================================
# 48. TEXTURAS Y SOMBRAS
# ============================================================================

def calcular_glcm(imagen, distancia=1, angulo=0):
    """
    Calcula matriz de co-ocurrencia (GLCM) para análisis de textura
    Args:
        imagen: objeto Imagen
        distancia: distancia entre píxeles
        angulo: ángulo en grados (0, 45, 90, 135)
    Returns:
        matriz GLCM
    """
    # Simplificar niveles de gris (de 256 a 32 para eficiencia)
    niveles = 32
    glcm = [[0 for _ in range(niveles)] for _ in range(niveles)]
    
    # Calcular desplazamiento según ángulo
    if angulo == 0:
        dx, dy = distancia, 0
    elif angulo == 45:
        dx, dy = distancia, -distancia
    elif angulo == 90:
        dx, dy = 0, -distancia
    else:  # 135
        dx, dy = -distancia, -distancia
    
    # Construir GLCM
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            i = imagen.get_pixel(x, y) * niveles // 256
            
            nx, ny = x + dx, y + dy
            if 0 <= nx < imagen.ancho and 0 <= ny < imagen.alto:
                j = imagen.get_pixel(nx, ny) * niveles // 256
                glcm[i][j] += 1
    
    return glcm


def caracteristicas_textura(glcm):
    """
    Calcula características de textura desde GLCM
    Args:
        glcm: matriz de co-ocurrencia
    Returns:
        dict con características
    """
    n = len(glcm)
    
    # Normalizar GLCM
    total = sum(sum(fila) for fila in glcm)
    if total == 0:
        return {'contraste': 0, 'energia': 0, 'homogeneidad': 0}
    
    glcm_norm = [[glcm[i][j] / total for j in range(n)] for i in range(n)]
    
    # Contraste
    contraste = sum((i - j)**2 * glcm_norm[i][j] 
                   for i in range(n) for j in range(n))
    
    # Energía (uniformidad)
    energia = sum(glcm_norm[i][j]**2 
                 for i in range(n) for j in range(n))
    
    # Homogeneidad
    homogeneidad = sum(glcm_norm[i][j] / (1 + abs(i - j))
                      for i in range(n) for j in range(n))
    
    return {
        'contraste': contraste,
        'energia': energia,
        'homogeneidad': homogeneidad
    }


def detectar_sombras(imagen, umbral_intensidad=80):
    """
    Detecta regiones de sombra basándose en intensidad
    Args:
        imagen: objeto Imagen
        umbral_intensidad: umbral para considerar sombra
    Returns:
        máscara de sombras
    """
    sombras = Imagen(imagen.ancho, imagen.alto)
    
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            intensidad = imagen.get_pixel(x, y)
            
            if intensidad < umbral_intensidad:
                sombras.set_pixel(x, y, 255)  # Es sombra
            else:
                sombras.set_pixel(x, y, 0)
    
    return sombras


# ============================================================================
# 49. RECONOCIMIENTO DE OBJETOS
# ============================================================================

class DescriptorHOG:
    """
    Descriptor HOG (Histogram of Oriented Gradients)
    """
    def __init__(self, tam_celda=8, tam_bloque=2, num_bins=9):
        self.tam_celda = tam_celda
        self.tam_bloque = tam_bloque
        self.num_bins = num_bins
    
    def calcular_gradientes(self, imagen):
        """Calcula magnitud y orientación de gradientes"""
        magnitudes = []
        orientaciones = []
        
        for y in range(1, imagen.alto - 1):
            mag_fila = []
            ori_fila = []
            
            for x in range(1, imagen.ancho - 1):
                gx = imagen.get_pixel(x+1, y) - imagen.get_pixel(x-1, y)
                gy = imagen.get_pixel(x, y+1) - imagen.get_pixel(x, y-1)
                
                magnitud = math.sqrt(gx**2 + gy**2)
                orientacion = math.atan2(gy, gx) * 180 / math.pi
                
                # Normalizar orientación a [0, 180)
                if orientacion < 0:
                    orientacion += 180
                
                mag_fila.append(magnitud)
                ori_fila.append(orientacion)
            
            magnitudes.append(mag_fila)
            orientaciones.append(ori_fila)
        
        return magnitudes, orientaciones
    
    def extraer(self, imagen):
        """Extrae descriptor HOG de la imagen"""
        magnitudes, orientaciones = self.calcular_gradientes(imagen)
        
        # Calcular histogramas por celda
        num_celdas_x = (imagen.ancho - 2) // self.tam_celda
        num_celdas_y = (imagen.alto - 2) // self.tam_celda
        
        histogramas_celdas = []
        
        for cy in range(num_celdas_y):
            fila_hist = []
            for cx in range(num_celdas_x):
                histograma = [0] * self.num_bins
                
                # Calcular histograma para esta celda
                for y in range(cy * self.tam_celda, (cy + 1) * self.tam_celda):
                    for x in range(cx * self.tam_celda, (cx + 1) * self.tam_celda):
                        if y < len(magnitudes) and x < len(magnitudes[0]):
                            mag = magnitudes[y][x]
                            ori = orientaciones[y][x]
                            
                            # Asignar a bin
                            bin_idx = int(ori * self.num_bins / 180) % self.num_bins
                            histograma[bin_idx] += mag
                
                fila_hist.append(histograma)
            histogramas_celdas.append(fila_hist)
        
        return histogramas_celdas


def plantilla_matching(imagen, plantilla):
    """
    Busca plantilla en imagen usando correlación
    Args:
        imagen: Imagen donde buscar
        plantilla: Imagen de plantilla
    Returns:
        (x, y, score) de mejor coincidencia
    """
    mejor_score = float('-inf')
    mejor_pos = (0, 0)
    
    for y in range(imagen.alto - plantilla.alto + 1):
        for x in range(imagen.ancho - plantilla.ancho + 1):
            # Calcular correlación normalizada
            suma = 0
            suma_cuad_img = 0
            suma_cuad_temp = 0
            
            for ty in range(plantilla.alto):
                for tx in range(plantilla.ancho):
                    img_val = imagen.get_pixel(x + tx, y + ty)
                    temp_val = plantilla.get_pixel(tx, ty)
                    
                    suma += img_val * temp_val
                    suma_cuad_img += img_val ** 2
                    suma_cuad_temp += temp_val ** 2
            
            # Correlación normalizada
            if suma_cuad_img > 0 and suma_cuad_temp > 0:
                score = suma / math.sqrt(suma_cuad_img * suma_cuad_temp)
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_pos = (x, y)
    
    return mejor_pos[0], mejor_pos[1], mejor_score


# ============================================================================
# 50. RECONOCIMIENTO DE ESCRITURA
# ============================================================================

class ReconocedorDigitos:
    """
    Reconocedor simple de dígitos manuscritos
    """
    def __init__(self):
        self.plantillas = {}  # {digito: características}
    
    def extraer_caracteristicas(self, imagen):
        """
        Extrae características simples de una imagen de dígito
        Args:
            imagen: Imagen del dígito
        Returns:
            vector de características
        """
        caracteristicas = []
        
        # Dividir imagen en cuadrantes y contar píxeles activos
        mitad_x = imagen.ancho // 2
        mitad_y = imagen.alto // 2
        
        cuadrantes = [
            (0, 0, mitad_x, mitad_y),
            (mitad_x, 0, imagen.ancho, mitad_y),
            (0, mitad_y, mitad_x, imagen.alto),
            (mitad_x, mitad_y, imagen.ancho, imagen.alto)
        ]
        
        for x1, y1, x2, y2 in cuadrantes:
            cuenta = 0
            for y in range(y1, y2):
                for x in range(x1, x2):
                    if imagen.get_pixel(x, y) > 128:
                        cuenta += 1
            caracteristicas.append(cuenta)
        
        # Normalizar
        total = sum(caracteristicas)
        if total > 0:
            caracteristicas = [c / total for c in caracteristicas]
        
        return caracteristicas
    
    def entrenar(self, imagenes, etiquetas):
        """Entrena con ejemplos"""
        for imagen, digito in zip(imagenes, etiquetas):
            caract = self.extraer_caracteristicas(imagen)
            
            if digito not in self.plantillas:
                self.plantillas[digito] = []
            self.plantillas[digito].append(caract)
    
    def reconocer(self, imagen):
        """
        Reconoce dígito en imagen
        Args:
            imagen: Imagen del dígito
        Returns:
            dígito reconocido
        """
        caract = self.extraer_caracteristicas(imagen)
        
        mejor_digito = None
        mejor_distancia = float('inf')
        
        for digito, plantillas in self.plantillas.items():
            for plantilla in plantillas:
                # Distancia euclidiana
                distancia = math.sqrt(sum((c1 - c2)**2 
                                        for c1, c2 in zip(caract, plantilla)))
                
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_digito = digito
        
        return mejor_digito


# ============================================================================
# 51. ETIQUETADO DE LÍNEAS
# ============================================================================

def etiquetado_lineas_waltz(vertices, aristas):
    """
    Algoritmo de etiquetado de líneas de Waltz para interpretación de escenas
    Args:
        vertices: lista de vértices
        aristas: lista de aristas con etiquetas posibles
    Returns:
        etiquetado consistente de aristas
    """
    # Etiquetas posibles: '+' convexa, '-' cóncava, '→' occluding
    
    # Propagación de restricciones simplificada
    etiquetas = {}
    
    for arista in aristas:
        v1, v2, opciones = arista
        # Asignar etiqueta más probable
        etiquetas[(v1, v2)] = opciones[0] if opciones else '+'
    
    return etiquetas


def interpretar_vertices(vertices, tipo_vertices):
    """
    Interpreta tipo de vértice en dibujo lineal
    Args:
        vertices: lista de vértices
        tipo_vertices: dict {vertice: tipo} (L, Y, T, W, etc.)
    Returns:
        interpretación 3D
    """
    interpretaciones = {}
    
    for vertice, tipo in tipo_vertices.items():
        if tipo == 'L':
            interpretaciones[vertice] = 'esquina_convexa'
        elif tipo == 'Y':
            interpretaciones[vertice] = 'esquina_3_caras'
        elif tipo == 'T':
            interpretaciones[vertice] = 'union_T'
        elif tipo == 'W':
            interpretaciones[vertice] = 'esquina_concava'
    
    return interpretaciones


# ============================================================================
# 52. MOVIMIENTO
# ============================================================================

def flujo_optico_lucas_kanade(img1, img2, punto, ventana=5):
    """
    Calcula flujo óptico usando método de Lucas-Kanade
    Args:
        img1: Imagen en tiempo t
        img2: Imagen en tiempo t+1
        punto: (x, y) punto a rastrear
        ventana: tamaño de ventana
    Returns:
        (dx, dy) desplazamiento
    """
    x, y = punto
    offset = ventana // 2
    
    # Calcular derivadas
    Ix = []
    Iy = []
    It = []
    
    for dy in range(-offset, offset + 1):
        for dx in range(-offset, offset + 1):
            px, py = x + dx, y + dy
            
            # Derivada espacial en X
            ix = (img1.get_pixel(px+1, py) - img1.get_pixel(px-1, py)) / 2
            Ix.append(ix)
            
            # Derivada espacial en Y
            iy = (img1.get_pixel(px, py+1) - img1.get_pixel(px, py-1)) / 2
            Iy.append(iy)
            
            # Derivada temporal
            it = img2.get_pixel(px, py) - img1.get_pixel(px, py)
            It.append(it)
    
    # Resolver sistema Av = b
    # Donde A = [[ΣIx², ΣIxIy], [ΣIxIy, ΣIy²]]
    # y b = [-ΣIxIt, -ΣIyIt]
    
    sum_ix2 = sum(ix**2 for ix in Ix)
    sum_iy2 = sum(iy**2 for iy in Iy)
    sum_ixiy = sum(ix * iy for ix, iy in zip(Ix, Iy))
    sum_ixit = sum(ix * it for ix, it in zip(Ix, It))
    sum_iyit = sum(iy * it for iy, it in zip(Iy, It))
    
    # Determinante
    det = sum_ix2 * sum_iy2 - sum_ixiy ** 2
    
    if abs(det) < 1e-7:
        return (0, 0)
    
    # Resolver para velocidad
    vx = (sum_iy2 * (-sum_ixit) - sum_ixiy * (-sum_iyit)) / det
    vy = (sum_ix2 * (-sum_iyit) - sum_ixiy * (-sum_ixit)) / det
    
    return (vx, vy)


def seguimiento_movimiento(secuencia_imagenes, punto_inicial):
    """
    Rastrea punto a través de secuencia de imágenes
    Args:
        secuencia_imagenes: lista de Imagenes
        punto_inicial: (x, y) punto inicial
    Returns:
        trayectoria del punto
    """
    trayectoria = [punto_inicial]
    punto_actual = punto_inicial
    
    for i in range(len(secuencia_imagenes) - 1):
        dx, dy = flujo_optico_lucas_kanade(
            secuencia_imagenes[i],
            secuencia_imagenes[i + 1],
            punto_actual
        )
        
        punto_actual = (punto_actual[0] + dx, punto_actual[1] + dy)
        trayectoria.append(punto_actual)
    
    return trayectoria


def estimacion_fondo(secuencia_imagenes):
    """
    Estima imagen de fondo promediando secuencia
    Args:
        secuencia_imagenes: lista de Imagenes
    Returns:
        Imagen de fondo estimada
    """
    if not secuencia_imagenes:
        return None
    
    ancho = secuencia_imagenes[0].ancho
    alto = secuencia_imagenes[0].alto
    fondo = Imagen(ancho, alto)
    
    for y in range(alto):
        for x in range(ancho):
            # Promediar valores en todas las imágenes
            suma = sum(img.get_pixel(x, y) for img in secuencia_imagenes)
            promedio = suma // len(secuencia_imagenes)
            fondo.set_pixel(x, y, promedio)
    
    return fondo


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== PERCEPCIÓN ===\n")
    
    # Ejemplo 45: Proyección 3D
    print("45. Gráficos por Computador:")
    punto_3d = Punto3D(100, 50, 200)
    punto_2d = proyeccion_perspectiva(punto_3d)
    print(f"   Punto 3D: {punto_3d}")
    print(f"   Proyección 2D: ({punto_2d[0]:.2f}, {punto_2d[1]:.2f})")
    
    punto_rotado = rotacion_3d(punto_3d, angulo_y=math.pi/4)
    print(f"   Rotado 45° en Y: {punto_rotado}\n")
    
    # Ejemplo 46: Filtros
    print("46. Filtros de Imagen:")
    img_test = Imagen(10, 10)
    # Agregar algo de "ruido"
    for y in range(10):
        for x in range(10):
            img_test.set_pixel(x, y, random.randint(0, 255))
    
    img_suavizada = filtro_media(img_test, tam_kernel=3)
    print(f"   Imagen de prueba creada: {img_test.ancho}x{img_test.alto}")
    print(f"   Filtro de media aplicado")
    print(f"   Pixel original (5,5): {img_test.get_pixel(5, 5)}")
    print(f"   Pixel suavizado (5,5): {img_suavizada.get_pixel(5, 5)}\n")
    
    # Ejemplo 47: Detección de aristas
    print("47. Detección de Aristas:")
    # Crear imagen con borde artificial
    img_borde = Imagen(20, 20)
    for y in range(20):
        for x in range(20):
            if x < 10:
                img_borde.set_pixel(x, y, 0)
            else:
                img_borde.set_pixel(x, y, 255)
    
    bordes = detector_sobel(img_borde)
    print(f"   Imagen con borde vertical creada")
    print(f"   Detector de Sobel aplicado")
    print(f"   Magnitud en (9, 10): {bordes.get_pixel(9, 10)}\n")
    
    # Ejemplo 48: Textura
    print("48. Análisis de Textura:")
    glcm = calcular_glcm(img_test, distancia=1, angulo=0)
    caracteristicas = caracteristicas_textura(glcm)
    print(f"   Características de textura:")
    for nombre, valor in caracteristicas.items():
        print(f"      {nombre}: {valor:.3f}")
    print()
    
    # Ejemplo 49: HOG
    print("49. Reconocimiento de Objetos (HOG):")
    hog = DescriptorHOG(tam_celda=4, num_bins=9)
    descriptor = hog.extraer(img_test)
    print(f"   Descriptor HOG extraído")
    print(f"   Dimensiones del descriptor: {len(descriptor)}x{len(descriptor[0]) if descriptor else 0}")
    print()
    
    # Ejemplo 52: Flujo óptico
    print("52. Análisis de Movimiento:")
    img_t1 = Imagen(20, 20)
    img_t2 = Imagen(20, 20)
    
    # Simular movimiento de un objeto
    for y in range(20):
        for x in range(20):
            if 8 <= x <= 12 and 8 <= y <= 12:
                img_t1.set_pixel(x, y, 255)
            if 9 <= x <= 13 and 8 <= y <= 12:
                img_t2.set_pixel(x, y, 255)
    
    flujo = flujo_optico_lucas_kanade(img_t1, img_t2, (10, 10))
    print(f"   Flujo óptico en punto (10, 10):")
    print(f"   Desplazamiento: ({flujo[0]:.2f}, {flujo[1]:.2f})")
    print(f"   (Objeto se movió hacia la derecha)")