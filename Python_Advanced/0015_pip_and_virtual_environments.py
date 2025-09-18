
'"""
Este archivo no es un script ejecutable, sino una guía en formato de script de Python
que explica cómo usar PIP (el gestor de paquetes de Python) y cómo configurar
entornos virtuales para gestionar las dependencias de los proyectos de forma aislada.

Los comandos mostrados aquí deben ser ejecutados en la terminal o línea de comandos,
no en un intérprete de Python.
"""'

# --- Guía de PIP y Entornos Virtuales en Python ---

# 1. PIP: El Gestor de Paquetes de Python
# PIP (Pip Installs Packages) es la herramienta estándar para instalar y gestionar
# paquetes de software escritos en Python. Estos paquetes se encuentran en el
# Python Package Index (PyPI).

print("--- 1. Comandos básicos de PIP ---")

# Comprobar la versión de PIP
# Es una buena práctica asegurarse de que PIP esté instalado y actualizado.
# Comando: pip --version
# Comando para actualizar PIP: python -m pip install --upgrade pip

# Instalar un paquete
# El comando `install` descarga e instala un paquete desde PyPI.
# Sintaxis: pip install <nombre_del_paquete>
# Ejemplo: pip install numpy

# Listar paquetes instalados
# El comando `freeze` muestra todos los paquetes instalados en el entorno actual
# junto con sus versiones, en un formato que puede ser guardado en un archivo.
# Comando: pip freeze
# Ejemplo de salida: numpy==1.26.4

# Guardar dependencias en un archivo requirements.txt
# Es una práctica estándar guardar las dependencias de un proyecto en este archivo.
# Comando: pip freeze > requirements.txt

# Instalar paquetes desde un archivo requirements.txt
# Esto permite a otros desarrolladores instalar fácilmente todas las dependencias del proyecto.
# Comando: pip install -r requirements.txt

# Desinstalar un paquete
# Elimina un paquete del entorno actual.
# Sintaxis: pip uninstall <nombre_del_paquete>
# Ejemplo: pip uninstall numpy

# 2. Entornos Virtuales: `venv`
# Un entorno virtual es un directorio que contiene una instalación de Python de una
# versión particular, además de varios paquetes adicionales.
# Permite aislar las dependencias de diferentes proyectos.

print("\n--- 2. Gestión de Entornos Virtuales con `venv` ---")

# Crear un entorno virtual
# `venv` es el módulo estándar para crear entornos virtuales en Python 3.
# Sintaxis: python -m venv <nombre_del_entorno>
# Ejemplo: python -m venv mi_entorno_virtual
# Esto creará un directorio llamado `mi_entorno_virtual`.

# Activar un entorno virtual
# Para usar un entorno virtual, primero debes activarlo.

# En Windows:
# Comando: .\<nombre_del_entorno>\Scripts\activate
# Ejemplo: .\mi_entorno_virtual\Scripts\activate

# En macOS y Linux:
# Comando: source <nombre_del_entorno>/bin/activate
# Ejemplo: source mi_entorno_virtual/bin/activate

# Una vez activado, el prompt de la terminal cambiará para mostrar el nombre del entorno,
# indicando que cualquier paquete que instales con `pip` se instalará dentro de este entorno.

# Desactivar un entorno virtual
# Para volver al entorno global de Python, simplemente ejecuta el comando `deactivate`.
# Comando: deactivate

# Flujo de trabajo típico:
# 1. Crea un nuevo directorio para tu proyecto.
# 2. Dentro de ese directorio, crea un entorno virtual: `python -m venv venv`
# 3. Activa el entorno virtual: `source venv/bin/activate` (o el equivalente en Windows)
# 4. Instala las dependencias: `pip install numpy pandas`
# 5. Escribe tu código.
# 6. Guarda las dependencias: `pip freeze > requirements.txt`
# 7. Cuando termines, desactiva el entorno: `deactivate`

print("\nEsta guía cubre los fundamentos de `pip` y `venv`. ¡Son herramientas esenciales para cualquier desarrollador de Python!")

