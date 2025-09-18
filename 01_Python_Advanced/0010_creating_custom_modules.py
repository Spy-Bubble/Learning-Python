
'"""
Este script demuestra cómo crear y utilizar tus propios módulos en Python.
Para que esto funcione, un archivo llamado `operaciones.py` debe existir en el mismo directorio.
"""'

# --- Creando y Usando Módulos Propios ---

# Python nos permite crear nuestros propios módulos. Un módulo es simplemente un archivo .py
# que contiene código reutilizable (funciones, clases, variables).

# 1. Creación del Módulo
# Se ha creado un archivo llamado `operaciones.py` que contiene:
# - Una función `sumar(a, b)`
# - Una función `restar(a, b)`
# - Una constante `PI`

# 2. Importación del Módulo Personalizado
# Podemos importar nuestro módulo `operaciones` de la misma manera que importamos módulos estándar.

print("--- Importando el módulo 'operaciones' completo ---")
import operaciones

# Ahora podemos usar las funciones y constantes del módulo con la notación de punto.
suma_resultado = operaciones.sumar(15, 7)
resta_resultado = operaciones.restar(10, 4)
valor_pi = operaciones.PI

print(f"Resultado de operaciones.sumar(15, 7): {suma_resultado}")
print(f"Resultado de operaciones.restar(10, 4): {resta_resultado}")
print(f"Valor de la constante PI en el módulo: {valor_pi}")

# 3. Importación de elementos específicos del módulo
# También podemos importar solo las partes que necesitamos.

print("\n--- Importando elementos específicos de 'operaciones' ---")
from operaciones import sumar, PI

# Ahora `sumar` y `PI` se pueden usar directamente.
suma_directa = sumar(100, 200)

print(f"Resultado de sumar(100, 200) directamente: {suma_directa}")
print(f"Usando la constante PI directamente: {PI}")

# Este enfoque modular ayuda a mantener el código organizado, reutilizable y fácil de mantener.

