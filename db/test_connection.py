"""
test_connection.py
Prueba básica de conexión desde Python hacia MariaDB.
"""

import mariadb
import sys
import os

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def test_connection():
    try:
        print("Intentando conectar a MariaDB...")

        conn = mariadb.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT
        )

        print("Conexion exitosa a MariaDB.")
        conn.close()
        print("Conexión cerrada correctamente.")

    except mariadb.Error as e:
        print("Error al conectar a MariaDB:")
        print(e)

if __name__ == "__main__":
    test_connection()
