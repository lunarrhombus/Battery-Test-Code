import datetime
import time
import csv
from connection import *


current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
baud_rate = 230400
enable_configuration = '#CFGM_ON\r\n'
exit_configuration = '#CFGM_OFF\r\n'
# Opens connection 
ser = init_serial_connection() 

def enable_config(ser):
    # ser = init_serial_connection()
    response = ""
    while response == "":
        ser.write(enable_configuration.encode())
        response = ser.readline().decode().strip()  
        print(f"Received: {response}")

def exit_config(ser):
    response = ""
    while response == "":
        ser.write(exit_configuration.encode())
        response = ser.readline().decode().strip()  
        print(f"Received: {response}")


def start():
    unit_name = input("PT or PTP: ")
    battery_type = input("Lith or NiMH: ")
    measure_type = input("Voltage or Current: ").title()

    while True:
        if measure_type == "Voltage":
            break
        elif measure_type == "Current":
            break
        measure_type = input("Voltage or Current: ").title()
        
        

    sample_rate = input("Desired sample rate (default = 5 seconds): ")

    if sample_rate == '':
        sample_rate = 5

    if measure_type == "Voltage":
        firmware = input("Firmware: ")
        notes = input("Any notes: ")
        unit_id = input("Unit ID: ")
        filename = text_header_content(unit_name, unit_id, firmware, notes, battery_type)
        voltage(sample_rate, filename)
    if measure_type == "Current":
        firmware = input("Firmware: ")
        notes = input("Any notes: ")
        unit_id = input("Unit ID: ")
        resistor = int(input("Resistance (in Ohms): "))
        current(unit_name, unit_id, sample_rate, firmware, notes, battery_type, resistor)

def text_header_content(unit_name, unit_id, firmware, notes, battery_type):
    initial_data = [[f'Voltage data for: {unit_name}.\nUnit ID: {unit_id}.\nBattery: {battery_type}.\nFirmware: {firmware}.\nNotes: {notes}'],
    ["TIME", "VOLTAGE"]]
    filename = f'./Test_Data/VD_{unit_name}_{battery_type}_{current_time}.csv'

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(initial_data)
    return filename

def voltage(sample_rate, filename):
    
    while True:
        data_to_append = connect(ser, filename)
        if len(data_to_append) > 5:

            append_data_to_csv(filename, data_to_append)
            print("CSV file has been updated with:", data_to_append)
        

def current(unit_name, unit_id, sample_rate, firmware, notes, battery_type, resistor):
    initial_data = [[f'Current data for: {unit_name}.\nBattery: {battery_type}.\nResistance: {resistor}.\nFirmware: {firmware}.\nUnit ID: {unit_id}.\nNotes: {notes}.'],
        ["TIME", "CURRENT"]]
    filename = f'./Test_Data/CD_{unit_name}_{battery_type}_{current_time}.csv'

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(initial_data)

    while True:
        data_to_append = [[datetime.datetime.now().strftime("%H:%M:%S"), ((int(connect())/1000)/resistor)]]
        append_data_to_csv(filename, data_to_append[0])
        print("CSV file has been updated with:", data_to_append)
        time.sleep(int(sample_rate))


# def append_data_to_csv(filename, data):
#     with open(filename, 'a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(data)
        
def auto_cal():
    ser = init_serial_connection()
    enable_config(ser)

    timeout = 2
    timeNow = time.time()
    
    while ( timeout + timeNow ) > time.time():
        ser.write(f'#ZOFFSET_AUTO\r\n'.encode())
        response = ser.readline().decode('utf-8').strip()  

    exit_config(ser)


def mal_cal():
    print("Not done, not doing it!")

def s_rate():
    
    ser = init_serial_connection()
    enable_config(ser)
    rate = input("Desired sample rate (1 - 1000): ")
    
    timeout = 2
    timeNow = time.time()
    
    while ( timeout + timeNow ) > time.time():
        ser.write(f'#SET_MPERS {rate}\r\n'.encode())
        response = ser.readline().decode('utf-8').strip()  
    print(f"Received: {response}")
    exit_config(ser)

def average():
    ser = init_serial_connection()
    enable_config(ser)

    sample_average = input("Number of samples to average (1 - 1000): ")

    timeout = 3
    timeNow = time.time()
    
    while ( timeout + timeNow ) > time.time():
        ser.write(f'#GETMA {sample_average}\r\n'.encode())
        response = ser.readline().decode('utf-8').strip()  

    exit_config(ser)

def read_config():
    ser = init_serial_connection()
    enable_config(ser)

    data =[]
    try:
        c = 0
        while c != 25:
            ser.write(f'#RDCFG\r\n'.encode())
            if ser.in_waiting > 0:
                for i in range(20):  
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').strip()
                        data.append(line)
                    else:
                        break 
        
            print("Received data:", data)
            c += 1


    except KeyboardInterrupt:
        print("Stopped by User")
    exit_config(ser)

def reset():
    ser = init_serial_connection()

    exit_config(ser)