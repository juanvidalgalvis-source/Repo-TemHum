# Proyecto RaspBerry Temp-Hum

*Proyecto académico* que implementa un sistema embebido para leer temperatura y humedad usando Raspberry Pi, GrovePi y un sensor DHT. Los datos se almacenan en MariaDB y el sistema está organizado con una arquitectura modular para facilitar la evolución por versiones.

## Estado del proyecto

Versión actual: V1.0 — Simulación

* Lecturas simuladas.
* Inserción de datos en MariaDB.
* Pruebas de conexión.
* Estructura modular establecida.

### En desarrollo: V2 — Pruebas de hardware
Incluye lectura real del sensor, comparación de configuraciones y creación de la versión estable v2-hw.

## Arquitectura del proyecto: V1.0
```
Repo-TemHum/
│  main.py
│  config.py
│
├─ sistema/
│   sensor_sim.py
│
├─ db/
│   db_manager.py
│   test_connection.py
│   tablas.sql
│
├─ interfaz/
└─ logs/
```

## Tecnologías

* Python 3
* Raspberry Pi + GrovePi [Por implementar]
* Sensor DHT [Por implementar]
* MariaDB
* Git y GitHub (Guardar versiones y reporte del proyecto)
* VSCode (escritura del proyecto)

### Ejecución
Modo simulación:
```
python main.py
```
Configurar modo hardware real editando config.py [Por implementar].

### Base de datos
Ejecutar el script:
```
db/tablas.sql
```
Esto crea la base de datos raspberry_temp_hum y la tabla lecturas.

# Autor
Juan Felipe Vidal Galvis /
Proyecto “RaspBerry Temp-Hum” — Universidad del Valle
