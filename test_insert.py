from sistema.sensor_sim import get_fake_sensor_data
from db.db_manager import insert_record

# Obtener datos simulados
temperature, humidity = get_fake_sensor_data()

print("Insertando datos simulados...")
insert_record(temperature, humidity)
