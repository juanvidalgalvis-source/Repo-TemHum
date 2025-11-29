import config
import time

# Seleccionar la implementación del sensor según el modo
if config.MODO_SIMULACION:
    from sistema.sensor_sim import get_fake_sensor_data as leer_sensor
else:
    from sistema.sensor_real import read as leer_sensor

def run_system(): # Función principal del sistema
    config.logger.info("Iniciando sistema")
    config.logger.info("Modo simulacion activado" if config.MODO_SIMULACION else "Modo sensor real activado")

    print("====================================")
    if config.MODO_SIMULACION:
        print("Ejecutando en MODO SIMULACION")
    else:
        print("Ejecutando en MODO SENSOR REAL")
    print("====================================")

    # Bucle principal de lectura de datos
    while True: 
        try:
            temperatura, humedad = leer_sensor() 

            if temperatura is None or humedad is None: # Validación de datos
                config.logger.warning("Lectura invalida")
            else:
                print("Temperatura:", temperatura, "Humedad:", humedad)
                config.logger.info("Lectura valida")

            time.sleep(config.INTERVALO_LECTURA) # Esperar antes de la siguiente lectura

        except KeyboardInterrupt:
            print("Sistema detenido por el usuario.")
            config.logger.info("Sistema detenido manualmente")
            break

        except Exception as e:
            print("Error inesperado:", e)
            config.logger.error("Error inesperado en main.py")

if __name__ == "__main__":
    run_system()

