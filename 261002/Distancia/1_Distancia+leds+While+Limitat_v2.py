#############################################################################
# Distancia+leds+While+Limitat_v2
# Autor: Pedro J
# modificat: 
#	01/10/26 : creació
#   02/10/26 : Per evitar que si el sensor no respon es quedi bloquejat esperant resposta es modifica el codi
#               que envia i rep el puls
#	Afegim leds segons distancia.
#############################################################################


import RPi.GPIO as GPIO
import time

# Definim el pin utilitzant la numeració GPIO (BCM)
GPIO.setmode(GPIO.BCM)

LED1 = 12
LED2 = 13
LED3 = 16
TRIG = 17
ECHO = 25

GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

#////////////////////////////////////////////////////////////////////////////////////
def mesura_distancia():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)      # 10 micro segons
    GPIO.output(TRIG, False)

    # Esperem que ECHO passi de 0 a 1
    inici = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - inici > 0.03: #espera 3 centesimes
            return -1

    start_time = time.time()

    while GPIO.input(ECHO) == 1: # si es produeix un error 0 funcioan el sensor. es queda aquí bloquejat. Cal versió dos
        if time.time() - start_time > 0.03:
            return -1

    end_time = time.time()

    temps_total = end_time - start_time
    distancia = (temps_total * 34300) / 2  # Resultat en cm
    return distancia
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# test de leds
def test_leds():
    LEDs = [LED1, LED2, LED3]

    for i in range(3):
        for led in LEDs:
            GPIO.output(led, 1)
        time.sleep(0.3)

        for led in LEDs:
            GPIO.output(led, 0)
        time.sleep(0.3)
#////////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////

test_leds()

try:
    while True:
        distancia = mesura_distancia()
        print(distancia)
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

        if distancia < 0 or distancia > 400: # si no ha pogut mesurar retorna -1
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 1)

        time.sleep(1)

except KeyboardInterrupt: # Missatge de finalització
        print("Mesura aturada per l'usuari\n       Aturant el programa...")
finally:
        GPIO.cleanup() # Neteja la configuració dels pins al sortir
        print("Pins alliberats correctament.")
