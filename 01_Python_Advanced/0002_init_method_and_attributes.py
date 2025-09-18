'''
Este script explica el propósito y uso del método especial `__init__`, 
conocido como el constructor de la clase en Python. Se demuestra cómo inicializar
los atributos de una instancia de manera eficiente.
'''

# --- El Método Constructor `__init__` ---

# 1. El problema: Inicialización manual de atributos
# Sin un constructor, debemos asignar valores a los atributos de cada objeto manualmente después de su creación.

class MascotaSinInit:
    """Clase de ejemplo que muestra la inicialización manual de atributos."""
    nombre = None
    edad = 0

print("--- Sin __init__ (Inicialización Manual) ---")
perro = MascotaSinInit()
perro.nombre = "Fido"
perro.edad = 5

print(f"Mascota creada manualmente: Nombre: {perro.nombre}, Edad: {perro.edad} años.")

# Este proceso es repetitivo y propenso a errores, especialmente con muchos atributos o muchos objetos.

# 2. La solución: El método `__init__`
# Python ejecuta automáticamente el método `__init__` al crear una nueva instancia de una clase.
# Su principal objetivo es inicializar los atributos del objeto (atributos de instancia).

class Mascota:
    """
    Esta clase representa una mascota, utilizando el método `__init__`
    para establecer sus atributos al momento de la creación.
    """
    # Atributo de clase: compartido por todas las instancias de Mascota.
    reino = "Animalia"

    def __init__(self, nombre_mascota, edad_mascota, especie="Desconocida"):
        """
        El constructor de la clase. Se ejecuta al crear un nuevo objeto Mascota.
        
        Args:
            nombre_mascota (str): El nombre de la mascota.
            edad_mascota (int): La edad de la mascota.
            especie (str, optional): La especie de la mascota. Por defecto es "Desconocida".
        """
        print(f"¡Creando una nueva mascota de especie '{especie}'!")
        
        # Atributos de instancia: cada objeto Mascota tendrá su propio nombre y edad.
        self.nombre = nombre_mascota
        self.edad = edad_mascota
        self.especie = especie

    def saludar(self):
        """La mascota emite un saludo."""
        print(f"¡Hola! Soy {self.nombre} y tengo {self.edad} años.")

# 3. Creación de objetos usando `__init__`
# Ahora, podemos pasar los valores de los atributos directamente al crear la instancia.
print("\n--- Con __init__ (Inicialización Automática) ---")

gato = Mascota(nombre_mascota="Misi", edad_mascota=3, especie="Gato")
conejo = Mascota(nombre_mascota="Tambor", edad_mascota=2, especie="Conejo")

# Accedemos a los atributos que fueron inicializados por el constructor
print(f"Mascota 1: {gato.nombre} ({gato.especie}) - Reino: {gato.reino}")
print(f"Mascota 2: {conejo.nombre} ({conejo.especie}) - Reino: {conejo.reino}")

# Llamamos a un método que usa los atributos de instancia
gato.saludar()
conejo.saludar()