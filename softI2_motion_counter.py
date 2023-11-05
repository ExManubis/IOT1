# Imports

from imu import MPU6050  # IMU libary from https://github.com/micropython-IMU/micropython-mpu9x50
import time
from machine import Pin, I2C, SoftI2C

# Objects

i2c = SoftI2C(scl = Pin(13), sda = Pin(14), freq =400000) #softI2C for custom pins
imu = MPU6050(i2c)                                        #imu object

# Variables

count = 0         #counter for number of trips measured.
standing = True     #dieraction of the IMU measurement. true is deffined as standing up.
previous_value = True        #second check of direction. used to measure differences in directions

# Function

        # Function for detecting fall. compares measurements for if IMU output changes from 0 to 1.        
def fall_detect():
    global standing       #global values to access variable outside function.
    global previous_value
    global count
    
    # increase count if check1 and check2 are different. and not already fallen.
    if previous_value != standing and not standing:  
        count = count + 1
        print("fall counter: ", count)  #print fall count
    
    previous_value = standing
        

# Program 

while True:
    # reading values
    acceleration = imu.accel   #from Libary, measures acceleration on axis.
    gyroscope = imu.gyro       #from Libary, measures rotation and direction on axis.
    
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
    
    time.sleep(0.5)
