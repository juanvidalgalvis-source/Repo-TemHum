"""
main.py
Archivo principal del sistema RaspBerry temp-hum.
Coordina la lectura del sensor, el almacenamiento en la base de datos
y la visualización en la interfaz de usuario.
"""

# ==========================
# Importación de módulos
# ==========================

import config
import time

from sistema.sensor_sim import get_fake_sensor_data # Importar función del sensor simulado
from config import logger, INTERVALO_LECTURA # Importar intervalo de lectura

# -----------------------------
# Selección dinámica del sensor
# -----------------------------
if config.MODO_SIMULACION:
    # Modo simulación (sensor falso)
    from sistema.sensor_sim import get_fake_sensor_data as leer_sensor
else:
    # Modo real (hardware)
    from sistema.sensor_real import read_stable as leer_sensor

# ==========================
# Función principal
# ==========================

def run_system():
    logger.info("===== INICIO DEL SISTEMA =====")
    logger.info(f"Modo simulación: {config.MODO_SIMULACION}")

    print("\n====================================")
    if config.MODO_SIMULACION:
        print(" Ejecutando en MODO SIMULACIÓN")
    else:
        print(" Ejecutando en MODO SENSOR REAL (GrovePi)")
    print("====================================\n")

    # -------------------------
    # Bucle principal del sistema
    # -------------------------
    while True:
        try:
            temperatura, humedad = leer_sensor()

            if temperatura is None or humedad is None:
                logger.warning("Lectura inválida, esperando siguiente intento...")
            else:
                print(f"Temperatura: {temperatura}°C — Humedad: {humedad}%")
                logger.info(f"Lectura válida → Temp={temperatura}, Hum={humedad}")

            time.sleep(INTERVALO_LECTURA)

        except KeyboardInterrupt:
            print("\nSistema detenido por el usuario.")
            logger.info("Sistema detenido manualmente.")
            break

        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            logger.error(f"Error inesperado en main.py: {e}")


if __name__ == "__main__":
    run_system()

