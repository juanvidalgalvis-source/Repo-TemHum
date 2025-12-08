# sistema/sensor_errors.py

import logging
from config import TEMP_MIN, TEMP_MAX, HUM_MIN, HUM_MAX

# ----------------------------------------------------
# validate_not_none(data)
# Detecta valores None, listas vacías o lecturas incompletas
# ----------------------------------------------------
def validate_not_none(data):
    """
    data puede ser:
    - None
    - lista vacía []
    - lista incompleta [temp] o [None, hum]
    """
    if data is None:
        logging.error("Lectura recibida es None.")
        return False

    if isinstance(data, (list, tuple)):
        if len(data) >= 2:
            temp, hum = data[0], data[1]
        else:
            logging.error("Lectura incompleta.")
            return False
    else:
        logging.error("Tipo inválido.")
        return False

    
    if len(data) != 2:
        logging.error("Lectura incompleta: no tiene dos valores (temp, hum).")
        return False

    temp, hum = data

    if temp is None or hum is None:
        logging.error("Lectura contiene valores None.")
        return False

    return True


# ----------------------------------------------------
# validate_range(temp, hum)
# Revisa valores fuera de rango físico
# ----------------------------------------------------
def validate_range(temp, hum):
    """
    Verifica que los valores se encuentren dentro de los
    límites definidos en config.py.
    Maneja casos de valores NaN, strings, y None.
    """

    # -----------------------------------------
    # 1. Verificar que temp y hum sean numéricos
    # -----------------------------------------
    try:
        temp = float(temp)
        hum = float(hum)
    except (TypeError, ValueError):
        logging.error("Lectura inválida: valores no numéricos → temp=%s, hum=%s" % (temp, hum))
        return False

    # -----------------------------------------
    # 2. Verificar que no sean NaN
    # -----------------------------------------
    if temp != temp or hum != hum:  # NaN nunca es igual a sí mismo
        logging.error("Lectura inválida: contiene valores NaN.")
        return False

    # -----------------------------------------
    # 3. Validación de rangos físicos
    # -----------------------------------------
    if temp < TEMP_MIN or temp > TEMP_MAX:
        logging.error("Temperature out of range: %s°C" % temp)
        return False

    if hum < HUM_MIN or hum > HUM_MAX:
        logging.error("Humidity out of range: {}%".format(hum))
        return False

    return True



# ----------------------------------------------------
# log_error(message)
# (Versión temporal antes de 6.4 / 6.7)
# Registrar errores si no existe logging global aún.
# ----------------------------------------------------
def log_error(message):
    """
    Función opcional que permite registrar errores directos.
    Esta función será absorbida por el logging global en 6.4.
    """
    logging.error(message)
