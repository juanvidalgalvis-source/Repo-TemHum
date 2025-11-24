
import grovepi
import time
import logging
from config import DHT_PORT, DHT_TYPE, INTERVALO_LECTURA, logger
from sistema.sensor_errors import validate_not_none, validate_range

def read_raw():
    """
    Realiza una lectura directa al sensor DHT usando grovepi.dht().
    No incluye validaciones ni manejo de errores.
    Devuelve una lista [temperatura, humedad] o valores crudos del sensor.
    """
    try:
        return grovepi.dht(DHT_PORT, DHT_TYPE)
    except Exception as e:
        logger.error(f"Error leyendo grovepi.dht(): {e}")
        return None, None


def read():
    """
    Versión mínima de lectura. 
    - Detecta lecturas None o incompletas.
    - Descarta lecturas inválidas devolviendo (None, None).
    - Retorna (temp, hum) cuando la lectura es válida.
    """

    raw = read_raw()

    # El validador de HU6.2 - Validar None o lectura incompleta
    if not validate_not_none(raw):
        logging.warning("Lectura descartada por ser None o incompleta.")
        return None, None

    temp, hum = raw

    # El validador de HU6.3 - Validar rango
    if not validate_range(temp, hum):
        logging.warning("Lectura descartada por valores fuera de rango.")
        return None, None

    return temp, hum

def read_stable(intentos=3):
    """
    HU8 — Lectura estable.
    Requiere 'intentos' lecturas válidas consecutivas.
    Si una falla, reinicia el conteo.
    """
    lecturas_validas = []

    while len(lecturas_validas) < intentos:
        temp, hum = read()

        if temp is not None and hum is not None:
            lecturas_validas.append((temp, hum))
            logger.debug(f"Lectura válida acumulada: {lecturas_validas}")
        else:
            logger.info("Lectura inválida. Reiniciando ciclo estable.")
            lecturas_validas = []  # Reinicio de estabilización

        time.sleep(INTERVALO_LECTURA)

    # Promedio final para estabilidad física del sensor
    t = sum(v[0] for v in lecturas_validas) / intentos
    h = sum(v[1] for v in lecturas_validas) / intentos

    temp_final = round(t, 2)
    hum_final = round(h, 2)

    logger.info(f"Lectura estable final → Temp={temp_final}, Hum={hum_final}")
    return temp_final, hum_final