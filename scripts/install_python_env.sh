#!/bin/bash

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use 'sudo $0'." 1>&2
    exit 1
fi
	# Enable the abort mode
set -e

	# Move to the work folder
cd ~
cd Desktop/Edge_IoT/

	# Update the package list
apt-get update

	# Upgrade installed packages
apt-get upgrade -y

	# Install nano editor
apt-get install -y nano

	# Install python 3.8
apt-get install -y python3.8
apt-get install -y python3.8-venv
python3.8 -m venv focux_env

	# Upgrade pip
source focux_env/bin/activate
cd focux_env/bin
./pip install --upgrade pip

	# Installing the packages
	# for python scripts
cd ~
cd Desktop/Edge_IoT/scripts
pip install -r packages.txt


	# Configure GPIO for admin root
# Modify permissions
sudo chmod g+rw /dev/gpiochip0

# Open the nano editor to create the udev rule file
sudo nano /etc/udev/rules.d/99-gpio.rules <<EOF
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"
EOF
