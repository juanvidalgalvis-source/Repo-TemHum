"""
sensor_sim.py
Módulo de simulación del sensor de temperatura y humedad.

Este archivo genera valores ficticios dentro de rangos
realistas para trabajar sin hardware. (Raspberry + GrovePi).
Solo genera datos, sin validaciones.
"""

import random


def get_fake_sensor_data():
    """
    Genera valores simulados del sensor.
    Solo genera datos, sin validaciones ni excepciones controladas.
    """
    # Probabilidad del 10% de fallo
    if random.random() < 0.10:
        raise ValueError("Fallo simulado en el sensor DHT (modo simulación).")

    # Rango típico simulado
    temperatura = round(random.uniform(20.0, 30.0), 2)
    humedad = round(random.uniform(40.0, 70.0), 2)
    return temperatura, humedad





# # Para probarlo de forma independiente
if __name__ == "__main__":  # Solo corre cuando se ejecuta el archivo de forma independiente
    temp, hum = get_fake_sensor_data()
    print("Temperatura simulada: {}°C".format(temp))
    print("Humedad simulada: {}%".format(hum))
