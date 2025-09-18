'''
Este script ofrece una guía sobre el encapsulamiento en Python, uno de los pilares
de la Programación Orientada a Objetos. Se explica cómo controlar el acceso a los
atributos y métodos de una clase usando modificadores de acceso.
'''

# --- Guía de Encapsulamiento en Python ---

class CuentaBancaria:
    """
    Clase que simula una cuenta bancaria para demostrar los conceptos de encapsulamiento.
    """
    def __init__(self, titular, saldo_inicial):
        # 1. Atributo Público: `titular`
        # Accesible desde cualquier lugar, tanto dentro como fuera de la clase.
        self.titular = titular

        # 2. Atributo Protegido: `_tipo_cuenta`
        # Convención que indica que no debe ser modificado directamente desde fuera de la clase.
        # Sin embargo, Python no impide el acceso.
        self._tipo_cuenta = "Ahorros"

        # 3. Atributo Privado: `__saldo`
        # Su acceso está restringido y no se puede acceder directamente desde fuera de la clase.
        # Python cambia su nombre internamente (name mangling) para evitar colisiones.
        self.__saldo = saldo_inicial

    # 4. Métodos Públicos (Getters y Setters)
    # Son la interfaz pública para interactuar con los atributos privados.

    def get_saldo(self):
        """
        Método Getter: Proporciona acceso de solo lectura al saldo privado.
        """
        print("Accediendo al saldo a través del método getter.")
        return self.__saldo

    def set_saldo(self, nuevo_saldo):
        """
        Método Setter: Permite modificar el saldo privado, a menudo con validaciones.
        """
        print("Modificando el saldo a través del método setter.")
        if nuevo_saldo >= 0:
            self.__saldo = nuevo_saldo
        else:
            print("Error: El saldo no puede ser negativo.")
            self.__negar_acceso()

    # 5. Método Privado
    # Destinado a ser usado solo por otros métodos dentro de la misma clase.
    def __negar_acceso(self):
        """
        Método privado que realiza una acción interna, no accesible desde el exterior.
        """
        print("Acción interna: Registrando intento de acceso no válido.")

# --- Demostración de Uso ---

print("--- Creando una instancia de CuentaBancaria ---")
mi_cuenta = CuentaBancaria("Juan Pérez", 1000.0)

# Acceso a atributo público (Permitido)
print(f"Titular de la cuenta: {mi_cuenta.titular}")
mi_cuenta.titular = "Juan Carlos Pérez"
print(f"Titular modificado: {mi_cuenta.titular}")

# Acceso a atributo protegido (Técnicamente posible, pero no recomendado)
print(f"\nTipo de cuenta (protegido): {mi_cuenta._tipo_cuenta}")

# Intento de acceso a atributo privado (Generará un AttributeError)
print("\nIntentando acceder directamente al saldo privado...")
try:
    print(mi_cuenta.__saldo)
except AttributeError as e:
    print(f"Error: {e}")

# Acceso correcto a través de métodos públicos (Getters y Setters)
print("\n--- Interactuando con el saldo de forma controlada ---")
saldo_actual = mi_cuenta.get_saldo()
print(f"Saldo actual obtenido con get_saldo(): ${saldo_actual}")

print("\nEstableciendo un nuevo saldo válido...")
mi_cuenta.set_saldo(1500.0)
print(f"Nuevo saldo: ${mi_cuenta.get_saldo()}")

print("\nIntentando establecer un saldo no válido...")
mi_cuenta.set_saldo(-200.0)
print(f"Saldo después del intento fallido: ${mi_cuenta.get_saldo()}")

# Name Mangling: Así es como Python realmente nombra al atributo privado
# Esto no debe usarse en código de producción.
print(f"\nAcceso al saldo privado usando 'name mangling': ${mi_cuenta._CuentaBancaria__saldo}")

