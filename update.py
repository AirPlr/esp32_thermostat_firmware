import os
import machine

def update_software():
    # Read the new code from main_new.py
    with open('main_new', 'r') as file:
        new_code = file.read()

    # Write the new code to main.py
    with open('main.py', 'w') as file:
        file.write(new_code)

    # Reboot the device
    machine.reset()