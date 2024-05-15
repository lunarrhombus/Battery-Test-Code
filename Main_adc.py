import datetime
from connection import *
from commands import *
import os

folder_path = './Test_Data'


def check_user_commands():
    commands = {
        "start": start,
        "auto_cal": auto_cal,
        "mal_cal": mal_cal,
        "s_rate": s_rate,
        "average": average,
        "read_config": read_config,
        "reset": reset,
        # "d_comm": d_comm
    }
    
    while True:
        command_input = input("Enter command: ")
        if command_input in commands:
            commands[command_input]()
            break  # Exit the loop after executing the command
        else:
            print("Unknown command. Please try again.")

def folder_check():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Data folder made.", folder_path)
        return 0
    else:
        return 0

def commands():
    print("****************************************************************************************************")
    print("See commands below")
    print("Note: Use ctrl + C to stop")
    print("start                  Start program, read and record.")
    print("auto_cal               Automatically calibrate ADC.")
    print("man_cal                Manually set zero value, -500 to 500.")
    print("s_rate                 Change sample rate, 0 to 1000 (0 means no measurement).")
    print("average                Give average of X number of samples, 0 - 1000.")
    print("read_config            Read current ADC configuration.")
    print("reset                  Reset.")
    print("\n")
    print("****************************************************************************************************")
    print("\n")
    check_user_commands()

   

if __name__ == "__main__":
    try:
        while True:
            folder_check()
            commands()
    except KeyboardInterrupt:
        print("Stopped by User")