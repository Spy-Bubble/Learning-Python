'''
Este script es una guía completa sobre conceptos avanzados de funciones en Python,
incluyendo la sintaxis de `def`, funciones `lambda`, decoradores y generadores.
'''

# --- Guía Completa de Funciones en Python ---

# 1. Definición Básica de una Función con `def`
print("--- 1. Funciones básicas con `def` ---")

def saludar(nombre):
    """Esta función recibe un nombre y devuelve un saludo en formato string."""
    return f"¡Hola, {nombre}! Bienvenido a Python."

# Llamada a la función y almacenamiento del resultado
mensaje_saludo = saludar("Ana")
print(mensaje_saludo)

# 2. Argumentos: Posicionales, por Palabra Clave y por Defecto
print("\n--- 2. Tipos de Argumentos ---")

def describir_mascota(nombre, especie="perro", edad=0):
    """Describe una mascota usando diferentes tipos de argumentos."""
    return f"Mascota: {nombre}, es un {especie} de {edad} años."

# Usando solo argumentos posicionales y por defecto
print(describir_mascota("Fido"))

# Usando argumentos por palabra clave para cambiar el orden
print(describir_mascota(edad=5, nombre="Misi", especie="gato"))

# 3. Número Arbitrario de Argumentos Posicionales: `*args`
print("\n--- 3. Argumentos arbitrarios con `*args` ---")

def sumar_todos(*numeros):
    """Suma todos los números pasados como argumentos."""
    print(f"Argumentos recibidos como una tupla: {numeros}")
    return sum(numeros)

resultado_suma = sumar_todos(10, 20, 30, 40)
print(f"La suma total es: {resultado_suma}")

# 4. Número Arbitrario de Argumentos por Palabra Clave: `**kwargs`
print("\n--- 4. Argumentos arbitrarios con `**kwargs` ---")

def mostrar_info_usuario(**datos_usuario):
    """Muestra la información de un usuario recibida como pares clave-valor."""
    print(f"Argumentos recibidos como un diccionario: {datos_usuario}")
    for clave, valor in datos_usuario.items():
        print(f"  - {clave.capitalize()}: {valor}")

mostrar_info_usuario(nombre="Carlos", ciudad="Madrid", profesion="Ingeniero")

# 5. Funciones Anónimas: `lambda`
print("\n--- 5. Funciones anónimas `lambda` ---")

# Una función `lambda` es una pequeña función anónima definida en una sola línea.
# Sintaxis: lambda argumentos: expresion

# Equivalente a: def duplicar(n): return n * 2
duplicar = lambda n: n * 2

print(f"Resultado de la lambda `duplicar(5)`: {duplicar(5)}")

# Son muy útiles en combinación con funciones como `map`, `filter` y `sorted`.
lista_numeros = [1, 2, 3, 4, 5]
numeros_pares = list(filter(lambda x: x % 2 == 0, lista_numeros))
print(f"Filtrando pares con una lambda: {numeros_pares}")

# 6. Decoradores
print("\n--- 6. Decoradores ---")

# Un decorador es una función que toma otra función como argumento, le añade
# alguna funcionalidad y devuelve otra función, sin modificar el código de la función original.

def mi_decorador(funcion_a_decorar):
    """Decorador simple que imprime mensajes antes y después de la ejecución."""
    def wrapper():
        print("Inicio de la ejecución de la función.")
        funcion_a_decorar()
        print("Fin de la ejecución de la función.")
    return wrapper

@mi_decorador
def funcion_saludo():
    """Función simple que será decorada."""
    print("¡Hola desde la función decorada!")

# Al llamar a `funcion_saludo`, en realidad estamos llamando al `wrapper` devuelto por el decorador.
funcion_saludo()

# 7. Generadores
print("\n--- 7. Generadores ---")

# Un generador es un tipo especial de función que devuelve un iterador. Utiliza la
# palabra clave `yield` en lugar de `return` para devolver datos de uno en uno, 
# pausando su estado entre llamadas.

def generador_de_numeros_pares(limite):
    """Genera números pares hasta un límite."""
    numero = 0
    while numero < limite:
        yield numero
        numero += 2

print("Generando números pares hasta 10:")
for par in generador_de_numeros_pares(10):
    print(par, end=" ")
print()

