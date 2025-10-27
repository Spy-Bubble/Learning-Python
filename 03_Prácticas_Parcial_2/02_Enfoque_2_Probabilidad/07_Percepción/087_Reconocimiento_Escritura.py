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
    # mostrar_ascii omitido por brevedad

# ============================================================================
# 50. RECONOCIMIENTO DE ESCRITURA (Simplificado)
# ============================================================================

class ReconocedorDigitosSimple:
    """
    Reconocedor simple de dígitos manuscritos usando comparación de
    características básicas (basado en plantillas/prototipos).
    """
    def __init__(self):
        # {digito_str: [lista_de_vectores_caracteristicas]}
        self.plantillas_caracteristicas = {}
        # Podríamos usar un promedio en lugar de guardar todas
        # self.prototipos = {} # {digito_str: vector_promedio}

    def _extraer_caracteristicas_cuadrantes(self, imagen, umbral_bin=128):
        """
        Extrae características simples: densidad de píxeles activos en cuadrantes.
        Args:
            imagen: Imagen del dígito (asumir normalizada en tamaño y binarizada)
            umbral_bin: umbral para considerar un pixel activo (blanco)
        Returns:
            vector de características (lista de floats normalizada)
        """
        caracteristicas = []
        ancho, alto = imagen.ancho, imagen.alto
        mitad_x, mitad_y = ancho // 2, alto // 2

        # Definir los 4 cuadrantes (x_start, y_start, x_end, y_end)
        cuadrantes_coords = [
            (0, 0, mitad_x, mitad_y),             # Superior Izquierdo
            (mitad_x, 0, ancho, mitad_y),         # Superior Derecho
            (0, mitad_y, mitad_x, alto),          # Inferior Izquierdo
            (mitad_x, mitad_y, ancho, alto)       # Inferior Derecho
        ]

        # Contar píxeles activos (> umbral) en cada cuadrante
        for x1, y1, x2, y2 in cuadrantes_coords:
            cuenta_activos = 0
            total_pixeles_cuadrante = (x2 - x1) * (y2 - y1)
            if total_pixeles_cuadrante == 0:
                 caracteristicas.append(0.0)
                 continue

            for y in range(y1, y2):
                for x in range(x1, x2):
                    if imagen.get_pixel(x, y) > umbral_bin:
                        cuenta_activos += 1
            # Normalizar por el número de píxeles en el cuadrante
            caracteristicas.append(cuenta_activos / total_pixeles_cuadrante)

        # Opcional: añadir más características (ej. centroide, momentos, etc.)

        # Normalizar L2 el vector completo (opcional)
        norma = math.sqrt(sum(c**2 for c in caracteristicas))
        if norma > 0:
             caracteristicas_norm = [c / norma for c in caracteristicas]
        else:
             caracteristicas_norm = caracteristicas

        return caracteristicas_norm

    def entrenar(self, imagenes, etiquetas):
        """
        'Entrena' almacenando las características de las imágenes de ejemplo.
        Args:
            imagenes: lista de objetos Imagen
            etiquetas: lista de etiquetas correspondientes (ej. '0', '1', ...)
        """
        print("   (Entrenando Reconocedor: Extrayendo características de plantillas...)")
        self.plantillas_caracteristicas = {} # Reiniciar
        for imagen, etiqueta_str in zip(imagenes, etiquetas):
            caract = self._extraer_caracteristicas_cuadrantes(imagen)

            if etiqueta_str not in self.plantillas_caracteristicas:
                self.plantillas_caracteristicas[etiqueta_str] = []
            self.plantillas_caracteristicas[etiqueta_str].append(caract)

        # Opcional: Calcular prototipo promedio por dígito
        # self.prototipos = {}
        # for digito, lista_caract in self.plantillas_caracteristicas.items():
        #      if lista_caract:
        #           num_caract = len(lista_caract[0])
        #           promedio = [sum(c[i] for c in lista_caract) / len(lista_caract)
        #                       for i in range(num_caract)]
        #           self.prototipos[digito] = promedio

    def reconocer(self, imagen):
        """
        Reconoce el dígito en la imagen comparando características con las plantillas.
        Usa el vecino más cercano (Nearest Neighbor).
        Args:
            imagen: objeto Imagen del dígito a reconocer
        Returns:
            etiqueta del dígito reconocido (string), o None si no hay plantillas
        """
        if not self.plantillas_caracteristicas:
             return None # No entrenado

        caract_entrada = self._extraer_caracteristicas_cuadrantes(imagen)

        mejor_digito = None
        min_distancia = float('inf')

        # Comparar con todas las plantillas almacenadas
        for digito, lista_plantillas in self.plantillas_caracteristicas.items():
            for plantilla_caract in lista_plantillas:
                # Calcular distancia euclidiana entre características
                distancia = math.sqrt(sum((c1 - c2)**2
                                       for c1, c2 in zip(caract_entrada, plantilla_caract)))

                if distancia < min_distancia:
                    min_distancia = distancia
                    mejor_digito = digito

        # Alternativa: Comparar con prototipos promedio
        # for digito, prototipo_caract in self.prototipos.items():
        #     distancia = ...
        #     if distancia < min_distancia: ...

        return mejor_digito

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

# --- Funciones para crear imágenes de dígitos simples ---
def crear_imagen_digito(digito_str, ancho=20, alto=20):
     img = Imagen(ancho, alto)
     # Lógica muy simple para dibujar dígitos (solo para demo)
     if digito_str == '1':
          for y in range(alto): img.set_pixel(ancho // 2, y, 255)
     elif digito_str == '0':
          for x in range(ancho//4, 3*ancho//4):
               img.set_pixel(x, alto//4, 255)
               img.set_pixel(x, 3*alto//4, 255)
          for y in range(alto//4, 3*alto//4):
               img.set_pixel(ancho//4, y, 255)
               img.set_pixel(3*ancho//4, y, 255)
     elif digito_str == '7':
          for x in range(ancho): img.set_pixel(x, alto//4, 255)
          for y in range(alto): img.set_pixel(3*ancho//4, y, 255)
     # Añadir ruido
     for _ in range(ancho*alto // 20):
          rx, ry = random.randint(0, ancho-1), random.randint(0, alto-1)
          img.set_pixel(rx, ry, random.randint(0, 255))
     return img

if __name__ == "__main__":
    print("=== 50. Reconocimiento de Escritura (Dígitos Simple) ===\n")

    reconocedor = ReconocedorDigitosSimple()

    # Crear datos de "entrenamiento" (plantillas)
    imagenes_train = [
        crear_imagen_digito('0'),
        crear_imagen_digito('1'),
        crear_imagen_digito('0'), # Más ejemplos
        crear_imagen_digito('1'),
        crear_imagen_digito('7')
    ]
    etiquetas_train = ['0', '1', '0', '1', '7']

    reconocedor.entrenar(imagenes_train, etiquetas_train)
    print("   Reconocedor entrenado con plantillas para '0', '1', '7'.\n")

    # Crear imágenes de prueba
    img_test_1 = crear_imagen_digito('1')
    img_test_0 = crear_imagen_digito('0')
    img_test_7 = crear_imagen_digito('7')

    print("   Reconociendo imágenes de prueba:")
    pred_1 = reconocedor.reconocer(img_test_1)
    pred_0 = reconocedor.reconocer(img_test_0)
    pred_7 = reconocedor.reconocer(img_test_7)

    print(f"      Imagen '1' -> Predicción: {pred_1}")
    print(f"      Imagen '0' -> Predicción: {pred_0}")
    print(f"      Imagen '7' -> Predicción: {pred_7}")