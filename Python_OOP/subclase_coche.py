""" 
Este módulo define la subclase `Coche`, que hereda de la clase `Vehiculo`
proveniente del módulo `clase_base_vehiculo`.
"""

# 1. Importación de la Superclase
# Para heredar de una clase que está en otro archivo, primero debemos importarla.
from clase_base_vehiculo import Vehiculo

# 2. Definición de la Subclase
class Coche(Vehiculo):
    """
    Subclase que representa un coche, heredando de `Vehiculo`.
    """
    def __init__(self, marca: str, modelo: str, numero_puertas: int):
        '"""Constructor de la clase Coche."""'
        # Se llama al constructor de la superclase para inicializar los atributos heredados.
        super().__init__(marca, modelo)
        # Atributo propio de la subclase
        self.numero_puertas = numero_puertas

    # Sobrescritura del método `describir`
    def describir(self):
        '"""Extiende la descripción para incluir el número de puertas."""'
        # Se llama al método original de la superclase.
        super().describir()
        # Se añade la información específica del coche.
        print(f"    Tipo: Es un coche con {self.numero_puertas} puertas.")