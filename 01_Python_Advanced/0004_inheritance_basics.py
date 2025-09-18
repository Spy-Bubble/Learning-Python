'''
Este script introduce el concepto de herencia en la Programación Orientada a Objetos con Python.
La herencia permite que una clase (hija) adquiera los atributos y métodos de otra clase (padre).
'''

# --- Herencia en Clases de Python ---

# 1. Clase Padre (o Superclase)
# Es la clase de la cual otras clases heredarán.
class Vehiculo:
    """
    Clase base que representa un vehículo genérico.
    Define propiedades y comportamientos comunes a todos los vehículos.
    """
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.en_movimiento = False

    def describir(self):
        """Devuelve una descripción básica del vehículo."""
        return f"Vehículo: {self.marca} {self.modelo}"

    def arrancar(self):
        """Método genérico para poner en movimiento el vehículo."""
        if not self.en_movimiento:
            self.en_movimiento = True
            print(f"El {self.marca} {self.modelo} ha arrancado.")
        else:
            print("El vehículo ya está en movimiento.")

# 2. Clase Hija (o Subclase)
# Hereda de la clase `Vehiculo` y puede añadir o modificar funcionalidades.
# La sintaxis es `class NombreClaseHija(NombreClasePadre):`
class Coche(Vehiculo):
    """
    Clase que representa un coche. Hereda de `Vehiculo` y añade
    características específicas como el número de puertas.
    """
    def __init__(self, marca, modelo, num_puertas):
        # `super()` llama al constructor de la clase padre (`Vehiculo`).
        # Esto es crucial para asegurar que la inicialización del padre se complete.
        super().__init__(marca, modelo)
        self.num_puertas = num_puertas

    # 3. Sobrescritura de Métodos
    # Podemos redefinir un método de la clase padre para que se comporte de manera diferente.
    def describir(self):
        """Sobrescribe el método `describir` para incluir el número de puertas."""
        return f"Coche: {self.marca} {self.modelo} con {self.num_puertas} puertas."

    # Método específico de la clase Coche
    def tocar_bocina(self):
        """Acción exclusiva de los coches."""
        print("¡Beep, beep!")

# 4. Otra Clase Hija
class Bicicleta(Vehiculo):
    """
    Clase que representa una bicicleta. También hereda de `Vehiculo`,
    pero con un comportamiento de arranque diferente.
    """
    def __init__(self, marca, modelo, tipo):
        super().__init__(marca, modelo)
        self.tipo = tipo # Ej: "Montaña", "Urbana"

    # Sobrescritura de método con comportamiento específico
    def arrancar(self):
        """Las bicicletas no arrancan, se empieza a pedalear."""
        if not self.en_movimiento:
            self.en_movimiento = True
            print(f"Has empezado a pedalear tu bicicleta {self.marca} de {self.tipo}.")
        else:
            print("Ya estás pedaleando.")

# 5. Demostración de uso
print("--- Creando y usando instancias ---\n")

# Instancia de la clase padre
vehiculo_generico = Vehiculo("Genérico", "V1")
print(vehiculo_generico.describir())
vehiculo_generico.arrancar()

print("\n" + "-"*20 + "\n")

# Instancia de la clase hija `Coche`
mi_coche = Coche("Toyota", "Corolla", 4)
print(mi_coche.describir()) # Llama al método sobrescrito
mi_coche.arrancar()         # Llama al método heredado del padre
mi_coche.tocar_bocina()     # Llama a su método específico

print("\n" + "-"*20 + "\n")

# Instancia de la clase hija `Bicicleta`
mi_bici = Bicicleta("Trek", "Marlin", "Montaña")
print(mi_bici.describir()) # Llama al método heredado del padre
mi_bici.arrancar()         # Llama al método sobrescrito

