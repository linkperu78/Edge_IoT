#!/bin/bash
echo Instalando paquete para Python 3.8
echo "Do you want to continue? [y/n] "
read answer

if [[ $answer == "y" || $answer == "Y" ]] ; then
 echo "Installing ..."
 sudo apt-get install python3.8 python3.8-dev python3.8-distutils python3.8-venv
elif [[ $answer == "n" || $answer == "N" ]]  ; then
 echo "Skip installation"
else
 echo "Invalid input, Y/y or N/n"
 exit 0
fi

cd ..
echo "Creando el virtual enviroment 'focux_env' "
sudo python3.8 -m venv focux_env
echo " Se ha terminado, chequear el entorno"


