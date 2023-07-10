#!/bin/bash

cd ~
cd Desktop/Edge_IoT

echo Iniciamos el script del Servidor

# Activate Python Enviroment
echo Activamos el virtual enviroment para Python 3.8
source focux_env/bin/activate

# Run python script
echo Iniciamos la tarea
python app.py

echo Terminamos la tarea

