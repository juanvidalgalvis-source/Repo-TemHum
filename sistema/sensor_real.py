import grovepi
import logging
from math import isnan
from config import DHT_PORT, DHT_TYPE, logger

def read():
    
    try:
        temp, hum = grovepi.dht(DHT_PORT, DHT_TYPE)

        # Validación EXACTA como la del profesor
        if temp is None or hum is None:
            return None, None
        
        if isnan(temp) or isnan(hum):
            return None, None

        return temp, hum

    except Exception as e:
        logger.error(f"Error leyendo el sensor DHT: {e}")
        return None, None
