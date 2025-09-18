# Las tuplas son similares a las listas, pero con una diferencia clave: son inmutables.
# Esto significa que una vez que se crea una tupla, no se pueden cambiar sus elementos.

# 1. Crear una tupla:
# Usamos paréntesis () para definir una tupla y separamos los elementos con comas.
colores = ("rojo", "verde", "azul", "amarillo")  

# 2. Acceder a elementos de una tupla:
# Al igual que las listas, podemos acceder a los elementos de una tupla usando índices. 
print(colores[0])  # Salida: rojo (primer elemento)
print(colores[3])  # Salida: amarillo (cuarto elemento)

# 3. Métodos de tuplas:
# Las tuplas tienen pocos métodos debido a su inmutabilidad.

# Método count() para contar cuántas veces aparece un elemento en la tupla.
# Pasamos el valor que queremos contar como argumento a count().
cantidad_rojo = colores.count("rojo")  # Cuenta cuántas veces aparece "rojo"
print(cantidad_rojo)  # Salida: 1
# Si el valor no está en la tupla, count() devuelve 0.
cantidad_naranja = colores.count("naranja")  # Cuenta cuántas veces aparece "naranja"
print(cantidad_naranja)  # Salida: 0

# Método index() para encontrar el índice de la primera aparición de un valor.
# Pasamos el valor que queremos buscar como argumento a index().
indice_verde = colores.index("verde")  # Encuentra el índice de "verde"
print(indice_verde)  # Salida: 1
# Si el valor no está en la tupla, se genera un ValueError.
# indice_naranja = colores.index("naranja")  # Esto causará un ValueError

# 4. Cuando usar tuplas vs listas:
# Usamos tuplas cuando queremos asegurarnos de que los datos no cambien.
# Las tuplas son útiles para almacenar datos que deben permanecer constantes, como coordenadas (x, y) o días de la semana.
# Usamos listas cuando necesitamos una colección de elementos que pueda cambiar, como una lista de tareas o una lista de compras.

# 5. Desempaquetado de tuplas:
# Podemos asignar los valores de una tupla a múltiples variables en una sola línea.
desempaquetar_colores = ("rojo", "verde", "azul", "amarillo")
color1, color2, color3, color4 = desempaquetar_colores
print(color1)  
print(color2)
print(color3)
print(color4)
# Esto tambien funciona con listas.
# Tratar de desempaquetar más o menos variables de las que hay en la tupla o lista causará un ValueError.

# 6. recoger exceso de valores con *
# Podemos usar el operador * para recoger múltiples valores en una variable.
numeros = (0, 1, 2, 3, 4, 5, 6)
num1, num2, *otros_numeros = numeros
print(num1)
print(num2)
print(otros_numeros)  # otros_numeros es una lista con los valores restantes
# Podemos usar * en cualquier posición, pero solo una vez en la asignación.
num1, *otros_numeros, num6 = numeros
print(num1)
print(num6)
print(otros_numeros)

# 7. Convertir entre listas y tuplas:
# Convertir una lista en una tupla usando la función tuple().
lista_frutas = ["manzana", "banana", "cereza"]
tupla_frutas = tuple(lista_frutas)
print(tupla_frutas)

# Convertir una tupla en una lista usando la función list().
tupla_marcas = ("Nike", "Adidas", "Puma")
lista_marcas = list(tupla_marcas)
print(lista_marcas)