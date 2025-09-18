'''
Este script es una guía definitiva sobre la programación defensiva en Python,
centrándose en la anticipación y el manejo de errores a través de la gestión de excepciones.
'''

# --- Guía de Programación Defensiva y Manejo de Excepciones ---

# La programación defensiva implica escribir código que sea robusto y capaz de
# funcionar de manera predecible incluso frente a entradas inesperadas o errores.
# El manejo de excepciones con `try...except` es la herramienta principal para esto.

# 1. Errores Comunes en Python
# Antes de manejarlos, es útil reconocer los tipos de errores más comunes.
# - SyntaxError: Error en la sintaxis del código (ej. `if x > 5:` sin indentación).
# - NameError: Se intenta usar una variable no definida.
# - TypeError: Se aplica una operación a un tipo de dato incorrecto (ej. `10 + "a"`).
# - IndexError: Se intenta acceder a un índice que no existe en una secuencia.
# - KeyError: Se intenta acceder a una clave que no existe en un diccionario.
# - ZeroDivisionError: Se intenta dividir un número por cero.

# 2. El Bloque `try...except`
# Permite "intentar" ejecutar un bloque de código que podría fallar. Si ocurre una
# excepción (error en tiempo de ejecución), se ejecuta el bloque `except` en lugar de que el programa se detenga.

print("--- 2. Manejo de Excepciones con `try...except` ---")

def dividir_de_forma_segura(dividendo, divisor):
    print(f"\nIntentando dividir {dividendo} entre {divisor}...")
    try:
        # Código que podría generar una excepción
        resultado = dividendo / divisor
        print(f"El resultado de la división es: {resultado:.2f}")
    except ZeroDivisionError:
        # Este bloque solo se ejecuta si ocurre un ZeroDivisionError
        print("Error: No se puede dividir por cero. Por favor, introduce un divisor diferente.")
    except TypeError:
        # Este bloque solo se ejecuta si ocurre un TypeError
        print("Error: Ambos valores deben ser numéricos.")
    except Exception as e:
        # `Exception` es una clase base que captura la mayoría de las excepciones.
        # Es una buena práctica capturar excepciones inesperadas al final.
        print(f"Ha ocurrido un error inesperado: {e}")

# Caso exitoso
dividir_de_forma_segura(10, 2)

# Caso con ZeroDivisionError
dividir_de_forma_segura(10, 0)

# Caso con TypeError
dividir_de_forma_segura(10, "texto")

# 3. El Bloque `finally`
# El código dentro del bloque `finally` se ejecuta siempre, sin importar si ocurrió
# una excepción o no. Es ideal para tareas de "limpieza", como cerrar archivos o conexiones.

print("\n--- 3. El Bloque `finally` ---")

def leer_archivo(ruta_archivo):
    archivo = None # Inicializamos la variable fuera del try
    try:
        archivo = open(ruta_archivo, "r")
        contenido = archivo.read()
        print(f"Contenido del archivo '{ruta_archivo}':\n---")
        print(contenido)
        print("---")
    except FileNotFoundError:
        print(f"Error: El archivo en la ruta '{ruta_archivo}' no fue encontrado.")
    finally:
        # Este bloque se ejecuta siempre.
        if archivo:
            archivo.close()
            print(f"El archivo '{ruta_archivo}' ha sido cerrado.")
        else:
            print("No se abrió ningún archivo, no hay nada que cerrar.")

# Creamos un archivo de prueba para el caso exitoso
with open("test_file.txt", "w") as f:
    f.write("Este es un archivo de prueba.")

leer_archivo("test_file.txt")
print("\n")
leer_archivo("ruta_inexistente.txt")

# 4. Validar Entradas del Usuario
# Un bucle `while` con un bloque `try-except` es un patrón común para asegurar
# que el usuario introduce datos del tipo correcto.

print("\n--- 4. Validando la entrada del usuario ---")

def solicitar_numero_entero():
    while True:
        try:
            entrada = input("Por favor, introduce un número entero: ")
            numero = int(entrada)
            print(f"¡Gracias! Has introducido el número {numero}.")
            return numero
        except ValueError:
            print(f"Entrada no válida. '{entrada}' no es un número entero. Inténtalo de nuevo.")

# Descomenta la siguiente línea para probar la validación de entrada
# numero_validado = solicitar_numero_entero()

