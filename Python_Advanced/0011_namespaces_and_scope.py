'''
Este script proporciona una guía completa sobre los espacios de nombres y el ámbito (scope) en Python.
Entender estos conceptos es crucial para manejar cómo y dónde se pueden acceder a las variables.
'''

# --- Guía de Espacios de Nombres y Ámbito en Python ---

# Un espacio de nombres es un sistema que mapea nombres a objetos. Python utiliza diferentes
# espacios de nombres para evitar colisiones entre nombres.

# El ámbito (scope) de una variable es la región del código donde esa variable es accesible.
# Python sigue la regla LEGB para resolver nombres:
# L - Local: Dentro de la función actual.
# E - Enclosing (Encerrado): En el ámbito de cualquier función contenedora (para funciones anidadas).
# G - Global: En el nivel superior del módulo.
# B - Built-in (Incorporado): Nombres predefinidos en Python (ej. print, len).

# 1. Ámbito Global vs. Ámbito Local

variable_global = "Soy global"

print("--- 1. Ámbito Global vs. Local ---
")

def mi_funcion():
    # Esta variable solo existe dentro de esta función (ámbito local).
    variable_local = "Soy local"
    print(f"Dentro de la función, 'variable_local' es: '{variable_local}'")
    print(f"Dentro de la función, 'variable_global' es: '{variable_global}'")

mi_funcion()

print(f"\nFuera de la función, 'variable_global' es: '{variable_global}'")
# Intentar acceder a `variable_local` aquí daría un NameError.
# print(variable_local) # Descomentar para ver el error.

# 2. La palabra clave `global`
# Para modificar una variable global desde un ámbito local, debemos usar la palabra clave `global`.

print("
--- 2. Modificando el ámbito global con `global` ---
")
contador = 0

def incrementar_contador():
    global contador
    contador += 1
    print(f"Dentro de la función, el contador ahora es: {contador}")

print(f"Contador antes de llamar a la función: {contador}")
incrementar_contador()
print(f"Contador después de llamar a la función: {contador}")

# 3. Ámbito Encerrado (Enclosing) y la palabra clave `nonlocal`
# Se aplica a funciones anidadas. `nonlocal` permite modificar una variable
# de la función externa más cercana (que no sea global).

print("
--- 3. Ámbito Encerrado y `nonlocal` ---
")
def funcion_externa():
    variable_encerrada = "Original"

    def funcion_interna():
        nonlocal variable_encerrada
        variable_encerrada = "Modificada por la función interna"
        print(f"  - Dentro de la interna: '{variable_encerrada}'")

    print(f"Antes de llamar a la interna: '{variable_encerrada}'")
    funcion_interna()
    print(f"Después de llamar a la interna: '{variable_encerrada}'")

funcion_externa()

# 4. Espacio de Nombres Incorporado (Built-in)
# Contiene todas las funciones y excepciones que están siempre disponibles.

print("
--- 4. Ámbito Incorporado (Built-in) ---
")
print("La función `print` y `len` son ejemplos del espacio de nombres incorporado.")
longitud = len("ejemplo") # `len` es una función built-in.
print(f"La longitud de 'ejemplo' es: {longitud}")

# Podemos ver los nombres en los diferentes espacios de nombres con `globals()` y `locals()`.
print("
--- Explorando Espacios de Nombres ---
")
# print("Nombres globales:", globals().keys())

def otra_funcion():
    var_a = 1
    var_b = 2
    print("Nombres locales en `otra_funcion`:", locals().keys())

otra_funcion()

