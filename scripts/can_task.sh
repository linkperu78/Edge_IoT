#!/bin/bash

echo Cerrando can0 port
echo focux | sudo -S ifconfig can0 down

echo Configurando can0 port
echo focux | sudo -S ip link set can0 up type can bitrate 250000

# Nos movemos a la carpeta
cd ~
cd Desktop/Edge_IoT

echo Activando virtual enviroment
source focux_env/bin/activate

echo Activando script en python para la lectura
python can_bus_reader.py

echo focux | sudo -S ifconfig can0 down
echo .
echo Terminado
