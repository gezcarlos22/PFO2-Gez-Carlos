# PFO 2: Sistema de Gestión de Tareas (API REST + SQLite)

Este proyecto consiste en una **API REST desarrollada en Flask** que gestiona el registro y la autenticación de usuarios con almacenamiento seguro en una base de datos **SQLite**. Las contraseñas se almacenan de manera hasheada para garantizar la seguridad del sistema. Además, incluye una interfaz de línea de comandos (CLI) programada en Python que consume la API usando la librería `requests`.

---

## 📁 Estructura del Proyecto

* **`servidor.py`**: Backend con la API Flask. Maneja las rutas `/registro`, `/login` y `/tareas`.
* **`cliente.py`**: Interfaz de consola que interactúa con la API para realizar las peticiones.
* **`requirements.txt`**: Archivo con las dependencias necesarias.
* **`docs/index.html`**: Documentación estática alojada en GitHub Pages.

---

## 🛠️ Requisitos Previos e Instalación

### Requisitos
* Python 3.x
* Paquetes de Python especificados en `requirements.txt` (`Flask` y `requests`).

### Instalación de dependencias
Abre una terminal en la raíz del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

---

## 🚀 Guía de Uso y Ejecución

Para poner en marcha el sistema, debes utilizar dos terminales diferentes:

1. **Paso 1: Levantar la API**
   En la primera terminal, ejecuta el servidor backend:
   ```bash
   python servidor.py
   ```
   *El servicio estará disponible en `http://localhost:5000`.*

2. **Paso 2: Iniciar la interfaz cliente**
   En una segunda terminal, ejecuta la CLI:
   ```bash
   python cliente.py
   ```
   *Se desplegará un menú interactivo con las opciones para registrarse, iniciar sesión, consultar las tareas y salir.*

---

## 📡 Endpoints de la API

| Método | Ruta | Descripción | Body / Parámetros |
| :--- | :--- | :--- | :--- |
| **POST** | `/registro` | Crea un nuevo usuario en la base de datos | `{"usuario": "...", "contraseña": "..."}` |
| **POST** | `/login` | Valida credenciales e inicia sesión | `{"usuario": "...", "contraseña": "..."}` |
| **GET** | `/tareas` | Retorna un HTML de bienvenida al sistema de tareas | N/A |

---

## 📘 Documentación Web y GitHub Pages

Puedes consultar la documentación conceptual completa (que abarca los motivos para el uso del hashing de claves y las ventajas de SQLite) junto con las capturas de pantalla de las pruebas en:

🌐 **[Documentación en GitHub Pages](https://gezcarlos22.github.io/PFO2-Gez-Carlos/)**

*(También puedes visualizarla localmente abriendo el archivo `docs/index.html` en cualquier navegador).*

> 📌 **Aviso sobre GitHub Pages:** Dado que GitHub Pages únicamente permite alojar contenido estático (HTML/CSS/JS) y no admite entornos de ejecución en segundo plano para servidores como Flask, el sitio `docs/index.html` sirve como repositorio de documentación interactiva. Para probar la API REST funcional, es necesario clonar el repositorio y ejecutar el proyecto localmente siguiendo los pasos anteriores.