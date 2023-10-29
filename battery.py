# IMPORTS
import sys
import uselect
from time import sleep
from machine import Pin, ADC

# VARIABLES
battery = ADC(Pin(34, Pin.IN)) # set BAT to pin 25
bat_acd = battery.read()
#bat_percentage = bat_acd

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)

# PROGRAM
while True:
    print(bat_acd)
    sleep(1)