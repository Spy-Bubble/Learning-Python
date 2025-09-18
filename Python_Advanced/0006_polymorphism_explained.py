'''
Este script explica el concepto de polimorfismo en Python, que permite que objetos
de diferentes clases respondan al mismo método o función de maneras específicas para cada clase.
'''

# --- Polimorfismo para Clases de Python ---

# 1. Polimorfismo con una función y objetos de diferentes clases
# El polimorfismo permite que una única función pueda tomar objetos de diferentes clases
# y ejecutar un método con el mismo nombre en ellos, obteniendo comportamientos distintos.

class Gato:
    """Clase que representa un gato."""
    def __init__(self, nombre):
        self.nombre = nombre

    def hablar(self):
        return "¡Miau!"

class Perro:
    """Clase que representa un perro."""
    def __init__(self, nombre):
        self.nombre = nombre

    def hablar(self):
        return "¡Guau!"

# Esta función demuestra el polimorfismo. No le importa el tipo de `animal`,
# solo que tenga un método `hablar()`.
def escuchar_animal(animal):
    """
    Ejecuta el método `hablar` de cualquier objeto animal que se le pase.
    
    Args:
        animal: Un objeto que debe tener un método `hablar()`.
    """
    print(f"{animal.nombre} dice: {animal.hablar()}")

print("--- Polimorfismo con Métodos de Clase ---
")
# Creamos instancias de diferentes clases
gato_michi = Gato("Michi")
perro_fido = Perro("Fido")

# Pasamos los diferentes objetos a la misma función
escuchar_animal(gato_michi)
escuchar_animal(perro_fido)

# 2. Polimorfismo en funciones incorporadas
# La función `len()` es un excelente ejemplo de polimorfismo. Funciona con diferentes
# tipos de datos (strings, listas, tuplas, diccionarios) porque cada uno de ellos
# implementa su propia versión de cómo calcular su "longitud".

print("
--- Polimorfismo en Funciones Incorporadas (len()) ---
")
texto = "Hola Mundo"
lista_numeros = [10, 20, 30, 40, 50]
diccionario_colores = {"rojo": "#FF0000", "verde": "#00FF00"}

print(f"La longitud del string '{texto}' es: {len(texto)}")
print(f"La longitud de la lista de números es: {len(lista_numeros)}")
print(f"La longitud del diccionario de colores es: {len(diccionario_colores)}")

# 3. Polimorfismo con Herencia
# El polimorfismo brilla cuando se combina con la herencia. Podemos tratar a todos los
# objetos de las clases hijas como si fueran de la clase padre.

class FiguraGeometrica:
    """Clase padre para cualquier figura geométrica."""
    def __init__(self, nombre):
        self.nombre = nombre

    def calcular_area(self):
        # Este método está diseñado para ser sobrescrito por las clases hijas.
        raise NotImplementedError("La clase hija debe implementar este método.")

class Rectangulo(FiguraGeometrica):
    """Representa un rectángulo y calcula su área."""
    def __init__(self, nombre, base, altura):
        super().__init__(nombre)
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

class Circulo(FiguraGeometrica):
    """Representa un círculo y calcula su área."""
    def __init__(self, nombre, radio):
        super().__init__(nombre)
        self.radio = radio

    def calcular_area(self):
        import math
        return math.pi * (self.radio ** 2)

print("
--- Polimorfismo con Herencia ---
")

figuras = [
    Rectangulo(nombre="Rectángulo 1", base=10, altura=5),
    Circulo(nombre="Círculo 1", radio=3)
]

# Iteramos a través de una lista de objetos de diferentes tipos
# y llamamos al mismo método `calcular_area` en cada uno.
for figura in figuras:
    area = figura.calcular_area()
    print(f"El área de la figura '{figura.nombre}' es: {area:.2f}")

