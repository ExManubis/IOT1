"""
IMU software for measuring times the Axis of the gyroscope is changed from upright Y axis.
the software measures the direction of the axis and saves it in variables to compare the states.
Then it counts the times that the axis have been changed from the Standing possision.

The Y axis pointing up is deffined as the "standing up straight" for the pourouses of mounting the
IMU unto a wearable device.

©Alexis Fredegaard 
Date: 27 october 2023
alexisfredegaard@gmail.com
"""

###########################################################################################
#Import block

from imu import MPU6050  # IMU libary from https://github.com/micropython-IMU/micropython-mpu9x50
import time
from machine import Pin, I2C, SoftI2C

###########################################################################################
#objects

i2c = SoftI2C(scl = Pin(12), sda = Pin(14), freq =400000) #softI2C for custom pins
imu = MPU6050(i2c)                                        #imu object

###########################################################################################
#variables

count = 0         #counter for number of trips measured.
standing = True     #dieraction of the IMU measurement. true is deffined as standing up.
current_value = True        #first check of direction. used to measure differences in directions
previous_value = True        #second check of direction. used to measure differences in directions

###########################################################################################
#function

#function for detecting fall. compares measurements for if IMU output changes from 0 to 1.        
def fall_detect():
    global current_value  #global values to access variable outside function.
    global previous_value
    global count
    
    if previous_value != current_value and not current_value:  # increase count if check1 and check2 are different. and not already fallen.
        #print("check1 :", check1, " check2: ", check2)
        count = count + 1
        print("fall counter: ", count)  #print fall count
    
    previous_value = current_value
        

#################################### {Main Code Block} ####################################

while True:
    # reading values
    acceleration = imu.accel   #from Libary, measures acceleration on axis.
    gyroscope = imu.gyro       #from Libary, measures rotation and direction on axis.
    
    """print ("Acceleration x: ", round(acceleration.x,2), " y:", round(acceleration.y,2),
           "z: ", round(acceleration.z,2))
           
    print ("gyroscope x: ", round(gyroscope.x,2), " y:", round(gyroscope.y,2),
           "z: ", round(gyroscope.z,2))
    """
    
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

# data interpretation (gyroscope)

#    if abs(gyroscope.x) > 20:
#        print("Rotation around the x axis")

#    if abs(gyroscope.y) > 20:
#        print("Rotation around the y axis")

#    if abs(gyroscope.z) > 20:
#        print("Rotation around the z axis")
    
    time.sleep(0.5)
###########################################################################################
