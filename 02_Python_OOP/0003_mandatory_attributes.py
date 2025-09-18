"""
Este script explica cómo definir atributos obligatorios en las clases de Python.
Al declarar parámetros en el método `__init__` sin un valor por defecto, forzamos
a que se proporcionen sus valores al momento de crear una instancia.
"""

# --- Atributos Obligatorios en Clases de Python ---

# 1. El problema: Atributos opcionales y creación de objetos incompletos
# Si una clase no tiene un `__init__` o sus parámetros son opcionales, podemos crear
# objetos sin la información esencial, lo que puede llevar a errores más adelante.

class ProductoSimple:
    # Sin __init__, los atributos deben asignarse manualmente después de la creación.
    nombre = None
    precio = 0.0

# Podemos crear un objeto sin proporcionar datos importantes.
producto_incompleto = ProductoSimple()
print("--- Objeto con atributos no inicializados ---")
print(f"Nombre: {producto_incompleto.nombre}, Precio: {producto_incompleto.precio}")
# Esto puede causar problemas si intentamos operar con este objeto.

# 2. La solución: Parámetros obligatorios en `__init__`
# Al definir parámetros en `__init__` sin valores por defecto, Python exigirá
# que se pasen argumentos para ellos durante la instanciación.

class Producto:
    """
    Representa un producto con nombre y precio, que son obligatorios en su creación.
    """
    def __init__(self, nombre: str, precio: float, categoria: str = "General"):
        """
        Constructor que requiere un nombre y un precio.
        La categoría es opcional y tiene un valor por defecto.
        """
        # Atributos obligatorios
        self.nombre = nombre
        self.precio = precio
        # Atributo opcional
        self.categoria = categoria

    def mostrar_detalle(self):
        """Muestra los detalles del producto."""
        print(f"Producto: {self.nombre} | Precio: ${self.precio:.2f} | Categoría: {self.categoria}")

# 3. Intento de crear un objeto sin los atributos obligatorios
print("\n--- Intentando crear un objeto sin argumentos obligatorios ---")

try:
    # Esto fallará porque `nombre` y `precio` no se han proporcionado.
    producto_fallido = Producto(nombre="Producto de prueba", precio=0.0)
    producto_fallido.mostrar_detalle()
except TypeError as e:
    print(f"Error esperado al instanciar: {e}")

# 4. Creación correcta de un objeto
# Debemos proporcionar un argumento para cada parámetro obligatorio de `__init__`.
print("\n--- Creando objetos de forma correcta ---")

# Instancia proporcionando solo los argumentos obligatorios
laptop = Producto(nombre="Laptop Pro", precio=1200.50)
laptop.mostrar_detalle()

# Instancia proporcionando todos los argumentos
raton_gaming = Producto(nombre="Ratón Gamer RGB", precio=75.99, categoria="Periféricos")
raton_gaming.mostrar_detalle()

# Conclusión: Usar `__init__` con parámetros sin valores por defecto es la forma
# estándar en Python para asegurar que los objetos se creen con un estado inicial válido y datos iniciales válidos.