import math

# ============================================================================
# 45. GRÁFICOS POR COMPUTADOR
# ============================================================================

class Punto3D:
    """Representa un punto en espacio 3D"""
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


def proyeccion_perspectiva(punto3d, distancia_focal=500, centro_x=0, centro_y=0):
    """
    Proyección de perspectiva simple de 3D a 2D (plano Z=0).
    Args:
        punto3d: objeto Punto3D
        distancia_focal: distancia de la cámara al plano de proyección
        centro_x, centro_y: centro de la pantalla (para desplazamiento)
    Returns:
        (x_2d, y_2d) coordenadas en el plano 2D
    """
    # Factor de escala basado en la distancia Z
    # Si z = 0, el punto está en el plano focal, factor = 1
    # Si z > 0 (lejos), factor < 1
    # Si z < 0 (cerca), factor > 1 (se agranda)
    # Evitar división por cero si z es exactamente -distancia_focal
    denominador = distancia_focal + punto3d.z
    if abs(denominador) < 1e-6:
        denominador = 1e-6 # Evitar división por cero

    factor = distancia_focal / denominador

    # Proyectar y desplazar al centro de la pantalla
    x_2d = punto3d.x * factor + centro_x
    y_2d = punto3d.y * factor + centro_y

    return (x_2d, y_2d)


def rotacion_3d(punto, angulo_x=0, angulo_y=0, angulo_z=0):
    """
    Aplica rotación en 3D alrededor de los ejes X, Y, Z (en ese orden).
    Args:
        punto: objeto Punto3D
        angulo_x, angulo_y, angulo_z: ángulos de rotación en radianes
    Returns:
        Nuevo objeto Punto3D rotado
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
    Ray tracing simple para detectar intersección rayo-esfera.
    Args:
        origen: lista/tupla [ox, oy, oz] punto de origen del rayo
        direccion: lista/tupla [dx, dy, dz] vector de dirección normalizado
        esfera_centro: lista/tupla [cx, cy, cz] centro de la esfera
        esfera_radio: radio de la esfera
    Returns:
        Distancia a la intersección más cercana, o float('inf') si no hay.
    """
    # Vector L del origen del rayo al centro de la esfera
    L = [esfera_centro[i] - origen[i] for i in range(3)]

    # Proyección de L sobre la dirección del rayo (tca)
    tca = sum(L[i] * direccion[i] for i in range(3))

    # Si tca < 0, la esfera está detrás del rayo
    if tca < 0:
        return float('inf')

    # Distancia al cuadrado del centro de la esfera a la línea del rayo (d^2)
    # d^2 = |L|^2 - tca^2
    d2 = sum(L[i]**2 for i in range(3)) - tca**2

    # Si d^2 > radio^2, el rayo no intersecta la esfera
    if d2 > esfera_radio**2:
        return float('inf')

    # Distancia desde tca al punto de intersección (thc)
    thc = math.sqrt(esfera_radio**2 - d2)

    # Distancias a los dos puntos de intersección
    t0 = tca - thc
    t1 = tca + thc

    # Devolver la intersección más cercana frente al rayo
    if t0 < 0: # Si t0 está detrás, usar t1
        if t1 < 0: return float('inf') # Ambas detrás
        return t1
    else:
        return t0 # t0 es la más cercana


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 45. Gráficos por Computador ===\n")

    # 1. Proyección 3D a 2D
    print("Proyección Perspectiva:")
    punto_3d = Punto3D(100, 50, 200) # x=100, y=50, z=200 (lejos)
    punto_2d = proyeccion_perspectiva(punto_3d, distancia_focal=100)
    print(f"   Punto 3D: {punto_3d}")
    print(f"   Proyección 2D (f=100): ({punto_2d[0]:.2f}, {punto_2d[1]:.2f})")
    # (Esperado: x_2d = 100 * 100/(100+200) = 33.33)

    punto_cercano = Punto3D(100, 50, -50) # z=-50 (cerca)
    punto_2d_cercano = proyeccion_perspectiva(punto_cercano, distancia_focal=100)
    print(f"   Punto cercano 3D: {punto_cercano}")
    print(f"   Proyección 2D (f=100): ({punto_2d_cercano[0]:.2f}, {punto_2d_cercano[1]:.2f})\n")
    # (Esperado: x_2d = 100 * 100/(100-50) = 200)

    # 2. Rotación 3D
    print("Rotación 3D:")
    punto_original = Punto3D(1, 0, 0)
    # Rotar 90 grados alrededor de Y (pi/2 radianes)
    punto_rotado_y = rotacion_3d(punto_original, angulo_y=math.pi/2)
    print(f"   Punto original: {punto_original}")
    print(f"   Rotado 90° en Y: {punto_rotado_y}")
    # (Esperado: (0.00, 0.00, -1.00))

    # Rotar 90 grados alrededor de Z
    punto_rotado_z = rotacion_3d(punto_original, angulo_z=math.pi/2)
    print(f"   Rotado 90° en Z: {punto_rotado_z}\n")
    # (Esperado: (0.00, 1.00, 0.00))

    # 3. Ray Tracing Simple (Esfera)
    print("Ray Tracing (Rayo-Esfera):")
    origen_rayo = [0, 0, -5]
    direccion_rayo = [0, 0, 1] # Hacia +Z (normalizado)
    centro_esfera = [0, 0, 0]
    radio_esfera = 2

    dist_interseccion = ray_tracing_simple(origen_rayo, direccion_rayo, centro_esfera, radio_esfera)
    print(f"   Rayo: Origen={origen_rayo}, Dirección={direccion_rayo}")
    print(f"   Esfera: Centro={centro_esfera}, Radio={radio_esfera}")
    if dist_interseccion != float('inf'):
        print(f"   Intersección encontrada a distancia: {dist_interseccion:.2f}")
        # (Esperado: t0 = tca - thc = 5 - sqrt(4-0) = 3)
    else:
        print("   No hay intersección.")