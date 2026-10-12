#############################################################################
# Sensor_distancia_amb_leds_threads_v1
# Autor: Pedro J
# modificat: 
#	02/10/26 : creació
#	Afegim leds segons distancia.
#############################################################################

import RPi.GPIO as GPIO
import time
import threading

# Definim el pin utilitzant la numeració GPIO (BCM)
GPIO.setmode(GPIO.BCM)

LED1 = 12
LED2 = 13
LED3 = 16
TRIG = 17
ECHO = 25

GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Variable compartida pels dos fils
distancia = 0

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()

#////////////////////////////////////////////////////////////////////////////////////
def mesura_distancia():
    global distancia

    while  not aturar.is_set():

        GPIO.output(TRIG, True)
        time.sleep(0.00001)      # 10 micro segons
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
        
        start_time = time.time()

        while GPIO.input(ECHO) == 1: # si es produeix un error 0 funcioan el sensor. es queda aquí bloquejat. Cal versió dos
        
        end_time = time.time()

        temps_total = end_time - start_time
        distancia = (temps_total * 34300) / 2  # Resultat en cm

        time.sleep(0.1) #mesura cada 100ms
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
def llums():
    global distancia

    while  not aturar.is_set():

        if 0 <= distancia <= 20:
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 0)
            GPIO.output(LED3, 0)

        if 20 < distancia <= 50:
            GPIO.output(LED1, 0)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 0)

        if 50 < distancia <= 400:
            GPIO.output(LED1, 0)
            GPIO.output(LED2, 0)
            GPIO.output(LED3, 1)

        if distancia < 0 or distancia > 400:
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 1)

        time.sleep(0.1) #actualitza cada 100ms
#////////////////////////////////////////////////////////////////////////////////////


#/// M A I N ////////////////////////////////////////////////////////////////////
fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=llums)

fil_1.start()
fil_2.start()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt: # Missatge de finalització
    
    print("Mesura aturada per l'usuari\nAturant el programa...")

    aturar.set()       # 1. Avisem els fils

    fil_1.join()       # 2. Esperem que acabi el fil 1
    fil_2.join()       # 3. Esperem que acabi el fil 2

finally:
    GPIO.cleanup()     # 4. Alliberem els GPIO
    print("Programa finalitzat")