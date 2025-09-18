"""
Este script se enfoca en el uso de la función `super()` en la herencia de clases en Python.
`super()` permite a una subclase llamar a métodos de su superclase, lo cual es fundamental
para extender y reutilizar la funcionalidad sin duplicar código, especialmente en el constructor `__init__`.
"""

# --- Herencia de Clases y el Uso de `super()` ---

# 1. Definición de la Superclase (Clase Base)
class Vehiculo:
    """
    Superclase que define las características básicas de cualquier vehículo.
    """
    def __init__(self, marca: str, modelo: str, anio: int):
        """Constructor de la clase base."""
        print(f"Inicializando Vehiculo (Superclase) para {marca} {modelo}...")
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    def describir(self):
        """Devuelve una descripción general del vehículo."""
        return f"Vehículo del año {self.anio}, marca {self.marca}, modelo {self.modelo}."

# 2. Definición de la Subclase usando `super()`
class Coche(Vehiculo):
    """
    Subclase que representa un coche. Hereda de `Vehiculo`.
    """
    def __init__(self, marca: str, modelo: str, anio: int, numero_puertas: int):
        """
        Constructor de la subclase `Coche`.
        """
        print("Inicializando Coche (Subclase)...")
        
        # La función `super()` devuelve un objeto temporal de la superclase (Vehiculo),
        # lo que nos permite llamar a sus métodos. Aquí, llamamos al `__init__` de `Vehiculo`
        # para que se encargue de inicializar los atributos `marca`, `modelo` y `anio`.
        # Esto evita tener que escribir `self.marca = marca`, etc., de nuevo.
        super().__init__(marca, modelo, anio)
        
        # Ahora, inicializamos el atributo que es específico de la clase `Coche`.
        self.numero_puertas = numero_puertas

    # Sobrescritura de un método para añadir funcionalidad
    def describir(self):
        """
        Sobrescribe el método `describir` para añadir el número de puertas.
        """
        # Llamamos al método `describir` original de la superclase para reutilizar su lógica.
        descripcion_base = super().describir()
        
        # Añadimos la información específica de la subclase.
        return f"{descripcion_base} Es un coche con {self.numero_puertas} puertas."

# 3. Herencia Múltiple (Herencia en cadena)
class CocheDeportivo(Coche):
    """
    Esta clase hereda de `Coche`, que a su vez hereda de `Vehiculo`.
    """
    def __init__(self, marca: str, modelo: str, anio: int, numero_puertas: int, es_convertible: bool):
        print("Inicializando CocheDeportivo...")
        # `super()` aquí llama al `__init__` de la clase padre directa, que es `Coche`.
        super().__init__(marca, modelo, anio, numero_puertas)
        self.es_convertible = es_convertible

    def describir(self):
        descripcion_coche = super().describir()
        tipo_techo = "convertible" if self.es_convertible else "techo rígido"
        return f"{descripcion_coche} Además, es un deportivo {tipo_techo}."

# 4. Demostración de uso
print("--- Creando una instancia de CocheDeportivo ---")
mi_deportivo = CocheDeportivo("Ferrari", "F8 Tributo", 2023, 2, True)

print("\n--- Descripción Final ---")
# Al llamar a `describir`, se invoca la cadena de llamadas con `super()`
# CocheDeportivo.describir() -> Coche.describir() -> Vehiculo.describir()
print(mi_deportivo.describir())

print("\n--- Atributos de la instancia ---")
print(f"Marca: {mi_deportivo.marca}, Puertas: {mi_deportivo.numero_puertas}, Convertible: {mi_deportivo.es_convertible}")