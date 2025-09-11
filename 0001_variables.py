# Las variables son contenedores que almacenan datos en la memoria

# Existen 4 partes de una variable: 
# 1. Tipo de dato (identificador)
# 2. Nombre de la variable
# 3. Operador de asignación (=)
# 4. Valor o dato que se almacena
dinero = 100
# 1.int  2.dinero  3.=  4.100
# Python usa tipado dinámico (No es necesario especificar el tipo de dato)

# Los tipos de datos más comunes son:
# int (enteros) 
dinero = 100
# float (decimales) 
pi = 3.14
# str (cadenas de texto) 
nombre = 'Juan'    
# bool (booleanos: True o False) 
es_mayor = True
# list (listas) 
frutas = ['manzana', 'banana', 'cereza']
# dict (diccionarios) 
persona = {'nombre': 'Ana', 'edad': 25}
# set (conjuntos) 
numeros = {1, 2, 3, 4, 5}

# Nomenclatura de variables
# 1. Deben comenzar con una letra o un guion bajo (_)
# 2. No pueden contener espacios (usar guion bajo para separar palabras)
# 3. No pueden contener caracteres especiales (%, $, &, etc.)
# 4. No pueden ser palabras reservadas (if, else, while, for, etc.)
# 5. Son sensibles a mayúsculas y minúsculas (edad, Edad y EDAD son diferentes)

# Inicializar variables
# "None" es un valor especial que indica la ausencia de valor
valor = None 

# Inicializar variables con tipo de dato 
numero = int()       # Inicializa con 0
decimal = float()    # Inicializa con 0.0
cadena = str()       # Inicializa con ''
booleano = bool()    # Inicializa con False
lista = list()       # Inicializa con []
diccionario = dict() # Inicializa con {}
conjunto = set()     # Inicializa con set()

# Asignación múltiple de variables
a, b, c = 1, 2, 3
# a = 1, b = 2, c = 3

# Intercambio de valores entre variables
x = 5
y = 10
# Intercambiar valores
x, y = y, x
# Ahora x = 10 y y = 5

# Imprimir variables
print(dinero)        # Imprime el valor de la variable dinero

# Reasignar valores a variables
dinero = 200        # Ahora dinero vale 200 en lugar de 100
print(dinero)       # Imprime el nuevo valor de la variable dinero

# Buena práctica
# Seguir las convenciones de estilo de Python (PEP 8)
# Más info: https://peps.python.org/pep-0008/
# Convención de Nomenclatura: 
# 1.naming variables (snake_case)
# 2.functions (snake_case) 
# 3.classes (CamelCase) 
# 4.constants (ALL_CAPS_WITH_UNDERSCORES)