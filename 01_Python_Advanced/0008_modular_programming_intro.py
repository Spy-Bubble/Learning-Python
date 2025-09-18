'''
Este script introduce el concepto de programación modular en Python.
La programación modular consiste en dividir un programa grande en partes más pequeñas
y manejables llamadas módulos. Esto mejora la organización, reutilización y mantenimiento del código.
'''

# --- Introducción a la Programación Modular ---

# La programación modular no siempre requiere crear nuestros propios archivos.
# Empezamos a usarla desde el momento en que utilizamos funciones incorporadas (built-in)
# o módulos que vienen con Python.

# 1. Reutilización de Código a través de Funciones
# La función `len()` es un ejemplo de un componente modular. No necesitamos saber
# cómo está implementada internamente para usarla. Simplemente la importamos
# (en este caso, está disponible globalmente) y la usamos para obtener la longitud de un objeto.

texto_ejemplo = "Este es un texto de ejemplo para la demostración."

# Usamos la función modular `len()` para obtener la longitud del texto.
longitud_del_texto = len(texto_ejemplo)

print("--- Uso de Funciones Incorporadas como Módulos ---
")
print(f"El texto es: '{texto_ejemplo}'")
print(f"La longitud del texto es: {longitud_del_texto} caracteres.")

# 2. Beneficios de la Modularidad
# - **Abstracción:** No necesitamos conocer los detalles internos de `len()` para usarla.
# - **Reutilización:** Podemos usar `len()` en cualquier parte de nuestro código con cualquier secuencia.
# - **Mantenibilidad:** Si hubiera un error en `len()`, solo necesitaría ser corregido en un lugar.

# En los siguientes scripts, veremos cómo importar módulos más complejos que no están
# disponibles globalmente y cómo crear nuestros propios módulos para organizar nuestro código.

print("
Este simple acto de usar una función predefinida es el primer paso en la programación modular.")

