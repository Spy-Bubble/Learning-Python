'''
Este script es una introducción al módulo `math` de Python, que proporciona
acceso a funciones y constantes matemáticas definidas por el estándar C.
'''

# --- El Módulo `math` para Principiantes ---

# Para usar las funciones del módulo, primero debemos importarlo.
import math

# 1. Constantes Matemáticas
# El módulo `math` incluye constantes fundamentales.
print("--- 1. Constantes Matemáticas ---")
print(f"Valor de Pi (π): {math.pi}")
print(f"Valor de e (número de Euler): {math.e}")

# 2. Funciones Básicas
print("\n--- 2. Funciones Básicas ---")

# Raíz cuadrada (sqrt)
numero_sqrt = 64
raiz_cuadrada = math.sqrt(numero_sqrt)
print(f"La raíz cuadrada de {numero_sqrt} es: {raiz_cuadrada}")

# Potencia (pow)
base = 2
exponente = 3
potencia = math.pow(base, exponente)
print(f"{base} elevado a la potencia {exponente} es: {potencia}")

# Factorial (factorial)
numero_fact = 5
factorial_resultado = math.factorial(numero_fact)
print(f"El factorial de {numero_fact} es: {factorial_resultado}")

# 3. Funciones de Redondeo
print("\n--- 3. Funciones de Redondeo ---")
numero_decimal = 4.7

# `ceil` (techo): Redondea al entero superior más cercano.
redondeo_techo = math.ceil(numero_decimal)
print(f"El techo ('ceil') de {numero_decimal} es: {redondeo_techo}")

# `floor` (suelo): Redondea al entero inferior más cercano.
redondeo_suelo = math.floor(numero_decimal)
print(f"El suelo ('floor') de {numero_decimal} es: {redondeo_suelo}")

# 4. Funciones Trigonométricas
# Estas funciones operan con radianes.
print("\n--- 4. Funciones Trigonométricas ---")
angulo_grados = 90

# `radians`: Convierte grados a radianes.
angulo_radianes = math.radians(angulo_grados)
print(f"{angulo_grados} grados equivalen a {angulo_radianes:.4f} radianes.")

# `sin`: Calcula el seno del ángulo en radianes.
seno = math.sin(angulo_radianes)
print(f"El seno de {angulo_grados} grados es: {seno}")

# `cos`: Calcula el coseno del ángulo en radianes.
coseno = math.cos(math.radians(180))
print(f"El coseno de 180 grados es: {coseno}")

