import math
import random # Para imagen de ejemplo

# ============================================================================
# DEPENDENCIAS (Clase Imagen y Filtro Gaussiano)
# ============================================================================
class Imagen:
    def __init__(self, ancho, alto, data=None):
        self.ancho = ancho
        self.alto = alto
        if data:
             self.pixeles = [[max(0, min(255, int(p))) for p in row] for row in data]
        else:
             self.pixeles = [[0 for _ in range(ancho)] for _ in range(alto)]
    def get_pixel(self, x, y):
        x_clamp = max(0, min(x, self.ancho - 1))
        y_clamp = max(0, min(y, self.alto - 1))
        return self.pixeles[y_clamp][x_clamp]
    def set_pixel(self, x, y, valor):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = max(0, min(255, int(valor)))
    def mostrar_ascii(self, escala=10):
        chars = "@%#*+=-:. "
        print("-" * (self.ancho // escala + 2))
        for y in range(0, self.alto, escala):
            linea = "|"
            for x in range(0, self.ancho, escala):
                 pixel_val = self.get_pixel(x, y)
                 char_idx = min(len(chars)-1, int(pixel_val / (256 / len(chars))))
                 linea += chars[char_idx]
            linea += "|"
            print(linea)
        print("-" * (self.ancho // escala + 2))

def filtro_gaussiano(imagen, sigma=1.0, tam_kernel=None):
    # (Implementación copiada de 083_Preprocesado_Filtros.py)
    if tam_kernel is None:
        tam_kernel = int(6 * sigma) + 1
        if tam_kernel % 2 == 0: tam_kernel += 1
    if tam_kernel % 2 == 0: raise ValueError("Kernel impar")
    offset = tam_kernel // 2
    kernel = [[0.0 for _ in range(tam_kernel)] for _ in range(tam_kernel)]
    suma_kernel = 0.0
    sigma_sq = sigma**2
    for ky in range(-offset, offset + 1):
        for kx in range(-offset, offset + 1):
            valor_exp = -(kx**2 + ky**2) / (2 * sigma_sq)
            valor_gauss = math.exp(valor_exp)
            kernel[ky + offset][kx + offset] = valor_gauss
            suma_kernel += valor_gauss
    if suma_kernel > 0: kernel = [[v / suma_kernel for v in fila] for fila in kernel]
    resultado = Imagen(imagen.ancho, imagen.alto)
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            suma_ponderada = 0.0
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    pixel_val = imagen.get_pixel(x + kx, y + ky)
                    kernel_val = kernel[ky + offset][kx + offset]
                    suma_ponderada += pixel_val * kernel_val
            resultado.set_pixel(x, y, suma_ponderada)
    return resultado

# ============================================================================
# 47. DETECCIÓN DE ARISTAS Y SEGMENTACIÓN
# ============================================================================

def detector_sobel(imagen):
    """
    Detector de bordes de Sobel. Calcula la magnitud del gradiente.
    Args:
        imagen: objeto Imagen (escala de grises)
    Returns:
        objeto Imagen con la magnitud de los bordes
    """
    # Kernels de Sobel para Gx y Gy
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [ 0,  0,  0], [ 1,  2,  1]]

    resultado = Imagen(imagen.ancho, imagen.alto)

    # Iterar sobre la imagen (evitando bordes donde el kernel no cabe)
    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            gx = 0.0 # Gradiente en X
            gy = 0.0 # Gradiente en Y

            # Aplicar convolución con kernels Sobel
            for ky in range(-1, 2):
                for kx in range(-1, 2):
                    pixel = imagen.get_pixel(x + kx, y + ky)
                    gx += pixel * sobel_x[ky + 1][kx + 1]
                    gy += pixel * sobel_y[ky + 1][kx + 1]

            # Calcular la magnitud del gradiente
            magnitud = math.sqrt(gx**2 + gy**2)
            resultado.set_pixel(x, y, magnitud)

    return resultado


def detector_canny(imagen, sigma=1.0, umbral_bajo=50, umbral_alto=150):
    """
    Detector de bordes de Canny (versión simplificada).
    Args:
        imagen: objeto Imagen
        sigma: sigma para el suavizado gaussiano inicial
        umbral_bajo, umbral_alto: umbrales para histéresis
    Returns:
        Imagen binaria con bordes detectados
    """
    # 1. Suavizado gaussiano para reducir ruido
    suavizada = filtro_gaussiano(imagen, sigma=sigma)

    # 2. Calcular gradientes (Magnitud y Dirección) - Similar a Sobel
    magnitudes = Imagen(imagen.ancho, imagen.alto)
    # Ángulos en grados [-180, 180]
    angulos = [[0.0 for _ in range(imagen.ancho)] for _ in range(imagen.alto)]

    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            # Usar diferencias centrales para gradientes
            gx = suavizada.get_pixel(x+1, y) - suavizada.get_pixel(x-1, y)
            gy = suavizada.get_pixel(x, y+1) - suavizada.get_pixel(x, y-1)

            mag = math.sqrt(gx**2 + gy**2)
            magnitudes.set_pixel(x, y, mag)

            # Calcular ángulo y asegurar que no sea NaN
            angulo_rad = math.atan2(gy, gx)
            angulos[y][x] = math.degrees(angulo_rad)

    # 3. Supresión No-Máxima (Adelgazamiento de bordes) - SIMPLIFICADO
    # Compara la magnitud con los vecinos en la dirección del gradiente
    supresion = Imagen(imagen.ancho, imagen.alto)
    for y in range(1, imagen.alto - 1):
        for x in range(1, imagen.ancho - 1):
            mag = magnitudes.get_pixel(x,y)
            ang = angulos[y][x]
            q = 255
            r = 255

            # Determinar vecinos a comparar según ángulo
            if (0 <= ang < 22.5) or (157.5 <= abs(ang) <= 180): # Horizontal
                q = magnitudes.get_pixel(x+1, y)
                r = magnitudes.get_pixel(x-1, y)
            elif (22.5 <= ang < 67.5) or (-157.5 <= ang < -112.5): # Diagonal /
                q = magnitudes.get_pixel(x+1, y+1)
                r = magnitudes.get_pixel(x-1, y-1)
            elif (67.5 <= ang < 112.5) or (-112.5 <= ang < -67.5): # Vertical
                q = magnitudes.get_pixel(x, y+1)
                r = magnitudes.get_pixel(x, y-1)
            elif (112.5 <= ang < 157.5) or (-67.5 <= ang < -22.5): # Diagonal \
                q = magnitudes.get_pixel(x-1, y+1)
                r = magnitudes.get_pixel(x+1, y-1)

            # Suprimir si no es máximo local
            if (mag >= q) and (mag >= r):
                supresion.set_pixel(x, y, mag)
            else:
                supresion.set_pixel(x, y, 0)

    # 4. Umbral de Histéresis
    resultado_canny = Imagen(imagen.ancho, imagen.alto)
    bordes_fuertes = set()
    bordes_debiles = set()

    # Clasificar píxeles
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            mag = supresion.get_pixel(x,y)
            if mag >= umbral_alto:
                resultado_canny.set_pixel(x,y, 255)
                bordes_fuertes.add((x,y))
            elif mag >= umbral_bajo:
                bordes_debiles.add((x,y))

    # Conectar bordes débiles a fuertes (simplificado)
    cambio = True
    while cambio:
         cambio = False
         for x, y in list(bordes_debiles): # Iterar sobre copia
              conectado = False
              for dy in [-1, 0, 1]:
                   for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0: continue
                        if (x+dx, y+dy) in bordes_fuertes:
                             conectado = True
                             break
                   if conectado: break
              if conectado:
                   resultado_canny.set_pixel(x, y, 255)
                   bordes_fuertes.add((x,y))
                   bordes_debiles.remove((x,y))
                   cambio = True

    return resultado_canny


def segmentacion_umbral(imagen, umbral=128):
    """
    Segmentación por umbral simple. Píxeles > umbral = blanco, sino negro.
    Args:
        imagen: objeto Imagen
        umbral: valor de umbral (0-255)
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
    Calcula un umbral óptimo para binarización usando el método de Otsu.
    Maximiza la varianza entre las clases (fondo y objeto).
    Args:
        imagen: objeto Imagen (escala de grises)
    Returns:
        umbral óptimo (int)
    """
    # 1. Calcular histograma de intensidades
    histograma = [0] * 256
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            intensidad = imagen.get_pixel(x, y)
            histograma[intensidad] += 1

    total_pixeles = imagen.ancho * imagen.alto
    if total_pixeles == 0: return 128 # Valor por defecto

    # 2. Calcular probabilidades y sumas acumuladas
    suma_total_intensidad = sum(i * histograma[i] for i in range(256))
    prob_acum = [0.0] * 256
    suma_intensidad_acum = [0.0] * 256
    prob_acum[0] = histograma[0] / total_pixeles
    suma_intensidad_acum[0] = 0.0 # 0 * hist[0]
    for i in range(1, 256):
         prob_acum[i] = prob_acum[i-1] + histograma[i] / total_pixeles
         suma_intensidad_acum[i] = suma_intensidad_acum[i-1] + i * (histograma[i] / total_pixeles)

    # 3. Iterar sobre posibles umbrales para encontrar el óptimo
    mejor_umbral = 0
    max_varianza_entre_clases = 0.0

    for umbral in range(256):
        peso_fondo = prob_acum[umbral]      # P(fondo)
        peso_objeto = 1.0 - peso_fondo      # P(objeto)

        # Si una clase tiene peso 0, la varianza es 0
        if peso_fondo == 0 or peso_objeto == 0:
            continue

        # Media de intensidad del fondo
        media_fondo = suma_intensidad_acum[umbral] / peso_fondo
        # Media de intensidad del objeto
        media_objeto = (suma_intensidad_acum[255] - suma_intensidad_acum[umbral]) / peso_objeto

        # Varianza entre clases: peso_fondo * peso_objeto * (media_fondo - media_objeto)^2
        varianza_entre = peso_fondo * peso_objeto * (media_fondo - media_objeto)**2

        # Actualizar si se encontró mejor varianza
        if varianza_entre > max_varianza_entre_clases:
            max_varianza_entre_clases = varianza_entre
            mejor_umbral = umbral

    return mejor_umbral

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 47. Detección de Aristas y Segmentación ===\n")

    # Crear imagen con borde artificial
    ancho_img, alto_img = 50, 50
    img_borde = Imagen(ancho_img, alto_img)
    for y in range(alto_img):
        for x in range(ancho_img):
             # Fondo oscuro, cuadrado claro en el centro
             valor = 50
             if 15 < x < 35 and 15 < y < 35: valor = 200
             # Añadir ruido suave
             valor += random.randint(-10, 10)
             img_borde.set_pixel(x, y, valor)

    print("   Imagen original (cuadrado claro sobre fondo oscuro):")
    img_borde.mostrar_ascii(escala=5)

    # 1. Detector de Sobel
    bordes_sobel = detector_sobel(img_borde)
    print("\n   Bordes detectados con Sobel (Magnitud):")
    bordes_sobel.mostrar_ascii(escala=5)

    # 2. Detector de Canny
    bordes_canny = detector_canny(img_borde, sigma=1.0, umbral_bajo=30, umbral_alto=80)
    print("\n   Bordes detectados con Canny:")
    bordes_canny.mostrar_ascii(escala=5)

    # 3. Segmentación por Umbral Fijo
    img_seg_fija = segmentacion_umbral(img_borde, umbral=120)
    print("\n   Segmentación con Umbral Fijo (120):")
    img_seg_fija.mostrar_ascii(escala=5)

    # 4. Segmentación con Umbral de Otsu
    umbral_otsu = algoritmo_otsu(img_borde)
    img_seg_otsu = segmentacion_umbral(img_borde, umbral=umbral_otsu)
    print(f"\n   Umbral calculado por Otsu: {umbral_otsu}")
    print("   Segmentación con Umbral de Otsu:")
    img_seg_otsu.mostrar_ascii(escala=5)