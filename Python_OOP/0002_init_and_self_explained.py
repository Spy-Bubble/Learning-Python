'''
Este script se centra en explicar el método `__init__` y el parámetro `self`,
dos de los conceptos más importantes en la Programación Orientada a Objetos con Python.
`__init__` es el constructor de la clase, y `self` representa la instancia del objeto.
'''

# --- El Método `__init__` y el Parámetro `self` ---

# 1. El problema: Atributos de Clase vs. Atributos de Instancia
# Los atributos de clase son compartidos por todas las instancias, lo que no siempre es deseable.

class PersonajeBasico:
    # Todas las instancias de PersonajeBasico compartirán estos mismos valores.
    puntos_de_vida = 100
    resistencia = 50

jugador = PersonajeBasico()
enemigo = PersonajeBasico()

enemigo.puntos_de_vida = 25 # Modificamos el atributo para esta instancia

print("--- Atributos de Clase (comportamiento no ideal) ---")
print(f"Vida del jugador: {jugador.puntos_de_vida}") # Sigue siendo 100
print(f"Vida del enemigo: {enemigo.puntos_de_vida}") # Es 25

# El problema es que no podemos definir atributos únicos al momento de crear el objeto.

# 2. La solución: El método constructor `__init__`
# El método `__init__` se ejecuta automáticamente cuando se crea un nuevo objeto (instancia).
# Su función principal es inicializar los atributos de esa instancia específica.

class Personaje:
    """
    Esta clase representa un personaje con atributos únicos definidos en su creación.
    """
    # `__init__` es el método constructor.
    # `self` es el primer parámetro y representa la instancia del objeto que se está creando.
    def __init__(self, nombre, vida, resistencia, experiencia=0):
        """
        Inicializa los atributos para cada nueva instancia de Personaje.
        """
        print(f"¡Creando un nuevo personaje llamado {nombre}!")
        
        # Atributos de instancia: Cada objeto tendrá su propio valor para estos atributos.
        # Usamos `self` para vincular el atributo a la instancia específica.
        self.nombre = nombre
        self.puntos_de_vida = vida
        self.resistencia = resistencia
        self.experiencia = experiencia

    def mostrar_estado(self):
        """
        Método que muestra el estado actual de los atributos de la instancia.
        """
        print(f"--- Estado de {self.nombre} ---")
        print(f"  - Vida: {self.puntos_de_vida}")
        print(f"  - Resistencia: {self.resistencia}")
        print(f"  - Experiencia: {self.experiencia}")

# 3. Creación de Objetos con Atributos de Instancia
print("\n--- Creando objetos con `__init__` ---")

# Al crear los objetos, pasamos los argumentos requeridos por `__init__`.
# Python pasa automáticamente la instancia (el objeto mismo) como el argumento `self`.
heroe = Personaje(nombre="Aragorn", vida=120, resistencia=80, experiencia=10)
jefe_final = Personaje(nombre="Sauron", vida=500, resistencia=150)

# Cada objeto ahora tiene su propio conjunto de atributos, independientes de los demás.
heroe.mostrar_estado()
jefe_final.mostrar_estado()

# Podemos añadir atributos a una instancia dinámicamente, aunque no es una práctica recomendada.
heroe.mana = 75
print(f"\nAtributo dinámico añadido a {heroe.nombre}: Mana = {heroe.mana}")