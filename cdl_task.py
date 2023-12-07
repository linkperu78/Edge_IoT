import rs485_lib as rs485
import serial

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Replace with your RS485 port
    baudrate=9600,         # Set baudrate according to your device settings
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

path_json_data = "json_values/parameters"
rs485_dictionary = rs485.cdl_rs485(path_json_data)
data_byte = rs485_dictionary.rs485_request(1,0,11)

try:
    # Send the hexadecimal message
    ser.write(bytearray(data_byte))
    print("Message sent successfully:", ' '.join([f'0x{byte:02X}' for byte in data_byte]))
except serial.SerialException as e:
    print("Error:", e)
finally:
    ser.close()  # Close the serial port



