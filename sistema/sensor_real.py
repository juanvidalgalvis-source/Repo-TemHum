import grovepi
from math import isnan
from config import DHT_PORT, DHT_TYPE, logger
from sistema.sensor_errors import validate_not_none, validate_range

def read():
    try:
        # 1. Lectura cruda del sensor
        temp, hum = grovepi.dht(DHT_PORT, DHT_TYPE)

        # 2. Validación de None / valores incompletos
        if not validate_not_none([temp, hum]):
            logger.warning("Lectura descartada: None o incompleta")
            return None, None

        # 3. Validación NaN
        if isnan(temp) or isnan(hum):
            logger.warning("Lectura descartada: valores NaN")
            return None, None

        # 4. Validación de rango físico
        if not validate_range(temp, hum):
            logger.warning("Lectura descartada: fuera de rango físico")
            return None, None

        return temp, hum

    except Exception as e:
        logger.error("Error leyendo el sensor DHT: {}".format(e))
        return None, None
