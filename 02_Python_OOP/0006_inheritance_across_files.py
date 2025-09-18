""" 
Este script principal demuestra cómo funciona la herencia de clases en Python
cuando la superclase y la subclase están definidas en archivos (módulos) diferentes.

Para que funcione, los siguientes archivos deben estar en el mismo directorio:
- `clase_base_vehiculo.py`: Contiene la superclase `Vehiculo`.
- `subclase_coche.py`: Contiene la subclase `Coche`.
"""

# --- Herencia de Clases en Diferentes Archivos ---

# 1. Importación de las Clases desde sus Módulos
# Importamos la superclase y la subclase de sus respectivos archivos.
from clase_base_vehiculo import Vehiculo
from subclase_coche import Coche

print("--- Demostración de Herencia entre Módulos ---")

# 2. Creación de una instancia de la Superclase
print("\nCreando una instancia de la superclase `Vehiculo`...")
vehiculo_generico = Vehiculo(marca="Genérica", modelo="V1")
vehiculo_generico.encender()
vehiculo_generico.describir()

# 3. Creación de una instancia de la Subclase
print("\nCreando una instancia de la subclase `Coche`...")
mi_coche = Coche(marca="Toyota", modelo="Corolla", numero_puertas=4)

# La instancia `mi_coche` tiene acceso tanto a los métodos heredados (`encender`)
# como a los métodos sobrescritos (`describir`).
mi_coche.encender()
mi_coche.describir()

# 4. Verificación de la Herencia
# La función `isinstance()` comprueba si un objeto es una instancia de una clase o de una subclase de ella.
# La función `issubclass()` comprueba si una clase es una subclase de otra.

print("\n--- Verificando la relación de herencia ---")
print(f"¿Es `mi_coche` una instancia de `Coche`? {isinstance(mi_coche, Coche)}")
print(f"¿Es `mi_coche` también una instancia de `Vehiculo`? {isinstance(mi_coche, Vehiculo)}")
print(f"¿Es la clase `Coche` una subclase de `Vehiculo`? {issubclass(Coche, Vehiculo)}")

# Este enfoque modular es la base de la organización de proyectos grandes en Python,
# permitiendo que el código sea limpio, reutilizable y fácil de mantener.