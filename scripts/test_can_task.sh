#!/bin/bash

echo Cerrando can0 port
echo focux | sudo -S ifconfig can0 down

echo Configurando can0 port
echo focux | sudo -S ip link set can0 up type can bitrate 250000

echo Activando virtual enviroment
source /home/jetson-03/Desktop/Edge_IoT/focux_env/bin/activate

echo Activando script en python para la lectura
python /home/jetson-03/Desktop/Edge_IoT/can_read.py

echo focux | sudo -S ifconfig can0 down
echo .
echo Terminado
