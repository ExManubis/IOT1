# IMPORTS
from machine import I2C, SoftI2C, UART, Pin, ADC
import sys
import uselect
import _thread
from gpio_lcd import GpioLcd
from time import sleep
import geofence as geo_f
from imu import MPU6050 #IMU Libary
from gps_bare_minimum import GPS_Minimum 
import umqtt_robust2 as mqtt #MQTT libary
import geofence as geof


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

# GPS + Geofence related variables:
gps_port = 2         # ESP32 UART port
gps_speed = 9600     # UART speed
gflat = 55.6918      #Geofence Lat defines lat center of Geofence circle 
gflon = 12.5546      #Geofence Lon defines lon center of Geofence circle
gfradius = 15        #Geofence radius in meter
#gps objects
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation

#IMU Related Objects
i2c = SoftI2C(scl = Pin(13), sda = Pin(14), freq =400000) #softI2C for custom pins
imu = MPU6050(i2c)                                        #imu object

# Fallcheck function related variables
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
        elif bat_pct < 100:
            lcd.clear()
            lcd.putstr('Battery: ' + str(bat_pct_int)+'%')
        elif bat_pct_int <5:
            sys.exit()
        sleep(60)

# Fall detection function
def fall_detect(): #function for IMU to detect fall
    global current_value  #global values to access variable outside function.
    global previous_value
    global count
    if previous_value != current_value and not current_value:  # increase count if check1 and check2 are different. and not already fallen.
        count = count + 1
        print("fall counter: ", count)  #print fall count
        ############################################################### NEED LCD PUTSTR HERE ##################################################
    previous_value = current_value

# IMU thread function
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
        
        sleep(0.5) #pause between measure

# Adafruit GPS function
def get_adafruit_gps():
    speed = lat = lon = None # Opretter variabler med None som værdi
    if gps.receive_nmea_data():
        # hvis der er kommet end bruggbar værdi på alle der skal anvendes
        if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            # gemmer returværdier fra metodekald i variabler
            speed =str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            # returnerer data med adafruit gps format der skal være 3 for at få den rigtige destination
            return speed + "," + lat + "," + lon + "," + "0.0"
        else: # hvis ikke både hastighed, latitude og longtitude er korrekte 
            print(f"GPS data to adafruit not valid:\nspeed: {speed}\nlatitude: {lat}\nlongtitude: {lon}")
            return False

def geo_measure():            #Function to measure if GPS position is within defined geofence
    lat1 = gps.get_latitude() 
    lon1 = gps.get_longitude()
    result = geof.inside_geofence(lat1, lon1, gflat, gflon, gfradius)
    if result == True:
        print("---------------Gps within geofence---------------")
    
    else:
        print("xxxxxxxxxxxxxxxx-GPS is outside geofence-xxxxxxxxxxxxxxxx")

"""
def adafruit_thread():
    while True:
        try:
            # Hvis funktionen returnere en string er den True ellers returnere den False
            gps_data = get_adafruit_gps()
            if gps_data: # hvis der er korrekt data så send til adafruit
                print(f'\ngps_data er: {gps_data}') # Printer GPS data
                mqtt.web_print(gps_data, 'storeK/feeds/Vest/csv') # Sender GPS data til adafruit
                
            sleep(4) # venter mere end 3 sekunder mellem hver besked der sendes til adafruit
            
            if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
                mqtt.besked = ""            
            mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
            print(".", end = '') # printer et punktum til shell, uden et enter
             
            geo_measure()
            

            
        # Stopper programmet når der trykkes Ctrl + c
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            mqtt.c.disconnect()
            mqtt.sys.exit()

"""

# PROGRAM

#threads
_thread.start_new_thread(bat_read_thread, ())
_thread.start_new_thread(imu_thread, ())
#_thread.start_new_thread(adafruit_thread, ())

while True:
    try:
        # Hvis funktionen returnere en string er den True ellers returnere den False
        gps_data = get_adafruit_gps()
        if gps_data: # hvis der er korrekt data så send til adafruit
            print(f'\ngps_data er: {gps_data}') # Printer GPS data
            mqtt.web_print(gps_data, 'storeK/feeds/Vest/csv') # Sender GPS data til adafruit 
        sleep(4) # venter mere end 3 sekunder mellem hver besked der sendes til adafruit
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        print(".", end = '') # printer et punktum til shell, uden et enter
         
        geo_measure()
        

        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()


