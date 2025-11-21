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

# Importar función del sensor simulado
from sistema.sensor_sim import get_fake_sensor_data


# ==========================
# Función principal
# ==========================

def run_sistem():
    print("Ejecutando sistema en modo SIMULACIÓN...\n")

    try: 
        ### Cuando funciona bien
        # Obtener datos simulados del sensor
        temperatura, humedad = get_fake_sensor_data()

        # Mostrar datos en consola 
        print(f"Temperatura simulada: {temperatura}°C")
        print(f"Humedad simulada: {humedad}%\n")

    except Exception as e:  ### Cuando no funciona bien
        # Manejo básico de errores
        print("⚠️  Advertencia: Fallo al obtener datos del sensor simulado.")
        print(f"Detalles del error: {e}\n")

# ==========================
# Punto de entrada
# ==========================

if __name__ == "__main__":
    if config.MODO_SIMULACION:
        run_sistem()
    else:
        print("Error: main.py aún no está configurado para el sensor real.")


