"""
sensor_unified.py
Módulo unificado para lectura del sensor de temperatura y humedad.

Este archivo centraliza la lectura cruda del sensor (real o simulado)
con todas las validaciones esenciales integradas.
"""

from math import isnan
import config
from sistema.sensor_errors import validate_not_none, validate_range

def read_raw():
    """
    Función unificada para lectura cruda del sensor.
    Realiza la lectura (real o simulada) con reintentos e integra todas las validaciones esenciales.

    Retorna:
        (temp, hum) si datos válidos
        (None, None) si error o datos inválidos después de reintentos
    """
    import time

    max_attempts = 3
    retry_delay = 0.5  # Espera entre intentos en segundos

    for attempt in range(1, max_attempts + 1):
        try:
            config.logger.debug("Intento {} de lectura del sensor".format(attempt))

            # Seleccionar fuente de datos según modo
            if config.MODO_SIMULACION:
                # Lectura simulada
                temp, hum = _read_simulated()
            else:
                # Lectura real del hardware
                temp, hum = _read_real()

            # 1. Validación de None / valores incompletos
            if not validate_not_none([temp, hum]):
                config.logger.warning("Intento {}: Lectura descartada - None o incompleta".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # 2. Validación NaN
            if isnan(temp) or isnan(hum):
                config.logger.warning("Intento {}: Lectura descartada - valores NaN".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # 3. Validación de rango físico
            if not validate_range(temp, hum):
                config.logger.warning("Intento {}: Lectura descartada - fuera de rango físico".format(attempt))
                if attempt < max_attempts:
                    time.sleep(retry_delay)
                    continue
                else:
                    return None, None

            # Lectura exitosa
            config.logger.debug("Intento {}: Lectura exitosa - Temp: {}°C, Hum: {}%".format(attempt, temp, hum))
            return temp, hum

        except Exception as e:
            config.logger.warning("Intento {}: Error leyendo el sensor: {}".format(attempt, e))
            if attempt < max_attempts:
                time.sleep(retry_delay)
            else:
                config.logger.error("Todos los intentos fallaron - devolviendo None")
                return None, None

def _read_real():
    """Lectura cruda del sensor real (sin validaciones)."""
    try:
        import grovepi
        return grovepi.dht(config.DHT_PORT, config.DHT_TYPE)
    except ImportError:
        # Si grovepi no está disponible, forzar modo simulación
        config.logger.warning("grovepi no disponible - forzando modo simulación")
        return _read_simulated()

def _read_simulated():
    """Lectura cruda del sensor simulado (sin validaciones)."""
    import random

    # Probabilidad del 10% de fallo simulado
    if random.random() < 0.10:
        raise ValueError("Fallo simulado en el sensor DHT (modo simulación).")

    # Rango típico simulado
    temperatura = round(random.uniform(20.0, 30.0), 2)
    humedad = round(random.uniform(40.0, 70.0), 2)
    return temperatura, humedad
