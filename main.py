# IMPORTS
import machine, Pin, I2C, SoftI2C
import sys
import uselect
import _thread
from machine import Pin, ADC
from gpio_lcd import GpioLcd
from time import sleep
import geofence as geo_f
from imu import MPU6050 #IMU Libary

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

#IMU Related Objects
i2c = SoftI2C(scl = Pin(12), sda = Pin(14), freq =400000) #softI2C for custom pins
imu = MPU6050(i2c)                                        #imu object

#fallcheck function related variables
count = 0         #counter for number of trips measured.
standing = True     #dieraction of the IMU measurement. true is deffined as standing up.
current_value = True        #first check of direction. used to measure differences in directions
previous_value = True        #second check of direction. used to measure differences in directions


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

def fall_detect(): #function for IMU to detect fall
    global current_value  #global values to access variable outside function.
    global previous_value
    global count
    
    if previous_value != current_value and not current_value:  # increase count if check1 and check2 are different. and not already fallen.
        count = count + 1
        print("fall counter: ", count)  #print fall count
    
    previous_value = current_value

def imu_thread():
    while True:
        # reading values
        acceleration = imu.accel   #from Libary, measures acceleration on axis.
        #dunno if need# gyroscope = imu.gyro       #from Libary, measures rotation and direction on axis.
        
        fall_detect()
        
    # data interpretation (accelerometer)

        if abs(acceleration.x) > 0.8:  #abs() function returns absolute values without + or -
            if (acceleration.x > 0):
                #x turned up up
                standing = False
                            
            else:
                #x turned up down
                standing = False 
                
        if abs(acceleration.y) > 0.8:
            if (acceleration.y > 0):
                #y turned up"
                standing = True
                
            else:
                #y turned up down"
                standing = False

        if abs(acceleration.z) > 0.8:
            if (acceleration.z > 0):
                #z turned up"
                standing = False
            
            else:
                #z turned down"
                standing = False 
        
        time.sleep(0.5) #pause between measure


# PROGRAM
_thread.start_new_thread(bat_read_thread, ())



