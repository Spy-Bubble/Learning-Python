# Las variables son contenedores que almacenan datos en la memoria

# 1. Existen 4 partes de una variable: 
dinero = 100
# Tipo de dato                 (int)
# Nombre de la variable        (dinero)
# Operador de asignación       (=) 
# Valor o dato que se almacena (100)

# Python usa tipado dinámico (No es necesario especificar el tipo de dato)

# 2. Los tipos de datos más comunes son:
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

# 3. Nomenclatura de variables
# Deben comenzar con una letra o un guion bajo (_)
# No pueden contener espacios (usar guion bajo para separar palabras)
# No pueden contener caracteres especiales (%, $, &, etc.)
# No pueden ser palabras reservadas (if, else, while, for, etc.)
# Son sensibles a mayúsculas y minúsculas (edad, Edad y EDAD son diferentes)

# 4. Inicializar variables
# "None" es un valor especial que indica la ausencia de valor
valor = None 

# 5. Inicializar variables con tipo de dato 
# Se usa cuando se quiere asegurar que la variable es de un tipo específico
numero = int()       # Inicializa con 0
decimal = float()    # Inicializa con 0.0
cadena = str()       # Inicializa con ''
booleano = bool()    # Inicializa con False
lista = list()       # Inicializa con []
diccionario = dict() # Inicializa con {}
conjunto = set()     # Inicializa con set()

# 6. Asignación múltiple de variables
a, b, c = 1, 2, 3
# a = 1, b = 2, c = 3

# 7. Intercambio de valores entre variables
x = 5
y = 10
# Intercambiar valores
x, y = y, x
# Ahora x = 10 y y = 5

# 8. Imprimir variables
print(dinero)        # Imprime el valor de la variable dinero

# 9. Reasignar valores a variables
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