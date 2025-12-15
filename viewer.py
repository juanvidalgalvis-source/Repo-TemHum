"""
viewer.py
Interfaz de línea de comandos (CLI) para consultar el estado del sistema de temperatura y humedad.

Permite consultar lecturas y estado del sistema sin necesidad de ejecutar el loop principal.
Uso: python viewer.py --last | --last10 | --status
"""

import argparse
import sys
import time
from datetime import datetime

# Importar módulos del sistema
import config
from db.db_manager import get_last_record, get_last_10_records, get_persistent_connection


def format_timestamp(timestamp):
    """
    Convierte timestamp a formato legible YYYY-MM-DD HH:MM:SS
    """
    if isinstance(timestamp, str):
        # Si ya es string, intentar parsear
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return timestamp
    elif isinstance(timestamp, (int, float)):
        # Timestamp Unix
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(timestamp)


def show_last_reading():
    """
    Muestra la última lectura registrada en la base de datos.
    """
    print("Consultando última lectura...")
    print("=" * 50)

    try:
        record = get_last_record()

        if record is None:
            print("No hay lecturas registradas en la base de datos.")
            return

        temp, hum, fecha_hora = record
        formatted_time = format_timestamp(fecha_hora)

        print("ÚLTIMA LECTURA")
        print("Temperatura: {}°C".format(temp))
        print("Humedad: {}%".format(hum))
        print("Timestamp: {}".format(formatted_time))
        print("=" * 50)

    except Exception as e:
        print("Error al consultar la base de datos: {}".format(e))
        print("Verifica que la base de datos esté disponible.")


def show_last_10_readings():
    """
    Muestra las últimas 10 lecturas en formato ordenado.
    """
    print("Consultando últimas 10 lecturas...")
    print("=" * 70)

    try:
        records = get_last_10_records()

        if not records:
            print("No hay lecturas registradas en la base de datos.")
            return

        print("ÚLTIMAS 10 LECTURAS")
        print("{:<3} {:<12} {:<10} {:<20}".format('#', 'Temperatura', 'Humedad', 'Timestamp'))
        print("-" * 70)

        for i, (temp, hum, fecha_hora) in enumerate(records, 1):
            formatted_time = format_timestamp(fecha_hora)
            print("{:<3} {:<12} {:<10} {:<20}".format(i, temp, hum, formatted_time))

        print("=" * 70)
        print("Total de lecturas mostradas: {}".format(len(records)))

    except Exception as e:
        print("Error al consultar la base de datos: {}".format(e))
        print("Verifica que la base de datos esté disponible.")


def show_system_status():
    """
    Muestra un resumen del estado del sistema.
    """
    print("Consultando estado del sistema...")
    print("=" * 60)

    try:
        # Verificar estado de la conexión a BD
        conn = get_persistent_connection()
        if conn is None:
            db_status = "Caída"
        else:
            try:
                conn.ping(reconnect=False)
                db_status = "Activa"
            except:
                db_status = "Reconectando"

        # Obtener última lectura
        last_record = get_last_record()
        if last_record:
            temp, hum, fecha_hora = last_record
            last_reading = "{}°C / {}% ({})".format(temp, hum, format_timestamp(fecha_hora))
        else:
            last_reading = "No disponible"

        # Nota: Los contadores de errores consecutivos no están disponibles
        # desde el viewer ya que son variables locales del main loop
        consecutive_errors = "No disponible (requiere ejecutar main.py)"

        # Timestamp actual como aproximación del último ciclo
        current_time = format_timestamp(time.time())
        last_cycle = "Aproximado: {}".format(current_time)

        print("ESTADO DEL SISTEMA")
        print("Base de datos: {}".format(db_status))
        print("Última lectura: {}".format(last_reading))
        print("Errores consecutivos: {}".format(consecutive_errors))
        print("Último ciclo exitoso: {}".format(last_cycle))
        print("=" * 60)

        if db_status == "Caída":
            print("Recomendación: Verifica la conexión a MariaDB")
        else:
            print("Sistema operativo correctamente")

    except Exception as e:
        print("Error al consultar el estado del sistema: {}".format(e))
        print("Verifica que los módulos del sistema estén disponibles.")


def main():
    """
    Función principal del CLI viewer.
    """
    parser = argparse.ArgumentParser(
        description="Viewer CLI para el sistema de temperatura y humedad",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python viewer.py --last      # Muestra la última lectura
  python viewer.py --last10    # Muestra las últimas 10 lecturas
  python viewer.py --status    # Muestra el estado del sistema
        """
    )

    # Definir argumentos mutuamente excluyentes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--last',
        action='store_true',
        help='Muestra la última lectura registrada'
    )
    group.add_argument(
        '--last10',
        action='store_true',
        help='Muestra las últimas 10 lecturas'
    )
    group.add_argument(
        '--status',
        action='store_true',
        help='Muestra el estado general del sistema'
    )

    # Parsear argumentos
    args = parser.parse_args()

    # Ejecutar la función correspondiente
    try:
        if args.last:
            show_last_reading()
        elif args.last10:
            show_last_10_readings()
        elif args.status:
            show_system_status()

    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print("\nError inesperado: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
