# IMPORTS
from machine import Pin
from gpio_lcd import GpioLcd
from time import sleep

# VARIABLES

# Create LCD object
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=2, num_columns=16)

# PROGRAM
while True:
    lcd.putstr('I2C LCD Tutorial')
    sleep(2)
    lcd.clear()
    lcd.putstr('Lets count 0-10!')
    sleep(2)
    lcd.clear()
    for i in range(11):
        lcd.putstr(str(i))
        sleep(1)
        lcd.clear()