
# esp32_thermostat_firmware
A repository for my smart thermostat/light controller to put in every room. can control every tasmota rgbw light (without hass for now)

Made with micropython to control thermostatic valves without cables because I can't fit them in walls, and to control the light bulb I put in my room by just pressing tangible stuff without taking out my phone or asking alexa

# ONLY CHECK RELEASES, THIS AUTO UPDATES
# HARDWARE NEEDED
I used: 
- The thermistor from the 37 in 1 kit on amazon for Arduino
- The rotary encoder from the same kit
- A 1.3" 128x64 Oled screen from Aliexpress
- An ESP32 WROOM flashed with Micropython
- A lot of cables (maybe building a custom PCB for this could be a nice idea)

# Beta 1: ONLY BASICS
The only things it does is being a bad thermometer, and switching the light on and off

## Beta 2: TO BE RELEASED
Complete refactor of the code, with functions such as Light Temperature Control and RGB Control. The termometer precision should be fixed

---
# TO DO
I'd like to add support for more stuff.
- I want to do a basic configuration via web for the first boot.
- Make it compatible with HASS
- Modding the valves to support tasmota too (or openBK)

