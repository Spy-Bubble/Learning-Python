'''
Este script se centra en explicar el parámetro `self` en Python, que es fundamental
para entender cómo los métodos de una clase operan sobre los datos de una instancia específica.
'''

# --- El Parámetro `self`: La Clave de la Instancia ---

class Usuario:
    """
    Una clase para representar a un usuario, demostrando el uso de `self`
    para acceder a los atributos de la instancia.
    """
    def __init__(self, nombre, email):
        """
        Constructor que inicializa los atributos de un nuevo usuario.
        `self` aquí se refiere a la nueva instancia que se está creando.
        """
        # Usamos `self` para adjuntar los datos a la instancia específica.
        self.nombre = nombre
        self.email = email
        self.sesion_iniciada = False

    # 1. `self` como primer parámetro en métodos de instancia
    # Por convención, el primer parámetro de cualquier método de instancia es `self`.
    # Representa la instancia del objeto sobre la cual se llama el método.
    def iniciar_sesion(self):
        """
        Cambia el estado de `sesion_iniciada` de la instancia actual (`self`).
        """
        self.sesion_iniciada = True
        # `self.nombre` accede al atributo `nombre` de *esta* instancia en particular.
        print(f"¡Bienvenido! El usuario '{self.nombre}' ha iniciado sesión.")

    def cerrar_sesion(self):
        """
        Cierra la sesión para la instancia actual (`self`).
        """
        self.sesion_iniciada = False
        print(f"El usuario '{self.nombre}' ha cerrado la sesión.")

    def mostrar_info(self):
        """
        Muestra la información del usuario de la instancia actual (`self`).
        """
        estado_sesion = "Activa" if self.sesion_iniciada else "Inactiva"
        print("--- Información del Usuario ---")
        print(f"  Nombre: {self.nombre}")
        print(f"  Email: {self.email}")
        print(f"  Sesión: {estado_sesion}")

# 2. Creación de múltiples instancias
# Cada instancia es un objeto independiente con sus propios datos.
print("--- Creando instancias de Usuario ---")
usuario_admin = Usuario(nombre="Admin", email="admin@example.com")
usuario_invitado = Usuario(nombre="Invitado", email="guest@example.com")

# 3. ¿Cómo funciona `self` en la práctica?
# Cuando llamas a un método desde una instancia (p. ej., `usuario_admin.iniciar_sesion()`),
# Python automáticamente pasa esa instancia (`usuario_admin`) como el primer argumento `self` al método.

print("\n--- Interactuando con la instancia 'usuario_admin' ---")
usuario_admin.iniciar_sesion()
usuario_admin.mostrar_info()

print("\n--- Interactuando con la instancia 'usuario_invitado' ---")
# `usuario_invitado` tiene su propio estado, independiente de `usuario_admin`.
usuario_invitado.mostrar_info()

# 4. La llamada de método equivalente
# La línea `usuario_admin.iniciar_sesion()` es azúcar sintáctica para:
# `Usuario.iniciar_sesion(usuario_admin)`
# Esto demuestra explícitamente que la instancia se pasa como `self`.
print("\n--- Demostración de llamada explícita ---")
print("Cerrando sesión de 'usuario_admin' usando la sintaxis de clase...")
Usuario.cerrar_sesion(usuario_admin)
usuario_admin.mostrar_info()

# Aunque `self` es una convención, no una palabra clave, es una práctica universal en Python.
# Usar otro nombre (como `this` o `objeto`) funcionaría, pero es fuertemente desaconsejado.

