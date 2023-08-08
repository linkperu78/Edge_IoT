#!/bin/bash

echo Cerrando can0 port
echo focux | sudo -S ifconfig can0 down

echo Configurando can0 port
echo focux | sudo -S ip link set can0 up type can bitrate 250000

echo Activando virtual enviroment
source /home/jetson/Desktop/Edge_IoT/focux_env/bin/activate

echo Activando script en python para la lectura
python /home/jetson/Desktop/Edge_IoT/my_test_can.py

echo focux | sudo -S ifconfig can0 down
echo .
echo Terminado
