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
MODO_SIMULACION = False

# TEST_MODE = True → NO inserta datos en BD (solo imprime en consola)
# TEST_MODE = False → Inserta en BD
TEST_MODE = False

# ================================
# CONFIGURACIÓN DEL SENSOR (HU6.6)
# ================================

DHT_PORT = 7    # Puerto del GrovePi donde está conectado el sensor DHT
DHT_TYPE = 0    # Tipo de sensor ((azul) DHT11 = 0, (blanco) DHT22 = 1)

# Intervalo entre lecturas (en segundos)
INTERVALO_LECTURA = 1


# ================================
# CONFIGURACIÓN DE BASE DE DATOS
# ================================
DB_HOST = "localhost"
DB_USER = "TempHum_user"
DB_PASSWORD = "1234TH"
DB_NAME = "RaspberryTempHum"
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

# ===========================================
# LOGGER DE ERRORES (HU20.2)
# ===========================================
ERROR_LOG_FILE = "logs/errors.log"
ERROR_LOG_LEVEL = logging.WARNING

# Logger especializado para errores críticos
error_logger = logging.getLogger("error_system")
error_logger.setLevel(ERROR_LOG_LEVEL)

# Handler para archivo de errores
error_file_handler = logging.FileHandler(ERROR_LOG_FILE)
error_file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
error_logger.addHandler(error_file_handler)

# Handler para consola de errores (solo críticos)
error_console_handler = logging.StreamHandler()
error_console_handler.setLevel(logging.ERROR)
error_console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
error_logger.addHandler(error_console_handler)
