import config
import time
from db.db_manager import insert_record
from db.db_manager import get_last_record, get_last_10_records, get_persistent_connection

from sistema.sensor_unified import read_raw as leer_sensor

def show_viewer_menu():
    """
    Muestra un menú interactivo para consultar datos del sistema.
    """
    while True:
        print("\n" + "="*50)
        print("VISOR DE DATOS - SISTEMA TEMP-HUM")
        print("="*50)
        print("1. Mostrar última lectura")
        print("2. Mostrar últimas 10 lecturas")
        print("3. Mostrar estado del sistema")
        print("4. Volver al menú principal")
        print("="*50)

        try:
            choice = input("Selecciona una opción (1-4): ").strip()

            if choice == "1":
                show_last_reading()
            elif choice == "2":
                show_last_10_readings()
            elif choice == "3":
                show_system_status()
            elif choice == "4":
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

        except KeyboardInterrupt:
            print("\n\nVolviendo al menú principal...")
            break
        except Exception as e:
            print("Error en el visor: {}".format(e))

def show_last_reading():
    """Muestra la última lectura (versión simplificada del viewer)."""
    print("\nConsultando última lectura...")
    print("=" * 50)

    try:
        record = get_last_record()

        if record is None:
            print("No hay lecturas registradas en la base de datos.")
            return

        temp, hum, fecha_hora = record
        formatted_time = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')

        print("ÚLTIMA LECTURA")
        print("Temperatura: {}°C".format(temp))
        print("Humedad: {}%".format(hum))
        print("Timestamp: {}".format(formatted_time))
        print("=" * 50)

    except Exception as e:
        print("Error al consultar la base de datos: {}".format(e))

def show_last_10_readings():
    """Muestra las últimas 10 lecturas (versión simplificada del viewer)."""
    print("\nConsultando últimas 10 lecturas...")
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
            formatted_time = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
            print("{:<3} {:<12} {:<10} {:<20}".format(i, temp, hum, formatted_time))

        print("=" * 70)
        print("Total de lecturas mostradas: {}".format(len(records)))

    except Exception as e:
        print("Error al consultar la base de datos: {}".format(e))

def show_system_status():
    """Muestra el estado del sistema (versión simplificada del viewer)."""
    print("\nVerificando estado del sistema...")
    print("=" * 60)

    try:
        # Verificar conexión a BD
        conn = get_persistent_connection()
        if conn:
            db_status = "Conectada"
            conn.close()
        else:
            db_status = "Caída"

        # Obtener última lectura
        last_record = get_last_record()
        if last_record:
            temp, hum, fecha_hora = last_record
            last_reading = "{}°C / {}% ({})".format(temp, hum, fecha_hora.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            last_reading = "No disponible"

        # Nota: Los contadores de errores no están disponibles desde aquí
        consecutive_errors = "No disponible (solo visible durante monitoreo)"

        # Timestamp actual como aproximación del último ciclo
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
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

def run_monitoring(): # Función de monitoreo continuo del sistema
    config.logger.info("Iniciando monitoreo continuo")
    config.logger.info("Modo simulacion activado" if config.MODO_SIMULACION else "Modo sensor real activado")

    print("====================================")
    print("INICIANDO MONITOREO CONTINUO")
    if config.MODO_SIMULACION:
        print("Ejecutando en MODO SIMULACION")
    else:
        print("Ejecutando en MODO SENSOR REAL")
    print("===================================")
    print("Presiona Ctrl+C para detener el monitoreo")
    print("===================================")

    # Contadores de errores consecutivos para alertas
    sensor_consecutive_errors = 0
    db_consecutive_errors = 0

    # Bucle principal de lectura de datos
    while True:
        start_time = time.time()  # Marcar inicio de la iteración

        try:
            temperatura, humedad = leer_sensor()

            if temperatura is None or humedad is None:
                # Lectura fallida - incrementar contador y disparar alertas
                sensor_consecutive_errors += 1
                config.logger.warning("Lectura del sensor fallida - errores consecutivos: {}".format(sensor_consecutive_errors))

                # Disparar alertas según umbrales
                if sensor_consecutive_errors == 5:
                    print("ALERTA: 5 errores consecutivos del sensor")
                    config.logger.warning("ALERTA SENSOR: 5 errores consecutivos del sensor")
                elif sensor_consecutive_errors == 20:
                    print("ALERTA CRÍTICA: 20 errores consecutivos - sensor fallando persistentemente")
                    config.error_logger.error("ALERTA CRÍTICA SENSOR: 20 errores consecutivos - sensor fallando persistentemente")
            else:
                # Lectura exitosa - resetear contador de sensor
                if sensor_consecutive_errors > 0:
                    config.logger.info("Sensor recuperado después de {} errores consecutivos".format(sensor_consecutive_errors))
                    sensor_consecutive_errors = 0

                print("Temperatura:", temperatura, "Humedad:", humedad)
                config.logger.info("Lectura valida")

                if not config.TEST_MODE:
                    success = insert_record(temperatura, humedad)
                    if not success:
                        # Error de BD - incrementar contador y disparar alertas
                        db_consecutive_errors += 1
                        config.logger.warning("Inserción en BD fallida - errores consecutivos: {}".format(db_consecutive_errors))

                        if db_consecutive_errors == 3:
                            print("ALERTA BD: 3 errores consecutivos de base de datos")
                            config.logger.warning("ALERTA BD: 3 errores consecutivos de base de datos")
                    else:
                        # Inserción exitosa - resetear contador de BD
                        if db_consecutive_errors > 0:
                            config.logger.info("BD recuperada después de {} errores consecutivos".format(db_consecutive_errors))
                            db_consecutive_errors = 0

        except KeyboardInterrupt:
            print("\nMonitoreo detenido por el usuario.")
            config.logger.info("Monitoreo detenido manualmente")
            break

        except Exception as e:
            # Error crítico del sistema
            print("ERROR CRÍTICO DEL SISTEMA")
            config.error_logger.error("Inesperado: Error crítico en main.py - {}".format(e))
            config.logger.error("Error inesperado en main.py")

        # Calcular tiempo transcurrido y ajustar sleep para respetar INTERVALO_LECTURA
        elapsed_time = time.time() - start_time
        remaining_time = config.INTERVALO_LECTURA - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)
        else:
            config.logger.warning("Iteración tardó más que INTERVALO_LECTURA: {:.2f}s".format(elapsed_time))

def show_main_menu():
    """
    Muestra el menú principal de la aplicación.
    """
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE MONITOREO TEMPERATURA-HUMEDAD")
        print("="*60)
        print("1. Iniciar monitoreo continuo")
        print("2. Ver datos del sistema (visor)")
        print("3. Salir")
        print("="*60)

        try:
            choice = input("Selecciona una opción (1-3): ").strip()

            if choice == "1":
                run_monitoring()
            elif choice == "2":
                show_viewer_menu()
            elif choice == "3":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intenta de nuevo.")

        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    show_main_menu()
