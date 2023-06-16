#!/bin/bash
bit_rate = 250000

echo Cerrando can0 port
sudo ifconfig can0 down

echo Configurando can0 port
sudo ip link set can0 up type can bitrate 250000
echo CAN0 configurado

echo Escuchando puerto can0
sudo candump can0

sudo ifconfig can0 down
echo .
echo Terminado
