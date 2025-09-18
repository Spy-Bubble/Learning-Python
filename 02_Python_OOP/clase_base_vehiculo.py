"""
Este módulo contiene la clase base `Vehiculo`, que servirá como superclase
para otros módulos que definan tipos específicos de vehículos.
"""

class Vehiculo:
    """
    Superclase que define las características y comportamientos generales de un vehículo.
    """
    def __init__(self, marca: str, modelo: str):
        """Constructor de la clase Vehiculo."""
        self.marca = marca
        self.modelo = modelo
        self.encendido = False

    def encender(self):
        """Enciende el motor del vehículo."""
        self.encendido = True
        print(f"El motor del {self.marca} {self.modelo} se ha encendido.")

    def describir(self):
        """Muestra la descripción básica del vehículo."""
        estado = "encendido" if self.encendido else "apagado"
        print(f"--- Vehículo: {self.marca} {self.modelo} ---")
        print(f"    Estado: El motor está {estado}.")