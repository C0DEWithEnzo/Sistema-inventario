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
```

---

## 💻 Instalación y Uso

Puedes ejecutar este proyecto de dos formas: usando **Docker Compose** (recomendado) o en **modo local/manual**.

### Opción 1: Con Docker Compose (Recomendado)

Asegúrate de tener instalados **Docker** y **Docker Compose**.

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/C0DEWithEnzo/Sistema-inventario.git
   cd Sistema-inventario
   ```

2. **Crear el archivo de entorno:**
   ```bash
   cp .env.example .env
   ```

3. **Levantar los servicios:**
   ```bash
   docker compose up --build
   ```

4. Abre tu navegador e ingresa a: **`http://localhost:5000`**

---

### Opción 2: Instalación Local (Python + MySQL)

#### Prerrequisitos
- Python 3.10+
- Servidor MySQL activo

1. **Clonar el repositorio y entrar a la carpeta:**
   ```bash
   git clone https://github.com/C0DEWithEnzo/Sistema-inventario.git
   cd Sistema-inventario
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la Base de Datos:**
   Importa el esquema en tu servidor MySQL:
   ```bash
   mysql -u tu_usuario -p < schema.sql
   ```

5. **Configurar el archivo `.env`:**
   Copia la plantilla y configura tus credenciales locales:
   ```bash
   cp .env.example .env
   ```
   Edita `.env`:
   ```env
   DB_HOST=localhost
   DB_USER=inventario_user
   DB_PASSWORD=tu_contraseña
   DB_NAME=inventario_db
   SECRET_KEY=tu_clave_secreta
   ```

6. **Ejecutar la aplicación:**
   ```bash
   python app.py
   ```
   Accede en tu navegador a: **`http://localhost:5000`**

---

## 🧪 Pruebas Automatizadas

El proyecto incluye tests integrados con `pytest`. Para ejecutarlos:

```bash
source venv/bin/activate
pytest
```

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

Desarrollado por [Enzo Elias](https://github.com/C0DEWithEnzo) 🚀