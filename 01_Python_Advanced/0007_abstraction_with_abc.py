'''
Este script explica la abstracción, un principio clave de la POO, utilizando el módulo `abc` de Python.
La abstracción permite definir una estructura común para un grupo de clases, obligándolas a implementar
ciertos métodos, pero ocultando los detalles complejos de implementación.
'''

# --- Abstracción con Clases Base Abstractas (ABC) ---

# Se importa la clase ABC (Abstract Base Class) y el decorador abstractmethod
from abc import ABC, abstractmethod

# 1. Creación de una Clase Base Abstracta
# Una clase abstracta sirve como una plantilla y no puede ser instanciada directamente.
# Se define heredando de ABC.
class Animal(ABC):
    """
    Clase base abstracta para todos los animales. Define una estructura común
    que todas las clases de animales concretos deben seguir.
    """
    def __init__(self, nombre):
        self.nombre = nombre

    # 2. Definición de un Método Abstracto
    # Un método abstracto se declara con el decorador @abstractmethod, pero no tiene implementación (solo `pass`).
    # Obliga a cualquier clase hija a implementar este método.
    @abstractmethod
    def emitir_sonido(self):
        """
        Método abstracto que debe ser implementado por cada subclase de Animal.
        Define la capacidad de emitir un sonido, pero no cómo se hace.
        """
        pass

    def describir(self):
        """Método concreto que las subclases heredan y pueden usar directamente."""
        print(f"Soy un animal y mi nombre es {self.nombre}.")

# 3. Intento de instanciar una clase abstracta (generará un error)
print("--- Intentando instanciar una clase abstracta ---")
try:
    animal_generico = Animal("Indefinido")
except TypeError as e:
    print(f"Error esperado: {e}")

# 4. Creación de Clases Concretas
# Estas clases heredan de la clase abstracta e implementan todos sus métodos abstractos.
class Perro(Animal):
    """Clase concreta que representa a un perro."""
    def emitir_sonido(self):
        # Implementación específica del método abstracto para la clase Perro
        print(f"{self.nombre} ladra: ¡Guau, guau!")

class Gato(Animal):
    """Clase concreta que representa a un gato."""
    def emitir_sonido(self):
        # Implementación específica del método abstracto para la clase Gato
        print(f"{self.nombre} maúlla: ¡Miau!")

# 5. Demostración de polimorfismo con clases concretas
print("\n--- Usando las clases concretas ---")

mi_perro = Perro("Toby")
mi_gato = Gato("Luna")

# Cada objeto llama a su propia versión implementada de `emitir_sonido`
mi_perro.describir()
mi_perro.emitir_sonido()

mi_gato.describir()
mi_gato.emitir_sonido()

# 6. ¿Qué pasa si una clase hija no implementa el método abstracto?
print("\n--- Intentando instanciar una clase que no implementa el método abstracto ---")

class Pez(Animal):
    """
    Esta clase generará un error al ser instanciada porque no implementa
    el método abstracto `emitir_sonido` de la clase `Animal`.
    """
    def nadar(self):
        print("Nadando...")

try:
    mi_pez = Pez("Nemo")
except TypeError as e:
    print(f"Error esperado: {e}")

