import math
import random # Para imagen de ejemplo
from collections import Counter # Puede ser útil para histogramas

# ============================================================================
# DEPENDENCIA (Clase Imagen)
# ============================================================================
class Imagen:
    def __init__(self, ancho, alto, data=None):
        self.ancho = ancho
        self.alto = alto
        if data: self.pixeles = [[max(0, min(255, int(p))) for p in row] for row in data]
        else: self.pixeles = [[0 for _ in range(ancho)] for _ in range(alto)]
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

# ============================================================================
# 48. TEXTURAS Y SOMBRAS
# ============================================================================

def calcular_glcm(imagen, distancia=1, angulo=0, niveles=8):
    """
    Calcula la Matriz de Co-ocurrencia de Niveles de Gris (GLCM) para análisis de textura.
    Args:
        imagen: objeto Imagen (escala de grises)
        distancia: distancia entre los píxeles a comparar
        angulo: ángulo en grados (0, 45, 90, 135)
        niveles: número de niveles de gris a cuantizar (reduce tamaño de GLCM)
    Returns:
        matriz GLCM (lista de listas) de tamaño `niveles` x `niveles`
    """
    if niveles <= 0 or niveles > 256:
         raise ValueError("Niveles debe estar entre 1 y 256")

    glcm = [[0 for _ in range(niveles)] for _ in range(niveles)]

    # Calcular desplazamiento (dx, dy) según ángulo
    rad = math.radians(angulo)
    dx = int(round(distancia * math.cos(rad)))
    dy = int(round(-distancia * math.sin(rad))) # Eje Y suele ir hacia abajo

    # Iterar sobre la imagen para construir GLCM
    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            # Coordenadas del píxel vecino
            nx, ny = x + dx, y + dy

            # Verificar si el vecino está dentro de los límites
            if 0 <= nx < imagen.ancho and 0 <= ny < imagen.alto:
                # Obtener y cuantizar los niveles de gris
                i = int(imagen.get_pixel(x, y) * niveles / 256)
                j = int(imagen.get_pixel(nx, ny) * niveles / 256)
                # Asegurar índices válidos (por si pixel es 255)
                i = min(i, niveles - 1)
                j = min(j, niveles - 1)

                # Incrementar conteo en GLCM (simétrica)
                glcm[i][j] += 1
                glcm[j][i] += 1 # Hacerla simétrica

    return glcm


def caracteristicas_textura(glcm):
    """
    Calcula características de textura de Haralick (simplificado) desde GLCM.
    Args:
        glcm: matriz GLCM (lista de listas)
    Returns:
        dict con características: {'contraste', 'energia', 'homogeneidad'}
    """
    n = len(glcm)
    if n == 0: return {'contraste': 0, 'energia': 0, 'homogeneidad': 0}

    # Normalizar GLCM para obtener probabilidades P(i, j)
    total_pares = sum(sum(fila) for fila in glcm)
    if total_pares == 0:
        return {'contraste': 0, 'energia': 0, 'homogeneidad': 0}

    glcm_norm = [[glcm[i][j] / total_pares for j in range(n)] for i in range(n)]

    contraste = 0.0
    energia = 0.0     # También llamado Angular Second Moment (ASM)
    homogeneidad = 0.0 # También llamado Inverse Difference Moment (IDM)

    for i in range(n):
        for j in range(n):
            p_ij = glcm_norm[i][j]
            contraste += ((i - j)**2) * p_ij
            energia += p_ij**2
            homogeneidad += p_ij / (1.0 + abs(i - j))

    return {
        'contraste': contraste,
        'energia': energia,
        'homogeneidad': homogeneidad
    }


def detectar_sombras_simple(imagen, umbral_intensidad=80):
    """
    Detecta regiones de sombra basándose únicamente en un umbral de intensidad.
    Args:
        imagen: objeto Imagen
        umbral_intensidad: píxeles por debajo de este valor se consideran sombra
    Returns:
        objeto Imagen (máscara binaria de sombras, 255=sombra, 0=no sombra)
    """
    mascara_sombras = Imagen(imagen.ancho, imagen.alto)

    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            intensidad = imagen.get_pixel(x, y)
            if intensidad < umbral_intensidad:
                mascara_sombras.set_pixel(x, y, 255) # Es sombra
            # else: # No es necesario, la imagen se inicializa a 0

    return mascara_sombras

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 48. Texturas y Sombras ===\n")

    # Crear una imagen de ejemplo con textura y una zona oscura
    ancho_img, alto_img = 50, 50
    img_textura_sombra = Imagen(ancho_img, alto_img)
    for y in range(alto_img):
        for x in range(ancho_img):
            # Textura tipo tablero
            valor = 180 if (x // 10 + y // 10) % 2 == 0 else 120
            # Zona oscura (sombra)
            if x > 30 and y > 30:
                 valor = max(10, valor - 100) # Reducir intensidad
            # Añadir ruido
            valor += random.randint(-10, 10)
            img_textura_sombra.set_pixel(x, y, valor)

    print("   Imagen de ejemplo (con textura y sombra):")
    img_textura_sombra.mostrar_ascii(escala=5)

    # 1. Análisis de Textura (GLCM)
    print("\n   Análisis de Textura (GLCM):")
    # Calcular GLCM para la imagen completa (mezcla de texturas)
    glcm_completa = calcular_glcm(img_textura_sombra, distancia=1, angulo=0, niveles=8)
    caract_completa = caracteristicas_textura(glcm_completa)
    print("      Características (imagen completa):")
    for nombre, valor in caract_completa.items():
        print(f"         {nombre}: {valor:.3f}")

    # (En una aplicación real, se calcularía sobre ventanas para localizar texturas)

    # 2. Detección de Sombras
    print("\n   Detección de Sombras (umbral simple):")
    umbral = 70
    mascara = detectar_sombras_simple(img_textura_sombra, umbral_intensidad=umbral)
    print(f"      Máscara de sombras (pixeles < {umbral}):")
    mascara.mostrar_ascii(escala=5)