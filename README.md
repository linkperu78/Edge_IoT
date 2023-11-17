# TEMSE-SITECH-IOTBOX-EDGE
## Author
- **Author**: [CST GROUP PERU S.A.C]
- **Colaborators:** 
    - Diego Quispe
    - Paul Huaman 
    - Mario Torres

## Requirements
- **Python (version 3.8.1) :**
    - smbus2
    - Jetson.GPIO
    - flask
    - flask_sqlalchemy
    - SQLalchemy_utils
    - python-can
    
## Description
Este repositorio contiene los programas y archivos requeridos para usar el EDGE AIoTBox para
extraer datos de un equipo R1600H mediante su puerto CAN J1939.
Se realizaran las siguientes funciones:
- Extraer y guardar datos de la maquinaria, decodificandolas y filtrandolas segun valores deseados para almacenar
- Permitir la visualizacion y extraccion de estos datos mediante un servidor local mediante solicitudes HTTP
- Encender y apagar el equipo automaticamente cuando la maquinaria encienda y comience a operar


## Instalacion
Dependiendo de la version que se tenga, se debe proceder con las siguientes instrucciones

### JETSON NANO
1. El equipo ya esta preparado, solo se requiere modificar los archivos dentro de la carpeta
"/json_values" los siguientes campos de acuerdo a la maquinaria a instalar

- `horometer.json`:  
```json
{
  "horometro" : "Cantidad ya existente en la maquinaria", 
  "ralenti"   : "Ignorar este campo"
}
```
- `machine_values.json` :  
```json
{
  "Cargadora" : "# Codigo de la cargadora",
  "IdEmpresa" : "# Id de la empresa",
  "Led"       : "# Pin de control del led verde (default: 10)"
}
```
- `sql_names.json` :  
```json
{
  "name"          : "nombre de la base de datos (.db)",
  "table_salud"   : "nombre de la tabla sql para SALUD",
  "table_pesaje"  : "nombre de la tabla sql para PESAJE",
  "salud_size"    : "Cantidad de datos SALUD a enviar por paquete",
  "pesaje_size"   : "Cantidad de datos PESAJE a enviar por paquete" 
}
```

### RE-COMPUTER J1010
1. Clonar este repositorio en tu equipo local mediante el siguiente comando:
```js
git clone https://github.com/gitfocux/TEMSE-SITECH-IOTBOX-EDGE.git
```

2. Dentro del equipo, muevase al directorio del repositorio


3. Dependiendo de la version

