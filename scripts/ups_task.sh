#!/bin/bash
cd ~
cd Desktop/Edge_IoT

echo Iniciando Tarea de UPS - watcher

current_path=$(pwd)
echo "Current directory = $current_path"

# Activate Python Enviroment
source focux_env/bin/activate

# Run python script
python ups_task.py

echo Terminamos la tarea de UPS 

