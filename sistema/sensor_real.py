import grovepi
import logging
from math import isnan
from config import DHT_PORT, DHT_TYPE, logger

def read():
    
    try:
        # Leer datos del sensor DHT
        temp, hum = grovepi.dht(DHT_PORT, DHT_TYPE)

        # Validar los datos leídos
        if temp is None or hum is None:
            return None, None
        
        # Comprobar si los valores son NaN (vacíos)
        if isnan(temp) or isnan(hum):
            return None, None

        return temp, hum
    
    # Manejar excepciones específicas del sensor
    except Exception as e:
        logger.error("Error leyendo el sensor DHT")
        return None, None
