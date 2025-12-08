# Proyecto RaspBerry Temp-Hum

*Proyecto académico* orientado a la implementación de un sistema embebido que permite leer temperatura y humedad utilizando una *Raspberry Pi*, el módulo *GrovePi* y un *sensor DHT-11*. El sistema almacena los datos en una *base de datos MariaDB* y se desarrolla de forma modular para facilitar su evolución por versiones (V1.0, V1.1, V2.0, V3.0 y V4.0). El objetivo principal es aprender y aplicar buenas prácticas de diseño embebido, manejo de sensores, separación lógica del software y gestión del proyecto mediante *metodologías ágiles*.

Este proyecto sigue un flujo básico donde el sensor proporciona los datos ambientales, Python los procesa y valida, y finalmente son almacenados en la base de datos para su consulta posterior (en la base de datos). Cada versión del proyecto agrega capas de funcionalidad progresiva que consolidan el sistema hasta llegar al entregable final: una arquitectura estable, validada y completamente documentada.

## Características principales
* Lectura real/simulada del sensor DHT
* Validación avanzada de errores
* Inserción en MariaDB
* Logging estructurado
* Modo simulación / modo hardware
* Modularidad del sistema

## Flujo de ejecucion del programa actual (v2.0)
1. main.py carga configuración
2. Selecciona sensor real o simulado
3. Lee valores
4. Valida
5. Inserta en la BD
6. Guarda logs
7. Repite según intervalo

## Estado del proyecto

Versión actual: V2.0 — Reestructuracion (Funcionalidad basica completa)

* Lecturas simuladas (sensor_sim.py).
* Lectura real del sensor DHT con GrovePi (sensor_real.py).
* Validación de lecturas (sensor_errors.py).
* Inserción de datos en MariaDB (db_manager.py).
* Pruebas unitarias (todos los archivos comenzados por _test_). [Se eliminara cuando el proyecto este completo]
* Logging centralizado (logs/sensor.log).
* Estructura modular establecida.
* Compatibilidad con Python 3.5.3 (Raspberry Pi).
* Uso de MySQLdb para conexiones a base de datos.

### En desarrollo:
Carpeta interfaz/ y modulo de interfaz. Ajustes finales de config.py.
Lectura estabilizada del sensor. 

## Arquictura cliente-servidor
El sistema implementa una arquitectura *cliente-servidor local de dos capas (two-tier)* ejecutada completamente dentro de la Raspberry Pi. El programa principal en Python actúa como cliente, encargado de leer el sensor y enviar las solicitudes de inserción hacia MariaDB, que funciona como el servidor de datos. Ambos componentes residen en la misma máquina, por lo que toda la comunicación cliente-servidor ocurre de forma interna.
*Cliente (main.py) → Servidor (MariaDB)*

A futuro se planea incorporar una interfaz gráfica que consulte los registros almacenados. Para ello, el sistema evolucionará hacia una *arquitectura de tres capas (three-tier)*, en la cual una API intermedia se encargará de gestionar las solicitudes entre la interfaz y la base de datos, evitando el acceso directo del cliente a MariaDB.
*Cliente (interfaz) → API (lógica intermedia) → Servidor (MariaDB)*

## Arquitectura (Markdown) del proyecto: V2.0
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
    ├─ test_validators.py
    └─ codigo/
        └─ Home_Weather_Display.py

```

## Tecnologías

* Python 3.5.3 (compatible con Raspberry Pi)
* Raspberry Pi + GrovePi
* Sensor DHT-11 (Sensor azul)
* MariaDB
* MySQLdb (para conexiones a base de datos)
* Git y GitHub (Guardar versiones y reporte del proyecto)
* VSCode (escritura del proyecto)
* Thonny (entorno de desarrollo en Raspberry Pi)

### Ejecución
Modo simulación (configurar TEST_MODE = True en config.py):
```
python main.py
```
Modo hardware real (configurar TEST_MODE = False en config.py):
```
python main.py
```
Ambos modos están completamente implementados y funcionales en V2.0.
Los datos recopilados se deben de ver en la base de datos, aun no se implementa la interfaz.

### Base de datos
Ejecutar el script:
```
db/tablas.sql
```
Esto crea la base de datos raspberry_temp_hum y la tabla lecturas.

### Scripts relevantes
* main.py — punto de entrada principal del sistema
* config.py — configuración del sistema (modo simulación/hardware, BD, etc.)
* db/db_manager.py — funciones de conexión e inserción a MariaDB
* sistema/sensor_real.py — lectura real del sensor DHT con GrovePi
* sistema/sensor_sim.py — simulación de lecturas del sensor
* sistema/sensor_errors.py — validación y manejo de errores de lecturas
* sistema/codigo/Home_Weather_Display.py — código base para mostrar temperatura y humedad en pantalla LCD RGB con GrovePi (Es parte de los proyectos de ejemplo incluidos en el GrovePi starter kit, se puede encontrar en la documentación o tutoriales de Dexter Industries) [El proyecto solo estrae lo escencial de este cdigo para funcionar]

### Requisitos de instalación
En Raspberry Pi:
```
pip3 install mysqlclient
```
Para compatibilidad con Thonny, se han eliminado emojis y se usa formato de cadenas compatible con Python 3.5.3.

## Licencia
Proyecto académico — no destinado para uso comercial.
Código base del GrovePi es propiedad de Dexter Industries.

# Autor
Juan Felipe Vidal Galvis /
Proyecto academico “RaspBerry Temp-Hum” — Universidad del Valle

### Este proyecto fue desarrollado únicamente con fines educativos como parte del curso Metodologías de Desarrollo de Software – Universidad del Valle.