'''
Este script explica los conceptos fundamentales de los objetos en Python, 
demostrando cómo crear instancias de una clase, acceder y modificar sus atributos, y llamar a sus métodos.
'''

# --- Objetos en Python: Instancias de Clases ---

# Primero, definimos una clase que servirá como plantilla para nuestros objetos.
class Vehiculo:
    """
    Esta clase representa un vehículo genérico. Todas las instancias de Vehiculo
    compartirán estos atributos y métodos iniciales.
    """
    # Atributo de clase: es el mismo para todas las instancias de la clase.
    ruedas = 4
    
    # Atributos de instancia (inicializados con valores por defecto)
    color = "Blanco"
    longitud_metros = 3.0

    def arrancar(self):
        """Simula el arranque del motor del vehículo."""
        print("El motor ha arrancado.")

    def detener(self):
        """Simula la detención del motor del vehículo."""
        print("El motor se ha detenido.")

# 1. Creación de objetos (Instanciación)
# Un objeto es una instancia de una clase. Se crea llamando a la clase como si fuera una función.
# Cada objeto es una entidad independiente con su propia memoria.

coche_deportivo = Vehiculo()
camioneta = Vehiculo()

print("--- Creación de Objetos ---")
print(f"Objeto 1 (coche_deportivo): {coche_deportivo}")
print(f"Objeto 2 (camioneta): {camioneta}")
print("Nota: Cada objeto tiene una dirección de memoria única.")

# 2. Acceso a los atributos de un objeto
# Se utiliza la notación de punto (objeto.atributo) para acceder a los valores.
print("\n--- Acceso a Atributos ---")
print(f"El coche deportivo tiene {coche_deportivo.ruedas} ruedas.")
print(f"El color inicial de la camioneta es {camioneta.color}.")

# 3. Modificación de los atributos de un objeto
# Los atributos de un objeto pueden ser modificados. Estos cambios solo afectan a esa instancia específica.
print("\n--- Modificación de Atributos ---")
coche_deportivo.color = "Rojo Fuego"
camioneta.color = "Azul Océano"
camioneta.longitud_metros = 5.2

print(f"Nuevo color del coche deportivo: {coche_deportivo.color}")
print(f"Nuevo color de la camioneta: {camioneta.color}")
print(f"Longitud del coche deportivo: {coche_deportivo.longitud_metros} metros.")
print(f"Longitud de la camioneta: {camioneta.longitud_metros} metros.")

# 4. Creación de atributos de instancia dinámicamente
# Python permite añadir nuevos atributos a una instancia en cualquier momento.
# Sin embargo, esto no es una práctica recomendada, ya que puede llevar a errores.
print("\n--- Atributos Dinámicos (No recomendado) ---")
coche_deportivo.velocidad_maxima_kmh = 250
print(f"Velocidad máxima del coche deportivo: {coche_deportivo.velocidad_maxima_kmh} km/h")

# Si intentamos acceder a este atributo en otra instancia, obtendremos un error.
# print(f"Velocidad máxima de la camioneta: {camioneta.velocidad_maxima_kmh}") # Esto daría un AttributeError

# 5. Llamada a los métodos de un objeto
# Los métodos también se invocan usando la notación de punto.
print("\n--- Llamada a Métodos ---")
print("Acciones del coche deportivo:")
coche_deportivo.arrancar()
coche_deportivo.detener()

print("\nAcciones de la camioneta:")
camioneta.arrancar()