"""
sensor_sim.py
Módulo de simulación del sensor de temperatura y humedad.

Este archivo genera valores ficticios dentro de rangos 
realistas para trabajar sin hardware. (Raspberry + GrovePi).
"""

import random


def get_fake_sensor_data():     # Retorna valores simulados de temperatura y humedad.
#   Rango típico del sensor DHT11:
#       Temperatura: 20°C – 30°C
#       Humedad:     40% – 70%

#   Genera valores simulados del sensor. 10% de probabilidad de generar un fallo.

    if random.random() < 0.10: # Probabilidad del 10% de fallo
        raise ValueError("Fallo simulado en el sensor DHT (modo simulación).") 

#   Rango típico simulado
    temperatura = round(random.uniform(20.0, 30.0), 2)
    humedad = round(random.uniform(40.0, 70.0), 2)
#Returns:   tuple: (temperatura, humedad)
    return temperatura, humedad


# # Para probarlo de forma independiente
if __name__ == "__main__":  # Solo corre cuando se ejecuta el archivo de forma independiente  
    temp, hum = get_fake_sensor_data()
    print(f"Temperatura simulada: {temp}°C")
    print(f"Humedad simulada: {hum}%")
