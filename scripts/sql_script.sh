#!/bin/bash

cd ~
cd Desktop/Edge_IoT

echo Ejecutamos el programa "sql_script.py"

# Activate Python Enviroment
source focux_env/bin/activate

# Run python script
python sql_script.py

echo Terminamos la tarea

