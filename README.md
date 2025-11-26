# Proyecto RaspBerry Temp-Hum

*Proyecto académico* que implementa un sistema embebido para leer temperatura y humedad usando Raspberry Pi, GrovePi y un sensor DHT. Los datos se almacenan en MariaDB y el sistema está organizado con una arquitectura modular para facilitar la evolución por versiones.

## Estado del proyecto

Versión actual: V1.1 — Simulación (con intento de implementacion de hardware)

* Lecturas simuladas (sensor_sim.py).
* Lectura real preliminar del sensor DHT (sensor_real.py).
* Validación de lecturas (sensor_errors.py).
* Inserción de datos en MariaDB (db_manager.py).
* Pruebas unitarias (todos los archivos comenzados por _test_).
* Logging centralizado (logs/sensor.log)
* Estructura modular establecida.

### En desarrollo:
Carpeta interfaz/. Ajustes finales de config.py.
Integración con el código oficial del profesor (será parte de la Versión 2, aún no disponible).
(Aunque el código existe, aún no forma parte de la versión estable por falta de pruebas en laboratorio).

## Arquitectura del proyecto: V1.1
```
Repo-TemHum/
│  .gitignore
│  main.py
│  README.md
│  test_insert.py
│  test_sensor_import.py
│
├─ db/
│   ├─ __init__.py
│   ├─ db_manager.py
│   ├─ tablas.sql
│   └─ test_connection.py
│
├─ interfaz/
│   (vacía)
│
├─ logs/
│   (vacía, se llena al ejecutar el sistema)
│
└─ sistema/
    ├─ __init__.py
    ├─ sensor_errors.py
    ├─ sensor_real.py
    ├─ sensor_sim.py
    └─ test_validators.py

```

## Tecnologías

* Python 3
* Raspberry Pi + GrovePi [Por implementar]
* Sensor DHT [Por implementar]
* MariaDB
* Git y GitHub (Guardar versiones y reporte del proyecto)
* VSCode (escritura del proyecto)

### Ejecución
Modo simulación (modo actual estable):
```
python main.py
```
Modo hardware real: Implementado parcialmente en sensor_real.py, pero aún no probado ni validado, por lo que no forma oficialmente parte de V1.1.

### Base de datos
Ejecutar el script:
```
db/tablas.sql
```
Esto crea la base de datos raspberry_temp_hum y la tabla lecturas.

### Scripts relevantes
* db_manager.py — funciones de conexión e inserción
* test_connection.py — prueba directa de conexión
* test_insert.py — inserción de datos simulados

# Autor
Juan Felipe Vidal Galvis /
Proyecto academico “RaspBerry Temp-Hum” — Universidad del Valle
