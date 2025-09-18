'''
Este script es un tutorial completo sobre cómo trabajar con fechas y horas en Python
utilizando el módulo `datetime`, uno de los más importantes de la biblioteca estándar.
'''

# --- Guía del Módulo `datetime` para Trabajar con Fechas y Horas ---

# El módulo `datetime` proporciona clases para manipular fechas y horas.
# Primero, debemos importarlo.
import datetime

# 1. La clase `datetime.time`: para trabajar solo con horas
print("--- 1. La clase `datetime.time` ---")

# Creación de un objeto `time` con valores específicos: hora, minuto, segundo, microsegundo.
hora_especifica = datetime.time(14, 30, 55, 123456)

print(f"Objeto time creado: {hora_especifica}")
print(f"  - Hora: {hora_especifica.hour}")
print(f"  - Minuto: {hora_especifica.minute}")
print(f"  - Segundo: {hora_especifica.second}")
print(f"  - Microsegundo: {hora_especifica.microsecond}")

# 2. La clase `datetime.date`: para trabajar solo con fechas
print("\n--- 2. La clase `datetime.date` ---")

# Creación de un objeto `date` con valores específicos: año, mes, día.
fecha_especifica = datetime.date(2025, 12, 31)

print(f"Objeto date creado: {fecha_especifica}")
print(f"  - Año: {fecha_especifica.year}")
print(f"  - Mes: {fecha_especifica.month}")
print(f"  - Día: {fecha_especifica.day}")

# `date.today()` devuelve la fecha local actual.
fecha_actual = datetime.date.today()
print(f"La fecha de hoy es: {fecha_actual}")

# 3. La clase `datetime.datetime`: para trabajar con fecha y hora combinadas
print("\n--- 3. La clase `datetime.datetime` ---")

# `datetime.now()` devuelve la fecha y hora local actuales.
fecha_y_hora_actual = datetime.datetime.now()

print(f"Fecha y hora actuales: {fecha_y_hora_actual}")
print(f"  - Componente de fecha: {fecha_y_hora_actual.date()}")
print(f"  - Componente de hora: {fecha_y_hora_actual.time()}")

# 4. Formateo de fechas y horas con `strftime()`
# El método `strftime()` convierte un objeto `datetime` en una cadena de texto
# con un formato específico, usando códigos de formato.
print("\n--- 4. Formateo de fechas con `strftime()` ---")

# %Y: Año con 4 dígitos
# %m: Mes como número (01-12)
# %d: Día del mes como número (01-31)
# %H: Hora (00-23)
# %M: Minuto (00-59)
# %S: Segundo (00-59)
formato_simple = fecha_y_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
print(f"Formato simple (YYYY-MM-DD HH:MM:SS): {formato_simple}")

# %A: Día de la semana completo (ej. Tuesday)
# %B: Mes completo (ej. February)
# %d: Día del mes
formato_legible = fecha_y_hora_actual.strftime("Hoy es %A, %d de %B de %Y")
print(f"Formato más legible (en inglés por defecto): {formato_legible}")

# 5. Formateo en otros idiomas con el módulo `locale`
# Para mostrar nombres de días y meses en otros idiomas, podemos usar el módulo `locale`.
print("\n--- 5. Usando `locale` para formateo en español ---")

import locale

# Establecemos la configuración regional a español.
# La cadena puede variar según el sistema operativo ('es', 'es_ES', 'es_ES.UTF-8').
try:
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
    fecha_formateada_es = fecha_y_hora_actual.strftime("%A, %d de %B de %Y a las %H:%M").capitalize()
    print(f"Fecha formateada en español: {fecha_formateada_es}")
except locale.Error:
    print("No se pudo establecer la configuración regional en español. Se mostrará en el idioma por defecto.")

