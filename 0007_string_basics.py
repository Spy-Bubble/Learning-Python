# Strings (Cadenas de texto) en Python

# 1. Las cadenas de texto son secuencias de caracteres encerradas entre comillas simples (' ') o dobles (" ").
# La concatenación de cadenas se puede hacer usando el operador (+) o las comas (,) en la función print().
fragmento1 = "Hola"
fragmento2 = " Mundo"    
# Concatenación con (+)
saludo1 = fragmento1 +  fragmento2
print(saludo1)
# Concatenación con (,)
saludo2 = fragmento1, fragmento2
print(saludo2)

# 2. Tipos de comillas en strings
# Puedes usar comillas simples o dobles para definir cadenas.
cadena1 = 'Hola con comillas simples'
cadena2 = "Hola con comillas dobles"
print(cadena1)
print(cadena2)
# Si necesitas incluir comillas dentro de la cadena, usa el otro tipo de comillas o el carácter de escape (\).
cadena3 = 'Ella dijo: "Hola, Es un placer conocerte."'
cadena4 = "Ella dijo: \"Hola, Es un placer conocerte.\""
print(cadena3)
print(cadena4)

# 3. f-strings (Cadenas formateadas)
# Las f-strings son cadenas de texto que permiten incrustar expresiones dentro de llaves {}.
# La letra f se puede escribir de forma mayúscula o minúscula, con comillas simples o dobles.
# f"" o F"" o f'' o F''
color = input("¿Cuál es tu color favorito?\n")
print(f"El {color} también es mi color favorito!")
# Tambien puedes realizar operaciones dentro de las llaves.
a = 5
b = 10
print(F"La suma de {a} y {b} es {a + b}.")

# 4. Métodos comunes de los strings
# Estos metodos permiten manipular y transformar cadenas de texto de forma sencilla.
# Para llamar un método, se escribe el nombre de la cadena seguido de un punto (.) y el nombre del método.
# Ejemplo: objeto.nombre_metodo()

# Algunos métodos comunes son:

# metodo.capitalize(): Convierte el primer carácter de la cadena a mayúscula.
cadena5 = "méxico"
print(cadena5.capitalize())

# metodo.upper(): Convierte todos los caracteres de la cadena a mayúsculas.
print(cadena5.upper())

# metodo.lower(): Convierte todos los caracteres de la cadena a minúsculas.
cadena7 = "La ImagInaCIón NO tiene LíMites."
print(cadena7.lower())

# metodo.title(): Convierte el primer carácter de cada palabra a mayúscula.
print(cadena7.title())

# metodo.strip(): Elimina los espacios en blanco al inicio y al final de la cadena.
cadena8 = "   Espacios en blanco   "
print(f"'{cadena8.strip()}'")

# metodo.replace(): Reemplaza todas las apariciones de una subcadena por otra.
cadena9 = "Me gusta programar en Java."
print(cadena9.replace("Java", "Python"))