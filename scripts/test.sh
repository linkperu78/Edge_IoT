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

#filename=$(basename "$O" .sh)

filename="can_bus_reader"
py_filename="$filename.py"


# Mostramos el programa en python que corremos
printf "\n ---------------------------\n"
echo "Programa Python : $py_filename"
printf " ---------------------------\n"
python "$py_filename"
printf " ---------------------------\n"

echo focux | sudo -S ifconfig can0 down
echo .
echo Terminado
