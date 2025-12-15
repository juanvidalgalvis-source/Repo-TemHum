"""
db_manager.py
Módulo encargado de manejar la conexión y operaciones con la base de datos MariaDB.

Gestión de base de datos: inserción y consultas con conexión persistente.
"""

import MySQLdb as mariadb
import datetime
import config

# ===========================================
# CONEXIÓN PERSISTENTE A MARIADB (HU21.1)
# ===========================================
_db_connection = None

def get_persistent_connection():
    """Retorna la conexión persistente, reconectando si es necesario."""
    global _db_connection

    # Verificar si la conexión existe y está activa
    if _db_connection is not None:
        try:
            # Ping para verificar si la conexión sigue viva
            _db_connection.ping()
            return _db_connection
        except mariadb.Error:
            config.logger.warning("BD WARNING: Conexión perdida, intentando reconectar...")
            _db_connection = None

    # Crear nueva conexión
    try:
        _db_connection = mariadb.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            db=config.DB_NAME,
            port=config.DB_PORT
        )
        config.logger.info("BD INFO: Conexión persistente establecida")
        return _db_connection
    except mariadb.Error as e:
        config.error_logger.error("BD ERROR: Error al conectar a MariaDB - {}".format(e))
        return None

def close_persistent_connection():
    """Cierra la conexión persistente."""
    global _db_connection
    if _db_connection is not None:
        try:
            _db_connection.close()
            config.logger.info("BD INFO: Conexión persistente cerrada")
        except mariadb.Error as e:
            config.error_logger.error("BD ERROR: Error al cerrar conexión - {}".format(e))
        finally:
            _db_connection = None

# Función legacy para compatibilidad
def get_connection():
    """Función legacy - usa get_persistent_connection()."""
    return get_persistent_connection()


# ===========================================
# FUNCIONES DE CONSULTA (HU21.2, HU21.3)
# ===========================================

def get_last_record():
    """
    Obtiene la última lectura registrada en la tabla lecturas.
    Retorna (temp, hum, fecha_hora) o None si no existe data.
    """
    conn = get_persistent_connection()
    if conn is None:
        config.error_logger.error("BD ERROR: No se puede consultar - conexión fallida")
        return None

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
        SELECT temperatura, humedad, fecha_hora
        FROM lecturas
        ORDER BY id DESC
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            temp, hum, fecha_hora = result
            config.logger.debug("BD INFO: Última lectura obtenida - T={}°C, H={}%, Fecha={}".format(temp, hum, fecha_hora))
            return (temp, hum, fecha_hora)
        else:
            config.logger.info("BD INFO: No hay registros en la base de datos")
            return None

    except mariadb.Error as e:
        config.error_logger.error("BD ERROR: Error al consultar última lectura - {}".format(e))
        return None
    finally:
        if cursor:
            cursor.close()


def get_last_10_records():
    """
    Obtiene las últimas 10 lecturas ordenadas de más reciente a más antigua.
    Retorna lista de tuplas [(temp, hum, fecha_hora), ...] o lista vacía si error.
    """
    conn = get_persistent_connection()
    if conn is None:
        config.error_logger.error("BD ERROR: No se puede consultar - conexión fallida")
        return []

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
        SELECT temperatura, humedad, fecha_hora
        FROM lecturas
        ORDER BY id DESC
        LIMIT 10
        """
        cursor.execute(query)
        results = cursor.fetchall()

        records = []
        for row in results:
            temp, hum, fecha_hora = row
            records.append((temp, hum, fecha_hora))

        config.logger.debug("BD INFO: Obtenidas {} lecturas históricas".format(len(records)))
        return records

    except mariadb.Error as e:
        config.error_logger.error("BD ERROR: Error al consultar últimas 10 lecturas - {}".format(e))
        return []
    finally:
        if cursor:
            cursor.close()


def insert_record(temperature, humidity):
    """Inserta un registro en la tabla lecturas."""
    conn = get_connection()
    if conn is None:
        print("No se puede insertar: conexión fallida.")
        return False

    try:
        cursor = conn.cursor()

        query = """
        INSERT INTO lecturas (temperatura, humedad, fecha_hora)
        VALUES (%s, %s, %s)
        """

        current_time = datetime.datetime.now()

        cursor.execute(query, (temperature, humidity, current_time))

        conn.commit()
        print("Registro insertado: T={}°C | H={}% | {}".format(temperature, humidity, current_time))

        return True

    except mariadb.Error as e:
        print("Error al insertar registro:", e)
        return False

    finally:
        conn.close()
        print("Conexion cerrada.")


if __name__ == "__main__":
    print("Este módulo gestiona la base de datos.")
