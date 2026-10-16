import os

import mysql.connector


def get_connection():
    """Conexión a MySQL. Los valores pueden sobrescribirse con variables de entorno."""
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "inventario_user"),
        password=os.environ.get("DB_PASSWORD", "proyectfs08!"),
        database=os.environ.get("DB_NAME", "inventario_db"),
    )
