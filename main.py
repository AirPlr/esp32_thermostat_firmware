import network
import urequests
from machine import Pin
from time import sleep
import sh1106
from machine import I2C, ADC, Pin
from math import log
from thermistor import Thermistor
import time
import update

version = "0.0"

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

oled.sleep(False)

oled.fill(0)
oled.text("AirHome", 0, 0)
oled.text("V:"+version, 0, 20)
oled.show()
oled.fill(0)

therm = Thermistor(ADC(34, atten=ADC.ATTN_11DB), beta=3435, therm_ohm=10_000, divider_ohm=10_000)
temperature_array = []
temperature_array.append(round(therm.read_temperature_celsius(),1))
mid_temp_arr=[]

def draw_icon(position_x, image_name_txt,sel):
    # Open the txt file containing the bits
    with open(image_name_txt, "r") as file:
        # Read the bits from the txt file
        bits = file.read()
        
        bytes_array = []
        binary_lines = bits.strip().split("\n")
        for line in binary_lines:
            # Remove leading and trailing whitespace
            line = line.strip()
            for i in range(0, len(line), 8):
                byte = line[i:i+8]
                bytes_array.append(int(byte, 2))
                
    for y in range(0, 64):
        for x in range(0, 8):
            byte = bytes_array[y * 8 + x]
            for bit in range(0, 8):
                pixel = (byte >> (7 - bit)) & 1
                
                if sel:
                    if not pixel:
                        oled.pixel(position_x + x * 8 + bit, y, pixel)
                else:
                    if pixel:
                        oled.pixel(position_x + x * 8 + bit, y, pixel)

# Display the image
    oled.show()

       
    

# Set up Wi-Fi connection
def connect_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        pass
    print("Connected to Wi-Fi")


# Function to update the device software
def update_software():
    # Get the latest version from GitHub releases
    releases_url = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
    owner = "your_github_username"
    repo = "your_repository_name"
    response = urequests.get(releases_url.format(owner=owner, repo=repo))
    latest_version = response.json()["tag_name"]

    # Compare the latest version with the current version
    if latest_version > version:
        print("New version available:", latest_version)
        # Perform the software update here
        # Download the latest main.py from the latest version
        download_url = "https://raw.githubusercontent.com/{owner}/{repo}/{tag}/main.py"
        response = urequests.get(download_url.format(owner=owner, repo=repo, tag=latest_version))
        new_main_code = response.text

        # Save the new main.py as main_new
        with open("main_new.py", "w") as file:
            file.write(new_main_code)

        # Run the update.py script to update the software
        update.update_software()
    else:
        print("No new version available")

# Function to control the Tasmota bulb
def control_bulb(ip, command):
    url = "http://" + ip + "/cm?cmnd=" + command
    response = urequests.get(url)
    print("Bulb command sent:", command)
    print("Response:", response.text)

# Function to read temperature from heat sensor
def read_temperature():
    # Implement your code to read temperature from the heat sensor here
    temp_erature=therm.read_temperature_celsius()
    temperature_array.append(temp_erature)
    if len(temperature_array)>50:
        mid_temp_arr=[]
        mid_temp_arr=temperature_array
        del temperature_array[:45]
        temperature_array.append(sum(mid_temp_arr)/len(mid_temp_arr))
        print(temperature_array)
    temperature=sum(temperature_array)/len(temperature_array)
    temperature=round(temperature,1)
    return temperature+16.5

# Main function
def main():
    
    
    
    
    
    
    
    
    
    
    
    # Connect to Wi-Fi
    
    
    try:
        with open("config", "r") as file:
            ssid = file.readline().strip()
            password = file.readline().strip()
        
    except:    
        ssid = "Your_SSID"
        password = "Your_Password"
    
    
    
    
    
    
    
    
    
    
    
    connect_wifi(ssid, password)

    # IP address of the Tasmota bulb
    bulb_ip = "192.168.1.13"  # Replace with your bulb's IP address

    # Main loop
    while True:
        # Read temperature
        temperature = read_temperature()
        print("Temperature:", temperature)

        # Display temperature on OLED screen
        oled.fill(0)
        oled.text("Temperature:", 0, 0)
        
        oled.text(str(temperature) + " C", 0, 20)
        draw_icon(60, "thermometer.txt",False)
        oled.show()
        # You can use the control_bulb() function to send commands to the Tasmota bulb

        # Delay between readings
        sleep(1)

# Run the main function
if __name__ == "__main__":
    main()