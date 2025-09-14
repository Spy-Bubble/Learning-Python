# 1. Entrada de datos input()
# La función input() permite al usuario ingresar datos desde la consola.
nombre = input("¿Cuál es tu nombre? ")

# 2. Salida de datos print()
# La función print() muestra datos en la consola.
print("Hola, " + nombre + "!")
# Los (+) son otra forma de concatenar cadenas. Normalamente se usan las comas(,).

edad = input("¿Cuántos años tienes? ")
print("Tienes", edad, "años.")

# También puedes usar f-strings para formatear la salida.
# Las f-strings son cadenas de texto que permiten incrustar expresiones dentro de llaves {}.
# Se definen anteponiendo una 'f' antes de las comillas.
print(f"{nombre} tiene {edad} años.")

# Los parametroas internos de la funcion print() son:
# args: los valores a imprimir.
# sep: define el separador entre los argumentos (por defecto es un espacio).
# end: define el carácter que se imprime al final (por defecto es un salto de línea).
print("Python", "es", "genial", sep=" ", end="!\n")



