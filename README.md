# 📦 Sistema de Gestión de Inventario

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=flat&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Un sistema de gestión de inventarios web moderno, dinámico y responsivo construido con **Python (Flask)** y **MySQL**. Diseñado bajo estándares de interfaz limpia tipo dashboard enterprise, cuenta con métricas en tiempo real, categorización de productos, ordenamiento, filtrado, paginación, exportación de datos y soporte completo para contenedorización con Docker.

---

## 🚀 Características Principales

- **Dashboard e Indicadores KPI**: Métricas globales calculadas dinámicamente en BD (valor total de inventario, total de productos, unidades en stock, productos agotados y alertas de stock bajo).
- **Gestión de Productos (CRUD completo)**: Alta, lectura, edición y eliminación segura con modales de confirmación.
- **Categorización y Estado**: Asignación de categorías a productos y badges de estado automático (*Disponible*, *Stock Bajo*, *Agotado*).
- **Filtros Avanzados y Paginación**: Búsqueda en tiempo real por texto, filtrado por chips de estado, selección por categorías y ordenamiento dinámico multi-columna.
- **Vista Previa Interactiva**: Al crear o editar un producto, un panel lateral actualiza en vivo el valor total y el badge del artículo antes de guardar.
- **Exportación de Datos**: Generación y descarga de inventario completo en formato **CSV**.
- **Seguridad**: Configuración de credenciales mediante variables de entorno (`.env`), evitando exposición de datos sensibles.

---

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.11, Flask, MySQL Connector.
- **Base de Datos**: MySQL 8.0.
- **Frontend**: HTML5, CSS3 (Custom Properties & Flexbox/Grid), JavaScript Vanilla, Lucide Icons.
- **DevOps & Entorno**: Docker, Docker Compose, `python-dotenv`.

---

## 📁 Estructura del Proyecto

```text
Sistema-Inventario/
├── .env.example          # Plantilla de variables de entorno
├── .gitignore            # Exclusión de archivos sensibles e hiper-temporales
├── Dockerfile            # Configuración del contenedor de la app Flask
├── docker-compose.yml    # Orquestación de servicios (Flask + MySQL)
├── requirements.txt      # Dependencias de Python
├── schema.sql            # Estructura e inserción inicial de la BD
├── app.py                # Controlador principal y rutas de Flask
├── db.py                 # Conexión a la base de datos MySQL
├── test_app.py           # Pruebas unitarias/integración
├── static/
│   └── style.css         # Hoja de estilos del Dashboard Enterprise
└── templates/
    ├── _form.html        # Formulario compartido con preview en vivo
    ├── agregar.html      # Vista para nuevo producto
    ├── base.html         # Plantilla base y layout global
    ├── editar.html       # Vista para edición de producto
    ├── error.html        # Manejo personalizado de errores HTTP/BD
    └── index.html        # Listado principal y métricas KPI
