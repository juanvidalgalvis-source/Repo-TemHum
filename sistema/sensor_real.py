"""
sensor_real.py
Módulo para lectura del sensor real de temperatura y humedad.

Este archivo solo lee del hardware, sin validaciones ni excepciones controladas.
"""

import grovepi
from config import DHT_PORT, DHT_TYPE

def read():
    """
    Lectura cruda del sensor real.
    Solo lee del hardware, sin validaciones.
    """
    return grovepi.dht(DHT_PORT, DHT_TYPE)


def read_stable():
    """
    Función responsable exclusiva de obtener una lectura confiable del sensor real.
    Intenta leer hasta 3 veces en caso de fallos, con validaciones completas.
    """
    import time
    from math import isnan
    from config import logger
    from sistema.sensor_errors import validate_not_none, validate_range

    max_attempts = 3
    retry_delay = 0.5  # Espera entre intentos en segundos

    for attempt in range(1, max_attempts + 1):
        try:
            logger.debug("Intento {} de lectura del sensor real".format(attempt))

            # 1. Lectura cruda del sensor real
            temp, hum = grovepi.dht(DHT_PORT, DHT_TYPE)

            # 2. Validación de None / valores incompletos
            if not validate_not_none([temp, hum]):
                logger.warning("Intento {}: Lectura descartada - None o incompleta".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # 3. Validación NaN
            if isnan(temp) or isnan(hum):
                logger.warning("Intento {}: Lectura descartada - valores NaN".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # 4. Validación de rango físico
            if not validate_range(temp, hum):
                logger.warning("Intento {}: Lectura descartada - fuera de rango físico".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # Lectura exitosa
            logger.debug("Intento {}: Lectura exitosa - Temp: {}°C, Hum: {}%".format(attempt, temp, hum))
            return temp, hum

        except Exception as e:
            logger.warning("Intento {}: Error leyendo el sensor real: {}".format(attempt, e))
            if attempt < max_attempts:
                time.sleep(retry_delay)
            else:
                logger.error("Todos los intentos fallaron - devolviendo None")
                return None, None
