# 1. Operador suma (+)
resultado_suma = 5 + 3  # resultado_suma es 8  
print("Suma:", resultado_suma)

# 2. Operador resta (-)
resultado_resta = 5 - 3  # resultado_resta es 2
print("Resta:", resultado_resta)

# 3. Operador multiplicación (*)
resultado_multiplicacion = 5 * 3  # resultado_multiplicacion es 15
print("Multiplicación:", resultado_multiplicacion)

# 4. Operador división (/)
resultado_division = 5 / 2  # resultado_division es 2.5 (float)
print("División:", resultado_division)  

# 5. Operador división entera (//)
# Devuelve el cociente sin la parte decimal
resultado_division_entera = 5 // 2  # resultado_division_entera es 2 (int)
print("División entera:", resultado_division_entera)   

# 6. Operador módulo (%)
# Devuelve el resto de la división
resultado_modulo = 5 % 2  # resultado_modulo es 1
print("Módulo:", resultado_modulo)

# 7. Operador potencia (**)
resultado_potencia = 5 ** 2  # resultado_potencia es 25
print("Potencia:", resultado_potencia)

# 8. Operaciones con variables:
a = 10
b = 3  
suma = a + b               # suma es 13
resta = a - b              # resta es 7
multiplicacion = a * b     # multiplicacion es 30
division = a / b           # division es 3.3333...
division_entera = a // b   # division_entera es 3
modulo = a % b             # modulo es 1
potencia = a ** b          # potencia es 1000
print("Operaciones con variables:")
print("Suma:", suma)
print("Resta:", resta)
print("Multiplicación:", multiplicacion)
print("División:", division)
print("División entera:", division_entera)
print("Módulo:", modulo)
print("Potencia:", potencia)

# 9. Operaciones multiples y mixtas 
# Se ejecutan segun la jerrarquía de operaciones matemáticas
resultado_mixto = 5 + 3 * 2 - 4 / 2 + 2 ** 3
# resultado_mixto es 5 + 6 - 2 + 8 = 17.0
print("Operaciones mixtas:", resultado_mixto)   

# 10. Operaciones multiples y mixtas con paréntesis
# Los paréntesis alteran la jerarquía de operaciones
resultado_parentesis = (5 + 3) * (2 - 4) / (2 + 2) ** 3
# resultado_parentesis es 8 * -2 / 4 ** 3 = -16 / 64 = -0.25
print("Operaciones mixtas con paréntesis:", resultado_parentesis)

# 11. Raíz cuadrada usando potencia
x = 16
# Usando la ley de los exponentes: x^(m/n) = n√(x^m)
raiz_cuadrada = x ** 0.5 # raíz cuadrada de x es 4.0, porque 16^(1/2) = 4
print("Raíz cuadrada de", x, "es:", raiz_cuadrada)

# 12. Uso de guiones bajos en números grandes
# Mejora la legibilidad de números grandes y no afecta su valor
numero_grande = 1_000_000_000  # Más legible que 1000000000
print("Número grande:", numero_grande)  

# 13. Uso de guiones bajos para decimales
decimal_grande = 3_141_592.653_589  # Más legible que 3141592.653589
print("Decimal grande:", decimal_grande)

# 14. Uso de guiones bajos en literales binarios, octales y hexadecimales
binario = 0b1010_1011_1100  # Más legible que 0b101010111100
octal = 0o12_34_56  # Más legible que 0o123456
hexadecimal = 0xAB_CD_EF  # Más legible que 0xABCDEF
print("Binario:", binario)           # Imprime 2748 
print("Octal:", octal)               # Imprime 42798
print("Hexadecimal:", hexadecimal)   # Imprime 11259375