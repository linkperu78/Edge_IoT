#!/bin/bash
echo Iniciando Tarea de UPS - watcher

# Activate Python Enviroment
source /home/jetson/Desktop/Edge_IoT/focux_env/bin/activate

# Run python script
python /home/jetson/Desktop/Edge_IoT/ups_task.py

echo Terminamos la tarea

