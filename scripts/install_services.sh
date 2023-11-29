#!/bin/bash

# Check if the script is being run as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use 'sudo $0'." 1>&2
    exit 1
fi
	# Enable the abort mode
set -e

	# Move to the work folder
cd ~/Desktop/Edge_IoT/services/

	# Duplicate the services into /lib/systemd/system services folder
cp my_ups.service /lib/systemd/system/my_ups.service
cp my_canbus.service /lib/systemd/system/my_canbus.service
cp my_server.service /lib/systemd/system/my_server.service

	# Update daemon manager
systemctl daemon-reload

	# Activate services after restart the system
systemctl enable my_ups.service
systemctl enable my_canbus.service
systemctl enable my_server.service
