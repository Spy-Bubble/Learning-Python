"""
Este script es una introducción fundamental a la Programación Orientada a Objetos (POO) en Python.
Define una clase simple y crea un objeto (instancia) a partir de ella.
"""

# --- Iniciación a la Programación Orientada a Objetos (POO) ---

# 1. Definición de una Clase
# Una clase es una plantilla o un plano para crear objetos.
# Contiene atributos (datos) y métodos (comportamientos) que los objetos de esa clase tendrán.
# Por convención, los nombres de las clases en Python usan la notación `CamelCase`.

class Coche:
    """Esta es una clase simple que representa un Coche."""
    # La palabra clave `pass` se usa cuando una declaración es requerida sintácticamente
    # pero no se quiere ejecutar ningún código. Es un marcador de posición.
    pass

# 2. Creación de un Objeto (Instanciación)
# Un objeto es una instancia de una clase. Se crea llamando a la clase como si fuera una función.
# Cada objeto creado a partir de la clase `Coche` será una entidad independiente.

mi_primer_coche = Coche()

# 3. Verificación del Objeto
# Podemos imprimir el objeto y su tipo para verificar que ha sido creado correctamente.

print("--- Creación de Clases y Objetos ---")
print(f"Hemos creado nuestro primer objeto: {mi_primer_coche}")
print(f"El tipo de nuestro objeto es: {type(mi_primer_coche)}")

# La salida mostrará que `mi_primer_coche` es un objeto de la clase `Coche`
# y la dirección de memoria donde está almacenado.

