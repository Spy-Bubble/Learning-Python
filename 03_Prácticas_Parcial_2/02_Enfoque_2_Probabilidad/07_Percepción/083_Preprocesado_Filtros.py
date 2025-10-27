import random
import math

# ============================================================================
# CLASE AUXILIAR Imagen
# ============================================================================
class Imagen:
    """Representa una imagen simple en escala de grises"""
    def __init__(self, ancho, alto, data=None):
        self.ancho = ancho
        self.alto = alto
        if data:
             # Asumir data es lista de listas
             if len(data) != alto or len(data[0]) != ancho:
                  raise ValueError("Dimensiones de data no coinciden")
             self.pixeles = [[max(0, min(255, int(p))) for p in row] for row in data]
        else:
             self.pixeles = [[0 for _ in range(ancho)] for _ in range(alto)]

    def get_pixel(self, x, y):
        """Obtiene valor de pixel con manejo de bordes (replicar borde)"""
        x_clamp = max(0, min(x, self.ancho - 1))
        y_clamp = max(0, min(y, self.alto - 1))
        return self.pixeles[y_clamp][x_clamp]

    def set_pixel(self, x, y, valor):
        """Establece valor de pixel (con clipping 0-255)"""
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = max(0, min(255, int(valor)))

    def mostrar_ascii(self, escala=10):
        """Muestra una representación ASCII simple de la imagen"""
        chars = "@%#*+=-:. " # Caracteres de oscuro a claro
        print("-" * (self.ancho // escala + 2))
        for y in range(0, self.alto, escala):
            linea = "|"
            for x in range(0, self.ancho, escala):
                 # Promedio en bloque (simplificado)
                 pixel_val = self.get_pixel(x, y)
                 char_idx = min(len(chars)-1, int(pixel_val / (256 / len(chars))))
                 linea += chars[char_idx]
            linea += "|"
            print(linea)
        print("-" * (self.ancho // escala + 2))


# ============================================================================
# 46. PREPROCESADO: FILTROS
# ============================================================================

def filtro_media(imagen, tam_kernel=3):
    """
    Aplica filtro de media (promedio o 'box blur') para suavizado.
    Args:
        imagen: objeto Imagen
        tam_kernel: tamaño del kernel (debe ser impar: 3, 5, etc.)
    Returns:
        nueva objeto Imagen suavizada
    """
    if tam_kernel % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    resultado = Imagen(imagen.ancho, imagen.alto)
    offset = tam_kernel // 2

    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            suma_vecindad = 0
            num_pixeles = tam_kernel * tam_kernel

            # Iterar sobre la vecindad definida por el kernel
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    # Usar get_pixel maneja los bordes automáticamente
                    valor_pixel_vecino = imagen.get_pixel(x + kx, y + ky)
                    suma_vecindad += valor_pixel_vecino

            # Calcular promedio y asignar al pixel resultado
            promedio = suma_vecindad / num_pixeles
            resultado.set_pixel(x, y, promedio)

    return resultado


def filtro_mediana(imagen, tam_kernel=3):
    """
    Aplica filtro de mediana (útil para reducir ruido 'sal y pimienta').
    Args:
        imagen: objeto Imagen
        tam_kernel: tamaño del kernel (impar)
    Returns:
        nueva objeto Imagen filtrada
    """
    if tam_kernel % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")

    resultado = Imagen(imagen.ancho, imagen.alto)
    offset = tam_kernel // 2

    for y in range(imagen.alto):
        for x in range(imagen.ancho):
            valores_vecindad = []

            # Recolectar valores de la vecindad
            for ky in range(-offset, offset + 1):
                for kx in range(-offset, offset + 1):
                    valores_vecindad.append(imagen.get_pixel(x + kx, y + ky))

            # Calcular mediana
            valores_vecindad.sort()
            mediana = valores_vecindad[len(valores_vecindad) // 2]
            resultado.set_pixel(x, y, mediana)

    return resultado


def filtro_gaussiano(imagen, sigma=1.0, tam_kernel=None):
    """
    Aplica filtro gaussiano para suavizado (blur).
    Args:
        imagen: objeto Imagen
        sigma: desviación estándar de la gaussiana (controla el blur)
        tam_kernel: tamaño del kernel (opcional, se calcula si es None)
    Returns:
        nueva objeto Imagen suavizada
    """
    # Determinar tamaño del kernel si no se especifica
    if tam_kernel is None:
        tam_kernel = int(6 * sigma) + 1 # Asegurar tamaño suficiente
        if tam_kernel % 2 == 0:
            tam_kernel += 1 # Asegurar impar

    if tam_kernel % 2 == 0:
        raise ValueError("El tamaño del kernel debe ser impar.")
    offset = tam_kernel // 2

    # Crear kernel gaussiano 2D
    kernel = [[0.0 for _ in range(tam_kernel)] for _ in range(tam_kernel)]
    suma_kernel = 0.0
    sigma_sq = sigma**2

    for ky in range(-offset, offset + 1):
        for kx in range(-offset, offset + 1):
            valor_exp = -(kx**2 + ky**2) / (2 * sigma_sq)
            valor_gauss = math.exp(valor_exp)
            kernel[ky + offset][kx + offset] = valor_gauss
            suma_kernel += valor_gauss

    # Normalizar kernel para que la suma sea 1
    if suma_kernel > 0:
         kernel = [[v / suma_kernel for v in fila] for fila in kernel]

    # Aplicar convolución con el kernel gaussiano
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
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 46. Preprocesado: Filtros de Imagen ===\n")

    # Crear una imagen de prueba con ruido y un borde
    ancho_img, alto_img = 50, 50
    img_ruido = Imagen(ancho_img, alto_img)
    for y in range(alto_img):
        for x in range(ancho_img):
             # Fondo con ruido
             valor = random.randint(30, 70)
             # Borde brillante
             if 15 < x < 35 and 15 < y < 35: valor = 200
             # Ruido sal y pimienta
             if random.random() < 0.05: valor = 0
             if random.random() < 0.05: valor = 255
             img_ruido.set_pixel(x, y, valor)

    print("   Imagen original (con ruido y borde):")
    img_ruido.mostrar_ascii(escala=5)

    # Aplicar Filtro de Media
    img_media = filtro_media(img_ruido, tam_kernel=3)
    print("\n   Imagen con Filtro de Media (3x3):")
    img_media.mostrar_ascii(escala=5)

    # Aplicar Filtro de Mediana
    img_mediana = filtro_mediana(img_ruido, tam_kernel=3)
    print("\n   Imagen con Filtro de Mediana (3x3):")
    img_mediana.mostrar_ascii(escala=5)

    # Aplicar Filtro Gaussiano
    img_gauss = filtro_gaussiano(img_ruido, sigma=1.5)
    print("\n   Imagen con Filtro Gaussiano (sigma=1.5):")
    img_gauss.mostrar_ascii(escala=5)