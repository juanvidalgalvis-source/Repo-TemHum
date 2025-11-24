import random
import logging

from sistema.sensor_errors import validate_not_none, validate_range

# ----------------------------------------------------
# Generador de lecturas simuladas
# ----------------------------------------------------
def generate_random_reading():
    """
    Produce diferentes tipos de lecturas:
    - Lecturas válidas
    - None
    - Listas incompletas
    - Valores None dentro de la lista
    - Valores fuera de rango
    """
    cases = [
        None,
        [],
        [None, 50],
        [25, None],
        [random.uniform(-20, 80), random.uniform(-10, 120)],  # valores locos
        [random.uniform(10, 30), random.uniform(40, 70)]       # valores válidos
    ]
    return random.choice(cases)


# ----------------------------------------------------
# Prueba de validadores
# ----------------------------------------------------
def test_validators(iterations=20):
    print("=== Ejecutando pruebas de validación (HU6.5) ===\n")

    for i in range(iterations):
        reading = generate_random_reading()
        print(f"Test #{i+1}  →  lectura generada:", reading)

        # Validación HU6.2 — None / incompleto
        valid_not_none = validate_not_none(reading)

        if not valid_not_none:
            print(" → Resultado: Lectura descartada por None/incompleta\n")
            continue

        temp, hum = reading

        # Validación HU6.3 — Rango
        valid_range = validate_range(temp, hum)

        if not valid_range:
            print(" → Resultado: Lectura fuera de rango\n")
            continue

        print(" → Resultado: Lectura válida ✔\n")

    print("Pruebas completadas. Revisa logs/sensor.log para detalles.")


# ----------------------------------------------------
# Ejecución directa
# ----------------------------------------------------
if __name__ == "__main__":
    test_validators()
