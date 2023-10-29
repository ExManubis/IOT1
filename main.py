# IMPORTS
import machine
import sys
import uselect
import _thread
from machine import Pin, ADC
from gpio_lcd import GpioLcd
from time import sleep

# VARIABLES

# Create LCD object
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=2, num_columns=16)

# Create variables + object for battery
battery = ADC(Pin(34)) # set BAT to pin 34
battery.atten(ADC.ATTN_11DB)
bat_min = 2300.0
bat_max = 880.0

# FUNCTIONS

# Battery program as function for threading
def bat_read_thread():
    while True:
        bat1 = battery.read()
        bat2 = battery.read()
        bat3 = battery.read()
        bat4 = battery.read()
        bat5 = battery.read()
        bat_avg = (bat1+bat2+bat3+bat4+bat5) / 5
        bat_1 = float(bat_avg - bat_min)
        bat_pct = float(bat_1 / bat_max)*100
        bat_pct_int = int(bat_pct)
        if bat_pct_int > 100:
            lcd.clear()
            lcd.putstr('Battery: ' + '100%')
        elif:
            lcd.clear()
            lcd.putstr('Battery: ' + str(bat_pct_int)+'%')
        elif bat_pct_int <5:
            sys.exit()
        sleep(60)

# PROGRAM
_thread.start_new_thread(bat_read_thread, ())



