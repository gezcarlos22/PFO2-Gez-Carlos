
"""Cliente de terminal para interactuar con la API de usuarios y tareas."""

import requests

SERVIDOR = "http://localhost:5000"


def enviar_solicitud(ruta, nombre, clave):
    """Envía las credenciales al endpoint indicado."""
    return requests.post(
        f"{SERVIDOR}/{ruta}",
        json={
            "usuario": nombre,
            "contraseña": clave
        }
    )


def registrar_usuario():
    """Solicita los datos necesarios para crear una cuenta."""
    nombre = input("Nuevo usuario: ").strip()
    clave = input("Contraseña: ").strip()

    try:
        respuesta = enviar_solicitud("registro", nombre, clave)
        print(respuesta.json().get("message"))
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")


def autenticar_usuario():
    """Inicia sesión y devuelve si la autenticación ha sido correcta."""
    nombre = input("Usuario: ").strip()
    clave = input("Contraseña: ").strip()

    try:
        respuesta = enviar_solicitud("login", nombre, clave)
        resultado = respuesta.json()

        print(resultado.get("message"))
        return resultado.get("status") == "success"

    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")
        return False


def consultar_tareas():
    """Solicita y muestra el contenido del endpoint de tareas."""
    try:
        respuesta = requests.get(f"{SERVIDOR}/tareas")

        print("\n--- Respuesta del servidor (/tareas) ---")
        print(respuesta.text.strip())
        print("-----------------------------------------\n")

    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor. ¿Está en ejecución?")


def ejecutar_menu():
    """Presenta el menú principal y gestiona las opciones del usuario."""
    autenticado = False

    while True:
        print("\n" + "=" * 45)
        print("       SISTEMA DE GESTIÓN DE TAREAS")
        print("=" * 45)
        print("  1. Crear una nueva cuenta")
        print("  2. Acceder a mi cuenta")
        print("  3. Consultar el sistema de tareas")
        print("  4. Cerrar el programa")
        print("-" * 45)

        opcion = input("Seleccione una opción del menú: ").strip()

        if opcion == "1":
            print("\n--- REGISTRO DE NUEVO USUARIO ---")
            registrar_usuario()

        elif opcion == "2":
            print("\n--- ACCESO A LA PLATAFORMA ---")
            autenticado = autenticar_usuario()

        elif opcion == "3":
            if autenticado:
                print("\n--- PANEL DE GESTIÓN DE TAREAS ---")
                consultar_tareas()
            else:
                print("\n[AVISO] Acceso restringido.")
                print("Para consultar las tareas, primero debe iniciar sesión.")

        elif opcion == "4":
            print("\nGracias por utilizar el Sistema de Gestión de Tareas.")
            print("Finalizando la aplicación...")
            break

        else:
            print("\n[ERROR] La opción introducida no es válida.")
            print("Por favor, seleccione una opción entre 1 y 4.")


if __name__ == "__main__":
    ejecutar_menu()