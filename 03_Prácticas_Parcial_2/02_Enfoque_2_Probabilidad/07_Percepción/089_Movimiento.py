import math
import random # Para imágenes de ejemplo
import numpy as np # Necesario para Lucas-Kanade (inversa de matriz)

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
        # Usar interpolación bilineal podría ser mejor que clamp para flujo óptico
        x_f, y_f = float(x), float(y)
        x1, y1 = int(x_f), int(y_f)
        x2, y2 = x1 + 1, y1 + 1
        
        # Pesos bilineales
        fx1 = x_f - x1
        fy1 = y_f - y1
        fx0 = 1.0 - fx1
        fy0 = 1.0 - fy1

        # Obtener valores de los 4 vecinos (con clamp)
        p11 = self._get_pixel_clamp(x1, y1)
        p12 = self._get_pixel_clamp(x1, y2)
        p21 = self._get_pixel_clamp(x2, y1)
        p22 = self._get_pixel_clamp(x2, y2)

        # Interpolar
        val = (p11 * fx0 * fy0 +
               p12 * fx0 * fy1 +
               p21 * fx1 * fy0 +
               p22 * fx1 * fy1)
        return val

    def _get_pixel_clamp(self, x, y): # Helper para get_pixel
        x_c = max(0, min(int(x), self.ancho - 1))
        y_c = max(0, min(int(y), self.alto - 1))
        return self.pixeles[y_c][x_c]

    def set_pixel(self, x, y, valor):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.pixeles[y][x] = max(0, min(255, int(valor)))
    # mostrar_ascii omitido

# ============================================================================
# 52. MOVIMIENTO
# ============================================================================

def flujo_optico_lucas_kanade(img1, img2, punto, ventana=5):
    """
    Calcula el flujo óptico (vector de movimiento [vx, vy]) para un punto
    usando el método diferencial de Lucas-Kanade.
    Asume brillo constante y movimiento pequeño.
    Args:
        img1: objeto Imagen en tiempo t
        img2: objeto Imagen en tiempo t+1
        punto: tupla (x, y) del punto a rastrear en img1
        ventana: tamaño de la ventana alrededor del punto (impar)
    Returns:
        (vx, vy) tupla con el vector de flujo óptico estimado
    """
    x_c, y_c = punto
    offset = ventana // 2
    if ventana % 2 == 0: offset -= 1 # Asegurar simetría si ventana par

    # Matrices para el sistema lineal A*v = b
    A = np.zeros((2, 2))
    b = np.zeros(2)

    # Iterar sobre la ventana alrededor del punto
    for y_w in range(-offset, offset + 1):
        for x_w in range(-offset, offset + 1):
            x, y = x_c + x_w, y_c + y_w # Coordenadas en la ventana

            # Calcular derivadas espaciales (Ix, Iy) y temporal (It)
            # Usar diferencias centrales en img1 para Ix, Iy
            Ix = (img1.get_pixel(x + 1, y) - img1.get_pixel(x - 1, y)) / 2.0
            Iy = (img1.get_pixel(x, y + 1) - img1.get_pixel(x, y - 1)) / 2.0
            # Usar diferencia temporal entre img2 e img1 para It
            It = img2.get_pixel(x, y) - img1.get_pixel(x, y)

            # Acumular en A y b
            A[0, 0] += Ix**2
            A[0, 1] += Ix * Iy
            A[1, 0] += Ix * Iy
            A[1, 1] += Iy**2
            b[0] -= Ix * It
            b[1] -= Iy * It

    # Resolver el sistema Av = b para v = [vx, vy]
    # v = A^{-1} * b
    try:
        # Calcular inversa de A
        A_inv = np.linalg.inv(A)
        # Calcular velocidad v
        v = A_inv @ b
        vx, vy = v[0], v[1]
    except np.linalg.LinAlgError:
        # Matriz A singular (ej. región sin textura), no se puede calcular flujo
        vx, vy = 0.0, 0.0

    return (vx, vy)


def seguimiento_movimiento(secuencia_imagenes, punto_inicial, ventana_lk=5):
    """
    Rastrea un punto a través de una secuencia de imágenes usando Lucas-Kanade.
    Args:
        secuencia_imagenes: lista de objetos Imagen
        punto_inicial: tupla (x, y) punto inicial en la primera imagen
        ventana_lk: tamaño de la ventana para Lucas-Kanade
    Returns:
        lista de tuplas (x, y) con la trayectoria estimada del punto
    """
    if not secuencia_imagenes or len(secuencia_imagenes) < 2:
        return [punto_inicial]

    trayectoria = [punto_inicial]
    punto_actual_x, punto_actual_y = float(punto_inicial[0]), float(punto_inicial[1])

    for i in range(len(secuencia_imagenes) - 1):
        img1 = secuencia_imagenes[i]
        img2 = secuencia_imagenes[i+1]

        # Calcular flujo óptico en la posición actual
        vx, vy = flujo_optico_lucas_kanade(img1, img2, (punto_actual_x, punto_actual_y), ventana=ventana_lk)

        # Actualizar la posición del punto
        punto_actual_x += vx
        punto_actual_y += vy
        
        # Redondear para la siguiente iteración (o mantener flotante)
        # punto_actual_int = (int(round(punto_actual_x)), int(round(punto_actual_y)))
        
        # Guardar posición (podría ser flotante para más precisión)
        trayectoria.append((punto_actual_x, punto_actual_y))

    return trayectoria


def estimacion_fondo_promedio(secuencia_imagenes):
    """
    Estima una imagen de fondo simple promediando los valores de píxeles
    a lo largo de una secuencia de imágenes.
    Args:
        secuencia_imagenes: lista de objetos Imagen
    Returns:
        objeto Imagen representando el fondo estimado, o None si la secuencia está vacía
    """
    num_imagenes = len(secuencia_imagenes)
    if num_imagenes == 0:
        return None

    ancho = secuencia_imagenes[0].ancho
    alto = secuencia_imagenes[0].alto
    fondo_estimado = Imagen(ancho, alto)
    
    # Acumular sumas de píxeles
    suma_pixeles = [[0.0 for _ in range(ancho)] for _ in range(alto)]
    for img in secuencia_imagenes:
        for y in range(alto):
            for x in range(ancho):
                 # Usar _get_pixel_clamp para evitar interpolación aquí
                 suma_pixeles[y][x] += img._get_pixel_clamp(x, y)

    # Calcular promedio y asignar a la imagen de fondo
    for y in range(alto):
        for x in range(ancho):
            promedio = suma_pixeles[y][x] / num_imagenes
            fondo_estimado.set_pixel(x, y, promedio)

    return fondo_estimado

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 52. Movimiento ===\n")

    # Crear secuencia simple: cuadrado moviéndose a la derecha
    ancho, alto = 30, 20
    secuencia = []
    for t in range(5): # 5 frames
        img = Imagen(ancho, alto)
        # Dibujar cuadrado
        x_start = 5 + t * 2 # Mover 2 píxeles por frame
        for y in range(5, 15):
             for x in range(x_start, x_start + 5):
                  img.set_pixel(x, y, 200) # Cuadrado claro
        secuencia.append(img)

    print(f"   Creada secuencia de {len(secuencia)} imágenes ({ancho}x{alto}) con cuadrado móvil.\n")

    # 1. Flujo Óptico (Lucas-Kanade)
    print("Flujo Óptico (Lucas-Kanade):")
    # Punto en el centro del cuadrado en el primer frame (t=0, x_start=5 -> centro x=7)
    punto_centro_inicial = (7, 10)
    img_t0 = secuencia[0]
    img_t1 = secuencia[1]

    vx, vy = flujo_optico_lucas_kanade(img_t0, img_t1, punto_centro_inicial, ventana=5)
    print(f"   Calculando flujo en {punto_centro_inicial} entre frame 0 y 1:")
    print(f"   Vector de flujo (vx, vy): ({vx:.2f}, {vy:.2f})")
    print(f"   (Esperado: vx ≈ 2.0, vy ≈ 0.0)\n")

    # 2. Seguimiento de Movimiento
    print("Seguimiento de Movimiento:")
    punto_seguir = (7, 10) # Punto inicial
    trayectoria = seguimiento_movimiento(secuencia, punto_seguir, ventana_lk=5)
    print(f"   Rastreando punto inicial {punto_seguir}:")
    print(f"   Trayectoria estimada:")
    for i, (px, py) in enumerate(trayectoria):
        print(f"      Frame {i}: ({px:.2f}, {py:.2f})")
        # (Posición x esperada: 7, 9, 11, 13, 15)
    print()

    # 3. Estimación de Fondo
    print("Estimación de Fondo:")
    fondo = estimacion_fondo_promedio(secuencia)
    print("   Imagen de fondo estimada (promedio de secuencia):")
    if fondo:
         # Mostrar ASCII es difícil para ver el promedio, pero podemos ver un pixel
         print(f"      Pixel (10,10) en fondo: {fondo.get_pixel(10, 10)}") # Debería ser intermedio
         # fondo.mostrar_ascii(escala=3) # Descomentar para visualizar
    else:
         print("      No se pudo estimar el fondo.")