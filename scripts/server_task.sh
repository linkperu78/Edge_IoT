#!/bin/bash
echo Iniciamos el script del Servidor

# Activate Python Enviroment
echo Activamos el virtual enviroment para Python 3.8
source /home/jetson-03/Desktop/Edge_IoT/focux_env/bin/activate

# Run python script
echo Iniciamos la tarea
python /home/jetson-03/Desktop/Edge_IoT/app.py

echo Terminamos la tarea

