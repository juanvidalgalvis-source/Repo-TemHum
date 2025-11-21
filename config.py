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


# # ================================
# # CONFIGURACIÓN DEL SENSOR
# # ================================
# # Puerto del GrovePi donde está conectado el sensor DHT
# DHT_PORT = 7

# # Tipo de sensor (DHT11 = 0, DHT22 = 1)
# DHT_TIPO = 0

# # Intervalo entre lecturas (en segundos)
# INTERVALO_LECTURA = 5


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
