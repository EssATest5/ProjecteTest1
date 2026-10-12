#############################################################################
# Sensor_distancia_v1
# Autor: Pedro J
# modificat: 
#	30/09/26 : creació per sensor distancia HC-SR04
#	
#############################################################################

import RPi.GPIO com a GPIO
import temps

# Definim el pin utilitzant la numeració GPIO (BCM)
GPIO.setmode(GPIO.BCM)
TRIG=17
ECHO = 25

GPIO.setup(TRIG GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#////////////////////////////////////////////////////////////////////////////////////
def mesura_distancia():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)      # 10 micro segons
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:  
    
    start_time = time.time()

    while GPIO.input(ECHO) == 1: # si es produeix un error 0 funcioan el sensor. es queda aquí bloquejat. Cal versió dos
    
    end_time = time.time()

    temps_total = end_time - start_time
    distancia = (temps_total * 34300)/2 # Resultat en cm

    return distancia
#////////////////////////////////////////////////////////////////////////////////////


#/// M A I N ////////////////////////////////////////////////////////////////////
try:
    while True:
        distancia = mesura_distancia()
        print(f"Distància: (distància:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt # Missatge de finalització
        print("Mesura aturada per l'usuari\nAturant el programa...")
finally:
        GPIO.cleanup() # Neteja la configuració dels pins al sortir
        print("Pins alliberats correctament.")
