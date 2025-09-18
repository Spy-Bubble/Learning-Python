"""
Este script explica el concepto de herencia en Python, una de las características
fundamentales de la POO. La herencia permite crear nuevas clases (subclases)
que reutilizan, extienden y modifican el comportamiento definido en otras clases (superclases).
"""

# --- Herencia de Clases: Superclases y Subclases ---

# 1. Definición de la Superclase (Clase Padre o Base)
# Es la clase general de la cual otras clases heredarán atributos y métodos.

class Usuario:
    """
    Superclase que representa a un usuario genérico de una plataforma.
    Define la estructura y comportamiento común para todos los tipos de usuarios.
    """
    # Atributos de clase comunes
    plataforma = "MiPlataforma Online"

    def __init__(self, user_id: str, alias: str, nombre: str):
        """Constructor para los atributos básicos de cualquier usuario.""" 
        # Atributos de instancia
        self.user_id = user_id
        self.alias = alias
        self.nombre = nombre

    def mostrar_datos(self):
        """Método común para mostrar la información básica del usuario."""
        print(f"--- Datos del Usuario: {self.alias} ---")
        print(f"  ID: {self.user_id}")
        print(f"  Nombre: {self.nombre}")
        print(f"  Plataforma: {self.plataforma}")

# 2. Definición de una Subclase (Clase Hija o Derivada)
# Hereda de la superclase `Usuario` y puede añadir o modificar su funcionalidad.
# La sintaxis es: class NombreSubclase(NombreSuperclase):

class UsuarioPremium(Usuario):
    """
    Subclase que representa a un usuario Premium. Hereda todo de la clase `Usuario`
    y añade sus propias características específicas.
    """
    def __init__(self, user_id: str, alias: str, nombre: str, nivel_suscripcion: str):
        """Constructor de la subclase."""
        # `super()` llama al constructor de la superclase (`Usuario`)
        # para inicializar los atributos que se heredan (user_id, alias, nombre).
        super().__init__(user_id, alias, nombre)
        
        # Atributo específico de la subclase UsuarioPremium
        self.nivel_suscripcion = nivel_suscripcion

    # 3. Sobrescritura de Métodos
    # Podemos redefinir un método de la superclase para que se comporte de forma diferente.
    def mostrar_datos(self):
        """
        Sobrescribe el método `mostrar_datos` para incluir la información Premium.
        """
        # Primero, llamamos al método original de la superclase para no repetir código.
        super().mostrar_datos()
        
        # Añadimos la información extra de la subclase.
        print(f"  Suscripción: {self.nivel_suscripcion}")

    def realizar_envio_prioritario(self):
        """Método exclusivo de la clase UsuarioPremium."""
        print(f"¡Envío prioritario realizado para el usuario {self.alias}!")


# 4. Demostración de uso
print("--- Creando una instancia de la Superclase `Usuario` ---")
usuario_free = Usuario(user_id="001", alias="user_free", nombre="Juan Básico")
usuario_free.mostrar_datos()

print("\n--- Creando una instancia de la Subclase `UsuarioPremium` ---")
usuario_pro = UsuarioPremium(user_id="p001", alias="pro_gamer", nombre="Ana Pro", nivel_suscripcion="Oro")

# La instancia de la subclase llama a su método `mostrar_datos` sobrescrito.
usuario_pro.mostrar_datos()

# La instancia de la subclase también puede llamar a sus métodos exclusivos.
usuario_pro.realizar_envio_prioritario()

# La herencia permite la reutilización de código y la creación de una jerarquía lógica entre clases.