-- Documetacion de respaldo

CREATE DATABASE IF NOT EXISTS RaspberryTempHum;

USE RaspberryTempHum;

CREATE TABLE IF NOT EXISTS lecturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT NOT NULL,
    humedad FLOAT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
