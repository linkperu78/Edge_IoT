import subprocess
import re

# Funciones base
def get_jetson_mac_address(interface = 'eth0'):
    try:
        output = subprocess.check_output(['ipconfig', interface]).decode('utf-8')
        mac_address = re.search(r'(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', output).group(0)
        print(mac_address)
        rpta = ""
        for mac in mac_address.split(':') :
            rpta += str(mac)
        return rpta
    except (subprocess.CalledProcessError, AttributeError):
        return "None"

# Estos seras las variables globales
# Que depende de la maquina

# Variables como llaves
# Direccion fisica MAC del Edge AIoT Box
mac = get_jetson_mac_address()

name_database = "dato.db"
name_salud_general = "salud_table"
name_salud_no_enviados = "salud_no_enviados"
name_pesaje_no_enviados = "pesaje_no_enviados"
package_size = 300
ip_default = "192.168.137.1"


# Estos valores van a eliminarse pues deben estar en el frontend
cargadora = "AE-SC-03"
id_empresa = 44

