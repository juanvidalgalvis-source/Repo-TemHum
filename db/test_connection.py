"""
test_connection.py
Prueba básica de conexión desde Python hacia MariaDB.
"""

import mariadb
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

        print("✅ Conexión exitosa a MariaDB.")
        conn.close()
        print("🔒 Conexión cerrada correctamente.")

    except mariadb.Error as e:
        print("❌ Error al conectar a MariaDB:")
        print(e)

if __name__ == "__main__":
    test_connection()
