import fcntl

def find_can_bitrate(channel='can0'):
    with open(f"/dev/{channel}", 'rb') as can_interface:
        # Get the bitrate using SIOCGCANBITRATE
        result = fcntl.ioctl(can_interface, 0x89ff, 0)
        # Extract the bitrate from the result
        bitrate = int.from_bytes(result[:4], byteorder='little')
    return bitrate

bitrate = find_can_bitrate()
print(f"CAN bus bitrate: {bitrate} bps")

