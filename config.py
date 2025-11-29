"""
config.py
Archivo de configuración global del proyecto RaspBerry temp-hum.

Aquí se definen todas las constantes:
- Intervalos de lectura
- Parámetros del sensor
- Credenciales de base de datos
- Ubicación de archivos de logs
- Modos de operación (simulación / hardware real)
"""

# ================================
# MODO DE OPERACIÓN
# ================================
# True  → Usar valores simulados (sin hardware)
# False → Usar GrovePi + Sensor DHT real
MODO_SIMULACION = True

# TEST_MODE = True → NO inserta datos en BD (solo imprime en consola)
# TEST_MODE = False → Inserta en BD
TEST_MODE = True

# ================================
# CONFIGURACIÓN DEL SENSOR (HU6.6)
# ================================

DHT_PORT = 7    # Puerto del GrovePi donde está conectado el sensor DHT
DHT_TYPE = 0    # Tipo de sensor ((azul) DHT11 = 0, (blanco) DHT22 = 1)

# Intervalo entre lecturas (en segundos)
INTERVALO_LECTURA = 3


# ================================
# CONFIGURACIÓN DE BASE DE DATOS
# ================================
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "raspberry_temp_hum"
DB_PORT = 3306


# ================================
# RUTAS Y ARCHIVOS
# ================================
#RUTA_LOG_ERRORES = "logs/errores.log"
#RUTA_LOG_DATOS = "logs/datos_sensor.log"

# Archivo SQL opcional para inicialización
#RUTA_SQL_TABLAS = "db/tablas.sql"


# ================================
# CONFIGURACIÓN DE INTERFAZ
# ================================
#MOSTRAR_EN_CONSOLA = True


# ================================
# RANGOS DE VALIDACIÓN
# ================================
TEMP_MIN = -10
TEMP_MAX = 60

HUM_MIN = 0
HUM_MAX = 100


# ===========================================
# LOGGING CENTRALIZADO (HU6.7)
# ===========================================
import logging
import os
os.makedirs("logs", exist_ok=True) # Asegura que la carpeta de logs exista

LOG_FILE = "logs/sensor.log"    # Ruta del archivo de log
LOG_LEVEL = logging.INFO   # Nivel de logging   # Cambiable a DEBUG en ramas C

# Inicialización global del logger
logging.basicConfig(
    filename=LOG_FILE,
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s")

# Logger global accesible desde TODOS los módulos
logger = logging.getLogger("sensor_system")