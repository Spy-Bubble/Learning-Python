# Las listas nos permiten almacenar múltiples valores en una sola variable.

# 1. Podemos crear una lista utilizando corchetes [] y separando los elementos con comas: 
frutas = ["manzana", "banana", "cereza"]  # Lista de cadenas
numeros = [1, 2, 3, 4, 5]  # Lista de enteros
# Las listas nos permiten mezclar diferentes tipos de datos:
tenis = ["Nike", 1000, "Blanco", True]  # Lista mixta
# Aquí, 'tenis' contiene una cadena, un entero, otra cadena y un booleano.

# 2. Para imprimir una lista completa, simplemente usamos la función print():
print(frutas)  
print(numeros) 
print(tenis)  

# 3. Podemos acceder a elementos individuales de una lista utilizando índices:
# Los índices comienzan en 0, por lo que el primer elemento está en el índice 0.
print(frutas[0])  # Salida: manzana (primer elemento)
print(numeros[2])      
print(tenis[3]) 
# También podemos usar índices negativos para acceder desde el final de la lista:
print(frutas[-1])  # Salida: cereza (último elemento)   
print(numeros[-2])  
print(tenis[-3])  

# 4. Reasignar un valor a un elemento de la lista:
# Solo necesitamos usar el índice del elemento que queremos cambiar y asignarle un nuevo valor.
frutas[1] = "kiwi"  # Cambiamos "banana" por "kiwi"
print(frutas)  
numeros[0] = 10  # Cambiamos 1 por 10   
print(numeros)  
tenis[3] = False  # Cambiamos True por False
print(tenis)  

# 5. Error por número de índice fuera de rango:
# Si intentamos acceder a un índice que no existe en la lista, obtendremos un error IndexError.
# Por ejemplo, si una lista tiene 3 elementos, los índices válidos son 0, 1 y 2.
# print(frutas[3])  # Esto causará un IndexError
# print(tenis[-5])   # Esto también causará un IndexError

# 6. Añadir elementos nuevos a una lista:
# Método append() para añadir un elemento al final de la lista.
# Para usarlo, escribimos el nombre de la lista seguido de .append() y pasamos el nuevo elemento como argumento.
frutas.append("uva")  # Añadimos "uva" al final de la lista
print(frutas)  
numeros.append(6)  # Añadimos 6 al final de la lista
print(numeros)
tenis.append(25.5)  # Añadimos 25.5 al final de la lista
print(tenis)

# Método insert() para añadir un elemento en una posición específica.
# Usamos .insert() con dos argumentos: el índice donde queremos insertar el nuevo elemento y el elemento en sí.
frutas.insert(1, "mango")  # Insertamos "mango" en el índice 1
print(frutas)
numeros.insert(0, 0)  # Insertamos 0 en el índice 0
print(numeros) 

# Metodo extend() para añadir múltiples elementos al final de la lista o fucionar con otra lista.
# Usamos .extend() y pasamos otra lista con los nuevos elementos.
frutas.extend(["pera", "piña"])  # Añadimos "pera" y "piña" al final
print(frutas)
numeros.extend([7, 8, 9])  # Añadimos 7, 8 y 9 al final
print(numeros)

# 7. Eliminar elementos de una lista:
# Método pop() para eliminar y devolver el último elemento de la lista.
# Si queremos esliminar la ultima posición, no necesitamos pasar ningún argumento.
# Si queremos eliminar un elemento específico, podemos pasar su índice como argumento a pop().
ultima_fruta = frutas.pop()  # Elimina y devuelve el último elemento
print(ultima_fruta)
print(frutas)
fruta_indice_1 = frutas.pop(1)  # Elimina y devuelve el elemento en el índice 1
print(fruta_indice_1)
print(frutas)

# Método remove() para eliminar la primera aparición de un valor específico.
# Pasamos el valor que queremos eliminar como argumento a remove().
numeros.remove(10)  # Elimina la primera aparición de 10
print(numeros)
# Si el valor no está en la lista, se genera un ValueError.
# numeros.remove(100)  # Esto causará un ValueError

# Método clear() para eliminar todos los elementos de la lista.
# No necesita argumentos.
tenis.clear()  # Elimina todos los elementos de la lista 'tenis'
print(tenis)
# Ahora 'tenis' es una lista vacía: []

# 8. Buscar elementos en una lista:
# Método index() para encontrar el índice de la primera aparición de un valor.
# Pasamos el valor que queremos buscar como argumento a index().
indice_uva = frutas.index("uva")  # Encuentra el índice de "uva"
print(indice_uva)
# Si el valor no está en la lista, se genera un ValueError.
# indice_naranja = frutas.index("naranja")  # Esto causará un ValueError

# Método count() para contar cuántas veces aparece un valor en la lista.
agregar_frutas_repetidas = ["manzana", "banana", "uva", "manzana"]
frutas.extend(agregar_frutas_repetidas)  # Añadimos frutas repetidas
print(frutas)
# Pasamos el valor que queremos contar como argumento a count().
cantidad_manzanas = frutas.count("manzana")  # Cuenta cuántas veces aparece "manzana"
print(cantidad_manzanas)
# Si el valor no está en la lista, count() devuelve 0.
cantidad_naranjas = frutas.count("naranja")  # Cuenta cuántas veces aparece "naranja"
print(cantidad_naranjas)  # Salida: 0

# 9. Ordenar y revertir una lista:
# Método reverse() para invertir el orden de los elementos en la lista.
# No necesita argumentos.
numeros.reverse()  # Invierte el orden de la lista 'numeros'
print(numeros)

# Método sort() para ordenar los elementos de la lista en orden ascendente.
# No necesita argumentos.
numeros.sort()  # Ordena la lista 'numeros' en orden ascendente
print(numeros)

# 10. Longitud de una lista:
# Usamos la función len() para obtener el número de elementos en una lista.
# Pasamos la lista como argumento a len().
longitud_numeros = len(numeros)  # Obtiene la longitud de la lista 'numeros'
print(longitud_numeros)