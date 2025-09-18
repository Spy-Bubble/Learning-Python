'''
Este script es una introducción a las buenas prácticas de documentación en Python.
Cubre comentarios, anotaciones de tipo (type hints) y docstrings, elementos esenciales
para escribir código claro, legible y mantenible.
'''

# --- Introducción a la Documentación con Python ---

# 1. Comentarios
# Los comentarios son notas para los desarrolladores y son ignorados por el intérprete de Python.
# Se usan para explicar el "porqué" del código, no el "qué".

print("--- 1. Comentarios ---")

# Esto es un comentario de una sola línea. Explica una parte compleja del código.
# Fórmula para calcular el interés compuesto
capital = 1000  # Capital inicial
tasa_interes = 0.05  # Tasa de interés anual

# Comentarios especiales (etiquetas comunes):
# TODO: Indica una tarea pendiente.
# FIXME: Señala un problema conocido que necesita ser corregido.
# BUG: Describe un error específico.
# NOTE: Una nota importante sobre el código.

# TODO: Implementar la validación de la tasa de interés.
# FIXME: La función no maneja correctamente valores negativos de capital.

print("Los comentarios ayudan a entender la lógica detrás del código.")

# 2. Anotaciones de Tipo (Type Hints)
# Son una forma de indicar explícitamente el tipo de dato esperado para una variable,
# el parámetro de una función o el valor de retorno. No son obligatorias, pero
# mejoran la legibilidad y permiten el uso de herramientas de análisis estático.

print("\n--- 2. Anotaciones de Tipo (Type Hints) ---")

def calcular_precio_final(precio_base: float, impuesto: float) -> float:
    """Calcula el precio final aplicando un impuesto."""
    return precio_base * (1 + impuesto)

# `-> None` se usa para indicar que una función no devuelve ningún valor.
def imprimir_saludo(nombre: str) -> None:
    """Imprime un saludo en la consola."""
    print(f"Hola, {nombre}")

precio_con_impuesto = calcular_precio_final(100.0, 0.21)
print(f"El precio final es: {precio_con_impuesto}")
imprimir_saludo("Mundo")

# 3. Docstrings (Cadenas de Documentación)
# Un docstring es una cadena de texto que aparece como la primera declaración en un
# módulo, función, clase o método. Su propósito es documentar lo que hace el código.

print("\n--- 3. Docstrings ---")

def potencia(base: int, exponente: int) -> int:
    '''Devuelve el resultado de elevar la base al exponente.

    Esta es una docstring multi-línea. La primera línea es un resumen conciso.
    Después de una línea en blanco, se pueden añadir más detalles sobre el
    funcionamiento, los parámetros y lo que devuelve.

    Args:
        base (int): El número base.
        exponente (int): El exponente al que se eleva la base.

    Returns:
        int: El resultado de base elevado al exponente.
    '''
    return base ** exponente

# 4. Accediendo a la Documentación
# Los docstrings se almacenan en el atributo `__doc__` y pueden ser accedidos
# programáticamente o a través de la función `help()`.

print("\n--- 4. Accediendo a la Documentación ---")

# Usando el atributo __doc__
print("Accediendo a través de `__doc__`:")
print(potencia.__doc__)

# Usando la función help()
print("\nAccediendo a través de `help()`:")
# help(potencia) # Descomentar para ver la ayuda interactiva en una consola.
print("La función `help(potencia)` mostraría la información del docstring de forma amigable.")

