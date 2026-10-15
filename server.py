
"""API para gestionar usuarios y validar el acceso al sistema de tareas."""

import sqlite3
import sys

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

NOMBRE_BD = "usuarios.db"

app = Flask(__name__)


def conectar_bd():
    """Abre una conexión con la base de datos."""
    return sqlite3.connect(NOMBRE_BD)


def inicializar_bd():
    """Prepara la tabla de usuarios si todavía no existe."""
    try:
        with conectar_bd() as conexion:
            conexion.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    contrasena_hash TEXT NOT NULL
                )
            """)
    except sqlite3.Error as error:
        print(f"[ERROR] Error al inicializar la base de datos: {error}")
        sys.exit(1)


def buscar_usuario(nombre):
    """Obtiene los datos de un usuario a partir de su nombre."""
    conexion = conectar_bd()
    conexion.row_factory = sqlite3.Row

    try:
        return conexion.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (nombre,)
        ).fetchone()
    finally:
        conexion.close()


def guardar_usuario(nombre, clave_hash):
    """Almacena un nuevo usuario junto con su contraseña cifrada mediante hash."""
    with conectar_bd() as conexion:
        conexion.execute(
            """
            INSERT INTO usuarios (usuario, contrasena_hash)
            VALUES (?, ?)
            """,
            (nombre, clave_hash)
        )


def obtener_datos():
    """Lee los datos enviados en formato JSON."""
    datos = request.get_json(silent=True)

    if not datos:
        return None, (
            jsonify({
                "status": "error",
                "message": "Se esperaba un JSON"
            }),
            400
        )

    nombre = datos.get("usuario")
    clave = datos.get("contraseña") or datos.get("contrasena")

    if not nombre or not clave:
        return None, (
            jsonify({
                "status": "error",
                "message": "Faltan campos: usuario y contraseña"
            }),
            400
        )

    return (nombre, clave), None


@app.route("/registro", methods=["POST"])
def registro():
    """Crea una cuenta nueva si el nombre de usuario está disponible."""
    datos, error = obtener_datos()

    if error:
        return error

    nombre, clave = datos

    if buscar_usuario(nombre):
        return jsonify({
            "status": "error",
            "message": "El usuario ya existe"
        }), 409

    clave_hash = generate_password_hash(clave)

    try:
        guardar_usuario(nombre, clave_hash)
    except sqlite3.Error as error_bd:
        return jsonify({
            "status": "error",
            "message": f"No se pudo guardar el usuario: {error_bd}"
        }), 500

    return jsonify({
        "status": "success",
        "message": f"Usuario '{nombre}' registrado correctamente"
    }), 201


@app.route("/login", methods=["POST"])
def login():
    """Comprueba las credenciales del usuario."""
    datos, error = obtener_datos()

    if error:
        return error

    nombre, clave = datos
    usuario = buscar_usuario(nombre)

    if usuario is None or not check_password_hash(
        usuario["contrasena_hash"], clave
    ):
        return jsonify({
            "status": "error",
            "message": "Usuario o contraseña incorrectos"
        }), 401

    return jsonify({
        "status": "success",
        "message": f"Bienvenido/a {nombre}. Ya podés acceder a /tareas"
    })


@app.route("/tareas", methods=["GET"])
def mostrar_tareas():
    """Presenta la página HTML de bienvenida."""
    pagina = """
    <html>
        <head>
            <title>Gestión de Tareas</title>
        </head>
        <body style="font-family: Arial, sans-serif;
                     text-align: center;
                     margin-top: 60px;">
            <h1>Bienvenido/a al Sistema de Gestión de Tareas</h1>
            <p>Iniciá sesión en /login para gestionar tus tareas.</p>
        </body>
    </html>
    """
    return pagina


@app.errorhandler(404)
def ruta_inexistente(error):
    """Devuelve un mensaje JSON cuando la ruta solicitada no existe."""
    return jsonify({
        "status": "error",
        "message": "Endpoint no encontrado"
    }), 404


if __name__ == "__main__":
    inicializar_bd()
    app.run(host="localhost", port=5000, debug=True)
