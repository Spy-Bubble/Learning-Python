'''
Este script proporciona una introducción a las clases en Python, explicando su definición,
los atributos, los métodos y cómo los tipos de datos incorporados también son clases.
'''

# --- Introducción a las Clases en Python ---

# 1. Definición de una clase simple
# Una clase es una plantilla para crear objetos. Se define con la palabra clave 'class'.
# Por convención, los nombres de las clases usan la notación CamelCase.
class MiPrimeraClase:
    """
    Esta es una clase de ejemplo para demostrar la sintaxis básica.
    El docstring dentro de una clase explica su propósito general.
    """
    # La palabra clave 'pass' se utiliza cuando una definición de clase o función está vacía.

# 2. Clases con atributos y métodos
# Las clases pueden contener atributos (variables) y métodos (funciones).
class Vehiculo:
    """
    Esta clase representa un vehículo genérico y define sus características y comportamientos básicos.
    """
    # Atributos de clase: son variables que pertenecen a la clase y son compartidas
    # por todas las instancias (objetos) de esta clase.
    ruedas = 4
    color = "Rojo"
    longitud_metros = 3.5

    # Métodos: son funciones definidas dentro de una clase que describen
    # los comportamientos de los objetos.
    def arrancar(self):
        """Este método simula el arranque del motor del vehículo."""
        print("El motor del vehículo ha arrancado.")

    def detener(self):
        """Este método simula la detención del motor del vehículo."""
        print("El motor del vehículo se ha detenido.")

# 3. Los tipos de datos en Python también son clases
# En Python, todo es un objeto, y cada objeto es una instancia de una clase.
# La función type() nos permite inspeccionar la clase de cualquier objeto.

# Ejemplo con una cadena de texto (string)
mi_texto = "Python es un lenguaje orientado a objetos"
print(f"Texto original: '{mi_texto}'")
print(f"La variable 'mi_texto' es una instancia de la clase: {type(mi_texto)}")

# Al ser un objeto de la clase 'str', tiene acceso a sus métodos, como .upper()
texto_en_mayusculas = mi_texto.upper()
print(f"Texto transformado a mayúsculas: '{texto_en_mayusculas}'")