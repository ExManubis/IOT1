#########################################################################
# IMPORT
import umqtt_robust2 as mqtt
from machine import UART
from time import sleep
from gps_bare_minimum import GPS_Minimum
#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port
gps_speed = 9600                           # UART speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation
#########################################################################   
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
        
    # Stopper programmet når der trykkes Ctrl + c
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()