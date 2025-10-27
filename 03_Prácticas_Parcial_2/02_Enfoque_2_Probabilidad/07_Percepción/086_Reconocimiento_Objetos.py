import math
import random # Para imagen de ejemplo

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
    def mostrar_ascii(self, escala=10): # Simplificado para demo
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
# 49. RECONOCIMIENTO DE OBJETOS
# ============================================================================

class DescriptorHOG:
    """
    Descriptor HOG (Histogram of Oriented Gradients) - Simplificado.
    Extrae características basadas en la distribución de orientaciones
    de gradientes en celdas locales.
    """
    def __init__(self, tam_celda=8, tam_bloque_celdas=2, num_bins=9):
        self.tam_celda = tam_celda # Tamaño de celda en píxeles (ej. 8x8)
        self.celdas_por_bloque = tam_bloque_celdas # Tamaño de bloque en celdas (ej. 2x2)
        self.num_bins = num_bins # Número de bins para el histograma de orientación
        self.angulo_max = 180 # Usar gradientes no signados (0-180 grados)

    def _calcular_gradientes(self, imagen):
        """Calcula magnitud y orientación (0-180) de gradientes"""
        magnitudes = [[0.0 for _ in range(imagen.ancho)] for _ in range(imagen.alto)]
        orientaciones = [[0.0 for _ in range(imagen.ancho)] for _ in range(imagen.alto)]

        for y in range(1, imagen.alto - 1):
            for x in range(1, imagen.ancho - 1):
                # Gradientes simples (diferencias centrales)
                gx = imagen.get_pixel(x + 1, y) - imagen.get_pixel(x - 1, y)
                gy = imagen.get_pixel(x, y + 1) - imagen.get_pixel(x, y - 1)

                mag = math.sqrt(gx**2 + gy**2)
                ori_rad = math.atan2(gy, gx)
                ori_deg = math.degrees(ori_rad)

                # Convertir a 0-180 grados
                if ori_deg < 0:
                    ori_deg += 180

                magnitudes[y][x] = mag
                orientaciones[y][x] = ori_deg % self.angulo_max # Asegurar rango

        return magnitudes, orientaciones

    def extraer(self, imagen):
        """Extrae el vector descriptor HOG de la imagen"""
        magnitudes, orientaciones = self._calcular_gradientes(imagen)

        # Dimensiones en celdas
        celdas_y = imagen.alto // self.tam_celda
        celdas_x = imagen.ancho // self.tam_celda

        # 1. Calcular histogramas por celda
        hist_celdas = [[[0.0] * self.num_bins for _ in range(celdas_x)] for _ in range(celdas_y)]

        bin_size = self.angulo_max / self.num_bins

        for cy in range(celdas_y):
            for cx in range(celdas_x):
                # Píxeles dentro de la celda actual
                y_start, y_end = cy * self.tam_celda, (cy + 1) * self.tam_celda
                x_start, x_end = cx * self.tam_celda, (cx + 1) * self.tam_celda

                for y in range(y_start, y_end):
                    for x in range(x_start, x_end):
                        mag = magnitudes[y][x]
                        ori = orientaciones[y][x]

                        # Votación ponderada por magnitud en los bins
                        bin_idx_f = ori / bin_size
                        bin_idx_0 = int(bin_idx_f - 0.5)
                        bin_idx_1 = (bin_idx_0 + 1) % self.num_bins
                        
                        # Interpolar voto entre bins cercanos
                        peso_1 = (bin_idx_f - (bin_idx_0 + 0.5))
                        peso_0 = 1.0 - peso_1
                        
                        hist_celdas[cy][cx][bin_idx_0 % self.num_bins] += mag * peso_0
                        hist_celdas[cy][cx][bin_idx_1] += mag * peso_1

        # 2. Normalizar histogramas por bloques
        descriptor_hog = []
        bloques_y = celdas_y - self.celdas_por_bloque + 1
        bloques_x = celdas_x - self.celdas_por_bloque + 1
        epsilon = 1e-5 # Para evitar división por cero

        for by in range(bloques_y):
            for bx in range(bloques_x):
                bloque_vector = []
                # Concatenar histogramas de celdas en el bloque
                for cy_in_block in range(self.celdas_por_bloque):
                    for cx_in_block in range(self.celdas_por_bloque):
                        bloque_vector.extend(hist_celdas[by + cy_in_block][bx + cx_in_block])

                # Normalizar L2 el vector del bloque
                norma_bloque = math.sqrt(sum(v**2 for v in bloque_vector) + epsilon**2)
                bloque_normalizado = [v / norma_bloque for v in bloque_vector]
                
                # Opcional: Clipping (ej. a 0.2)
                # bloque_normalizado = [min(v, 0.2) for v in bloque_normalizado]
                # Renormalizar después de clipping
                # norma_bloque = math.sqrt(sum(v**2 for v in bloque_normalizado) + epsilon**2)
                # bloque_normalizado = [v / norma_bloque for v in bloque_normalizado]

                descriptor_hog.extend(bloque_normalizado)

        return descriptor_hog # Devuelve un vector plano


def plantilla_matching_ncc(imagen, plantilla):
    """
    Busca una plantilla en una imagen usando Correlación Cruzada Normalizada (NCC).
    Args:
        imagen: objeto Imagen donde buscar
        plantilla: objeto Imagen de la plantilla
    Returns:
        (x, y, score) de la mejor coincidencia encontrada.
    """
    mejor_score = -float('inf') # NCC va de -1 a 1
    mejor_pos = (0, 0)

    # Dimensiones
    h_img, w_img = imagen.alto, imagen.ancho
    h_temp, w_temp = plantilla.alto, plantilla.ancho

    # Calcular media y std dev de la plantilla (una sola vez)
    pixels_temp = [plantilla.get_pixel(tx, ty) for ty in range(h_temp) for tx in range(w_temp)]
    mean_temp = sum(pixels_temp) / len(pixels_temp) if pixels_temp else 0
    std_dev_temp = math.sqrt(sum((p - mean_temp)**2 for p in pixels_temp)) if pixels_temp else 0

    if std_dev_temp < 1e-6: # Plantilla plana, no se puede normalizar
        print("Advertencia: Plantilla tiene desviación estándar casi cero.")
        return 0, 0, 0.0

    # Deslizar la plantilla sobre la imagen
    for y in range(h_img - h_temp + 1):
        for x in range(w_img - w_temp + 1):
            # Extraer región de la imagen del tamaño de la plantilla
            pixels_region = [imagen.get_pixel(x + tx, y + ty) for ty in range(h_temp) for tx in range(w_temp)]
            
            # Calcular media y std dev de la región
            mean_region = sum(pixels_region) / len(pixels_region)
            std_dev_region = math.sqrt(sum((p - mean_region)**2 for p in pixels_region))

            if std_dev_region < 1e-6: # Región plana
                 score = 0.0
            else:
                 # Calcular Correlación Cruzada Normalizada
                 numerador = sum((pixels_region[i] - mean_region) * (pixels_temp[i] - mean_temp)
                                 for i in range(len(pixels_region)))
                 denominador = std_dev_region * std_dev_temp
                 score = numerador / denominador / len(pixels_region) # Normalizar por N

            # Actualizar mejor coincidencia
            if score > mejor_score:
                mejor_score = score
                mejor_pos = (x, y)

    return mejor_pos[0], mejor_pos[1], mejor_score

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 49. Reconocimiento de Objetos (HOG y Template Matching) ===\n")

    # Crear imagen simple con un borde vertical
    img_borde_hog = Imagen(32, 32)
    for y in range(32):
        for x in range(32):
             img_borde_hog.set_pixel(x, y, 255 if x > 15 else 50)

    print("   Imagen de prueba (borde vertical):")
    img_borde_hog.mostrar_ascii(escala=4)

    # 1. Extracción de Descriptor HOG
    print("\n   Descriptor HOG:")
    hog = DescriptorHOG(tam_celda=8, tam_bloque_celdas=2, num_bins=9)
    descriptor = hog.extraer(img_borde_hog)
    print(f"      Descriptor HOG extraído.")
    print(f"      Longitud del vector HOG: {len(descriptor)}")
    # (Esperado: Bloques_X * Bloques_Y * Celdas_Bloque_X * Celdas_Bloque_Y * Bins)
    # (32/8 - 2 + 1) * (32/8 - 2 + 1) * 2 * 2 * 9 = 3 * 3 * 4 * 9 = 324

    # 2. Template Matching
    print("\n   Template Matching (NCC):")
    # Usar la misma imagen como 'imagen grande' y una parte como plantilla
    plantilla = Imagen(10, 10)
    for y in range(10):
         for x in range(10):
              # Copiar esquina superior izquierda de la imagen con borde
              plantilla.set_pixel(x, y, img_borde_hog.get_pixel(x, y))

    print("      Plantilla (esquina superior izquierda):")
    plantilla.mostrar_ascii(escala=2)

    mejor_x, mejor_y, score = plantilla_matching_ncc(img_borde_hog, plantilla)
    print(f"\n      Mejor coincidencia encontrada en: ({mejor_x}, {mejor_y})")
    print(f"      Score (NCC): {score:.4f}")
    # (Esperado: (0, 0) con score cercano a 1.0)