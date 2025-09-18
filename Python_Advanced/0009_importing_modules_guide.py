'''
Este script es una guía completa sobre cómo importar y usar módulos en Python.
Los módulos permiten reutilizar código y organizar los programas de manera más efectiva.
Se demuestran las diferentes sintaxis de importación y sus casos de uso.
'''

# --- Guía de Importación y Uso de Módulos en Python ---

# Un módulo en Python es simplemente un archivo .py que contiene definiciones y declaraciones de Python.
# La biblioteca estándar de Python viene con una gran cantidad de módulos útiles.

# 1. La sentencia `import <módulo>`
# Esta es la forma más básica de importación. Carga el módulo completo en el espacio de nombres actual.
# Para acceder a sus funciones o atributos, se debe usar la notación de punto: `módulo.nombre_elemento`.

print("--- 1. Usando `import <módulo>` ---
")
import math

# Usamos la función `sqrt` y la constante `pi` del módulo `math`
raiz_cuadrada = math.sqrt(25)
valor_pi = math.pi

print(f"El módulo `math` ha sido importado.")
print(f"La raíz cuadrada de 25 es: {raiz_cuadrada}")
print(f"El valor de Pi es aproximadamente: {valor_pi}")

# 2. La sentencia `from <módulo> import <nombre>`
# Esta forma importa un nombre específico (función, clase, variable) directamente al espacio de nombres actual.
# No es necesario usar el prefijo del módulo para acceder a él.

print("
--- 2. Usando `from <módulo> import <nombre>` ---
")
from random import randint, choice

# `randint` y `choice` se pueden usar directamente sin el prefijo `random.`
numero_aleatorio = randint(1, 10)
fruta_elegida = choice(["manzana", "banana", "cereza"])

print(f"Se importaron `randint` y `choice` del módulo `random`.")
print(f"Número aleatorio entre 1 y 10: {numero_aleatorio}")
print(f"Fruta elegida al azar: {fruta_elegida}")

# 3. La sentencia `from <módulo> import *` (Importar todo)
# Esto importa todos los nombres públicos de un módulo al espacio de nombres actual.
# **Advertencia:** Esta práctica no es recomendada porque puede contaminar el espacio de nombres
# y hacer que sea difícil determinar de dónde proviene una función, además de poder sobrescribir
# funciones o variables existentes.

# from random import * # Ejemplo, no se ejecutará para mantener el código limpio.
# numero = random() # `random` ahora es una función directamente accesible.

# 4. Alias de Módulos y Funciones con `as`
# Se pueden crear alias (apodos) para módulos o funciones para acortar sus nombres o evitar conflictos.

print("
--- 4. Usando alias con `as` ---
")
# Alias para un módulo completo
import datetime as dt

# Alias para una función específica
from math import pow as potencia

fecha_actual = dt.datetime.now()
resultado_potencia = potencia(2, 3) # Equivalente a math.pow(2, 3)

print(f"Se importó `datetime` como `dt` y `math.pow` como `potencia`.")
print(f"La fecha y hora actual es: {fecha_actual}")
print(f"2 elevado a la potencia de 3 es: {resultado_potencia}")

# 5. La función `dir()` para explorar módulos
# `dir()` se puede usar para ver todos los nombres (funciones, clases, variables) que contiene un módulo.

print("
--- 5. Explorando un módulo con `dir()` ---
")
# print("Contenido del módulo `math`:")
# print(dir(math))
print("La función `dir(math)` mostraría todos los nombres disponibles en el módulo `math`.")

