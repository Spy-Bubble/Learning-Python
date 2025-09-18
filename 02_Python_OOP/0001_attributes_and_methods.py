"""
Este script explica cómo definir y utilizar atributos (datos) y métodos (comportamientos)
en las clases de Python. Los atributos almacenan el estado de un objeto, mientras que
los métodos definen las acciones que un objeto puede realizar.
"""

# --- Atributos y Métodos en las Clases ---

# 1. Definición de una Clase con Atributos y Métodos
class Personaje:
    """
    Esta clase representa un personaje de un juego, con sus estadísticas y acciones.
    """
    # Atributos de clase: Son variables que pertenecen a la clase y son compartidas
    # por todas las instancias (objetos) que se creen de esta clase.
    puntos_de_vida = 100
    resistencia = 50
    experiencia = 0

    # Métodos: Son funciones definidas dentro de una clase. El primer parámetro
    # siempre es `self`, que representa la instancia del objeto.
    def esta_vivo(self):
        """Comprueba si el personaje todavía tiene puntos de vida."""
        return self.puntos_de_vida > 0

    def mostrar_game_over(self):
        """Imprime un mensaje de fin de juego."""
        print("GAME OVER: El personaje ha sido derrotado.")

# 2. Creación de un Objeto y Acceso a sus Atributos
print("--- Creando un personaje y accediendo a sus atributos ---")

# Creamos una instancia de la clase Personaje
jugador_1 = Personaje()

# Accedemos a los atributos del objeto usando la notación de punto (objeto.atributo)
print(f"Puntos de vida iniciales del jugador: {jugador_1.puntos_de_vida}")

# 3. Modificación de los Atributos de un Objeto
print("\n--- Modificando los atributos del objeto ---")

print("El jugador recibe un ataque que reduce su vida a 0.")
# Podemos cambiar el valor de los atributos de una instancia específica.
# Este cambio solo afecta a `jugador_1`.
jugador_1.puntos_de_vida = 0

print(f"Puntos de vida actuales del jugador: {jugador_1.puntos_de_vida}")

# 4. Llamada a los Métodos de un Objeto
print("\n--- Llamando a los métodos del objeto ---")

# Usamos los métodos para realizar acciones o comprobaciones sobre el objeto.
# Comprobamos si el jugador sigue vivo después del ataque.
if not jugador_1.esta_vivo():
    print("El personaje ya no tiene puntos de vida.")
    # Llamamos a otro método basado en el estado del objeto.
    jugador_1.mostrar_game_over()