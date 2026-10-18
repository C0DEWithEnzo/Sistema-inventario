import os
from dotenv import load_dotenv
import mysql.connector

# Carga las variables definidas en el archivo .env
load_dotenv()

def get_connection():
    """Conexión a MySQL usando variables de entorno seguras."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "inventario_user"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "inventario_db"),
    )