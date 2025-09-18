'''
Este script es una guía completa sobre el uso de paquetes en Python.
Un paquete es una forma de estructurar el espacio de nombres de los módulos de Python
utilizando "nombres de módulo con puntos". Un paquete es un directorio que contiene
módulos y un archivo especial `__init__.py`.

Para que este script funcione, debe existir una estructura de directorios como la siguiente:
mi_paquete/
    __init__.py
    modulo_a.py
    modulo_b.py
    sub_paquete/
        __init__.py
        modulo_c.py
'''

# --- Guía Completa de Uso de Paquetes en Python ---

# 1. Importación de módulos de un paquete
# Se utiliza la notación de punto para especificar la ruta del módulo dentro del paquete.

print("--- 1. Importando módulos específicos del paquete ---")
import mi_paquete.modulo_a
import mi_paquete.modulo_b

# Al importar, el código en `mi_paquete/__init__.py` se ejecuta una vez.

# Para usar las funciones, debemos usar la ruta completa.
resultado_a = mi_paquete.modulo_a.funcion_a()
resultado_b = mi_paquete.modulo_b.funcion_b()

print(f"Llamada a mi_paquete.modulo_a.funcion_a(): {resultado_a}")
print(f"Llamada a mi_paquete.modulo_b.funcion_b(): {resultado_b}")

# 2. Importación con la cláusula `from`
# Esto permite importar una función o módulo específico directamente al espacio de nombres actual.

print("\n--- 2. Usando `from` para importar directamente ---")
from mi_paquete.modulo_a import funcion_a
from mi_paquete import modulo_b as mod_b # Usando un alias

# Ahora `funcion_a` se puede llamar directamente, y `modulo_b` a través de su alias.
print(f"Llamada directa a funcion_a(): {funcion_a()}")
print(f"Llamada a través de alias mod_b.funcion_b(): {mod_b.funcion_b()}")

# 3. Importación de sub-paquetes
# La lógica es la misma, simplemente se extiende la ruta con más puntos.

print("\n--- 3. Importando desde un sub-paquete ---")
from mi_paquete.sub_paquete import modulo_c

resultado_c = modulo_c.funcion_c()
print(f"Llamada a modulo_c.funcion_c() desde el sub-paquete: {resultado_c}")

# 4. El archivo `__init__.py` y la importación con `*`
# El archivo `__init__.py` puede estar vacío, pero también puede contener código de inicialización
# o definir la variable `__all__`.

# `__all__` es una lista de strings que define qué módulos deben ser importados
# cuando se ejecuta `from <paquete> import *`.

print("\n--- 4. Usando `from mi_paquete import *` ---")
# Gracias a `__all__ = ['modulo_a', 'modulo_b']` en `mi_paquete/__init__.py`,
# los siguientes módulos estarán disponibles.
from mi_paquete import *

# Ahora podemos acceder a `modulo_a` y `modulo_b` directamente.
# Nota: esto importa los *módulos*, no las funciones dentro de ellos.
resultado_a_star = modulo_a.funcion_a()
print(f"Resultado de modulo_a.funcion_a() tras import *: {resultado_a_star}")

# 5. El guardián `if __name__ == '__main__'`
# Es una construcción común para hacer que el código de un módulo sea ejecutable
# solo cuando el archivo se corre directamente, pero no cuando se importa.

print("\n--- 5. Comportamiento de `__name__` ---")
print(f"Cuando se ejecuta este script directamente, su `__name__` es: '{__name__}'")

# Si importáramos `modulo_a`, su `__name__` sería 'mi_paquete.modulo_a'.
# Esto permite a los módulos saber si están siendo importados o ejecutados.

