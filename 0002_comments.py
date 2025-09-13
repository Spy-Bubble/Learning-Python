# Comments that contradict the code are worse than no comments. 
# Los comentarios que contradicen al código son peores que no tener comentarios.

# Always make a priority of keeping the comments up-to-date when the code changes!
# ¡Siempre da prioridad a mantener los comentarios actualizados cuando el código cambie!

# Comentarios en Python
# Para comentar algo en Python, se usa el símbolo numeral (#)

# 1. Comentario de una sola línea
# Este es un comentario de una sola línea
print("Hola, mundo!")

# 2. Desactivar partes del código
# print("Este código está comentado y no se ejecutará")

# 3. División de líneas largas
def funcion_larga():
    # Primera sección
    # Esta sección hace esto
    # . . . código de la primera sección
    # Segunda sección
    # Esta sección hace esto otro
    # . . . código de la segunda sección
    # Tercera sección
    # Esta sección hace otra cosa más
    # . . . código de la tercera sección
    pass # Placeholder para el cuerpo de la función (no hace nada)

# 4. Comentarios a la derecha del código
x = 10  # No anula el código

# Los comentarios de 1 linea intentan describir el bloque de código que sigue
# Los comentarios a la derecha del código intentan explicar una línea específica

# 5. Comentarios de múltiples líneas
"""
Este es un comentario de múltiples líneas.
Se usa para describir bloques de código más grandes.
También se puede usar para documentación.
"""

# Se puede usar comillas simples
'''
Este es otro comentario de múltiples líneas.
También se usa para describir bloques de código más grandes.
También se puede usar para documentación.
'''

# 6. Convenciones para escribir buenas cadenas de documentación "docstrings" 
class MiClase:
    # Para dosctrings de una sola línea, mantener las """ al mismo nivel
    """Esta es una clase de ejemplo."""
  
    def metodo(self):
        # Para docstrings de múltiples líneas, las """ que cierran deben estar alineadas consigo mismas
        """Este es un método de ejemplo.
        Hace algo interesante.
        """
        pass

# Escribir docstrings para todo modulo, función, clase y método público  