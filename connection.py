import sys
import subprocess
# import pkg_resources
import datetime
import time
import serial
import serial.tools.list_ports
import threading
import csv

current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
baud_rate = 230400
enable_configuration = '#CFGM_ON\r\n'
exit_configuration = '#CFGM_OFF\r\n'
data_store = {}

# def install_package(package):
#     try:
#         pkg_resources.require(package)
#     except pkg_resources.DistributionNotFound:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# install_package('pyserial')


# import serial.tools.list_ports

# Checks if the ADCs using a CH340 chip are connected.

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # print(f"{port.device} - {port.description}")
        if "CH340" in port.description:
            return port.device
    return None

def init_serial_connection():
    device = list_serial_ports()
    if device:
        return serial.Serial(device, baud_rate, timeout=1)
    else:
        print("No ADC connection found.")
        return None

# End of check of ADC connection.
def write_to_file(filename, data):

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def connect(ser, filename):
    if ser:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                data_store.update({datetime.datetime.now().strftime("%H:%M:%S") : data})
                if len(data_store) % 5 == 0:
                    thread1 = threading.Thread(target=write_to_file, args=(filename, data_store,))
                    thread1.start()
                    thread1.join()

                    
            

def still_connected():
    check = list_serial_ports()
    if "USB-SERIAL CH340" in check:
        return False
    return True

