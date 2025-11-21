"""
db_manager.py
Módulo encargado de manejar la conexión y operaciones con la base de datos MariaDB.

En esta fase solo contiene la estructura base. La lógica será completada
en tareas posteriores.

Gestión de base de datos: inserción y consultas.
"""

import mariadb
import datetime
import config

def get_connection():
    """Crea y retorna una conexión a MariaDB."""
    try:
        conn = mariadb.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT
        )
        return conn
    except mariadb.Error as e:
        print("❌ Error al conectar a MariaDB:", e)
        return None


def insert_record(temperature, humidity):
    """Inserta un registro en la tabla lecturas."""
    conn = get_connection()
    if conn is None:
        print("❌ No se puede insertar: conexión fallida.")
        return False

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO lecturas (temperatura, humedad, fecha_hora)
        VALUES (?, ?, ?)
        """

        current_time = datetime.datetime.now()

        cursor.execute(query, (temperature, humidity, current_time))

        conn.commit()
        print(f"✅ Registro insertado: T={temperature}°C | H={humidity}% | {current_time}")

        return True

    except mariadb.Error as e:
        print("❌ Error al insertar registro:", e)
        return False

    finally:
        conn.close()
        print("🔒 Conexión cerrada.")


if __name__ == "__main__":
    print("Este módulo gestiona la base de datos.")
