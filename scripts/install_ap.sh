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
cd Desktop/

	# Update the package list
apt-get update

	# Upgrade installed packages
apt-get upgrade -y

	# Install nano editor
apt-get install -y nano

	# Install DMKS
apt-get install -y dkms

	# Clonning the driver for wifi
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
	# Installing the driver
make dkms_install
cd ..
rm -r rtl8812au
	# Access Point ESP-AP configuration
# Access point name
nmcli con add type wifi ifname wlan0 con-name ESP-AP autoconnect yes ssid ESP-AP
# Wifi frecuency and normative status
nmcli con modify ESP-AP 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
# Wifi security settings
nmcli con modify ESP-AP wifi-sec.key-mgmt wpa-psk
# Wifi password
nmcli con modify ESP-AP wifi-sec.psk "123456789"
# Activating Access Point
nmcli con up ESP-AP




