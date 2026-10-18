# 📦 Sistema de Inventario

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?style=for-the-badge&logo=flask&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

Una aplicación web **Full-Stack** diseñada para gestionar el inventario de un pequeño negocio o emprendimiento de manera sencilla y eficiente.

## ✨ Características Principales

*   **Operaciones CRUD completas:** Crear, Leer, Actualizar y Eliminar productos.
*   **Dashboard intuitivo:** Visualización clara de los productos con estadísticas rápidas (total de productos, valor total, stock bajo).
*   **Gestión de Stock:** Alertas visuales (badges) cuando un producto tiene menos de 5 unidades.
*   **Diseño Responsive:** Interfaz adaptable a dispositivos móviles y escritorio.
*   **Arquitectura MVC:** Separación clara entre la lógica de negocio (`app.py`), la base de datos (`db.py`) y la vista (templates HTML).

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3, Flask
*   **Base de Datos:** MySQL
*   **Frontend:** HTML5, CSS3 (CSS puro, sin frameworks, con diseño moderno)
*   **Entorno de Desarrollo:** Linux (Bazzite) + Distrobox
*   **Control de Versiones:** Git y GitHub

## 🚀 Instalación y Ejecución Local
  
   Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1. Clonar el repositorio

   git clone https://github.com/C0DEWithEnzo/Sistema-inventario.git
   cd Sistema-inventario

2. Configurar el entorno virtual

   * Crear el entorno virtual
   python3 -m venv venv

   * Activarlo
     En Linux/Mac:
   source venv/bin/activate
     En Windows:
   venv\Scripts\activate

3. Instalar dependencias

   pip install Flask mysql-connector-python

4. Configurar la Base de Datos (MySQL)

   Abre tu cliente de MySQL (o la terminal) y ejecuta:

   CREATE DATABASE inventario_db;
    USE inventario_db;

    CREATE TABLE productos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        precio DECIMAL(10, 2) NOT NULL,
        cantidad INT NOT NULL DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Crear un usuario para la app (Recomendado)
    CREATE USER 'inventario_user'@'localhost' IDENTIFIED BY 'TuContraseñaSegura123';
    GRANT ALL PRIVILEGES ON inventario_db.* TO 'inventario_user'@'localhost';
    FLUSH PRIVILEGES;

5. Configurar las credenciales

    Abre el archivo db.py y actualiza las credenciales con los datos que creaste:

    import mysql.connector

    def get_connection():
      return mysql.connector.connect(
          host="localhost",
          user="inventario_user",
          password="TuContraseñaSegura123", # <-- CAMBIAR AQUÍ
          database="inventario_db"
      )

6. Ejecutar la aplicación

   python app.py

## 📂 Estructura del Proyecto

```text
Sistema-Inventario/
│
├── app.py               # Rutas y lógica principal de Flask
├── db.py                # Módulo de conexión a la base de datos MySQL
├── requirements.txt     # Dependencias del proyecto (Flask, mysql-connector)
├── .gitignore           # Archivos ignorados por Git (venv, __pycache__, etc.)
├── README.md            # Documentación del proyecto
│
├── templates/           # Vistas HTML (Jinja2)
│   ├── index.html       # Página principal (lista de productos)
│   ├── agregar.html     # Formulario para crear producto
│   └── editar.html      # Formulario para editar producto
│
└── static/              # Archivos estáticos
    └── style.css        # Hoja de estilos principal
