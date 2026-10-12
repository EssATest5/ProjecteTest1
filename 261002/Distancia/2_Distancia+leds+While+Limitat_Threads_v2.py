#############################################################################
# Distancia+leds+While+Limitat_Threads_v2
# Autor: Pedro J
# modificat: 
#	02/10/26 : creació
#   02/10/26 : Per evitar que si el sensor no respon es quedi bloquejat esperant resposta es modifica el codi
#               que envia i rep el puls
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
distancia = -1 #incicialment infinit ( segons el meu codi)

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()

#////////////////////////////////////////////////////////////////////////////////////
def mesura_distancia():
    global distancia
    
    limit_temps = False 
    while not aturar.is_set(): 
        limit_temps = False
        
        # Envia puls          
        GPIO.output(TRIG, True)
        time.sleep(0.00005)      # 10 micro segons, funciona amb molts retorns perduts
                                  # ho canvio a 50 i va molt millor
        GPIO.output(TRIG, False)

        # Esperem que ECHO passi de 0 a 1
        inici = time.time()
        while (GPIO.input(ECHO) == 0) and not limit_temps:
            limit_temps = ((time.time() - inici) > 0.03 ) #espera 3 centesimes
        start_time = time.time()
       
        if limit_temps: print("temps 1 superat") 
       
        while (GPIO.input(ECHO) == 1) and not limit_temps: # si es produeix un error 0 funcioan el sensor. es queda aquí bloquejat. Cal versió dos
            limit_temps = ((time.time() - start_time) > 0.03) #espera 3 centesimes
            if limit_temps: print("temps 2 superat")

        if not limit_temps:
            end_time = time.time()
            temps_total = end_time - start_time
            distancia = (temps_total * 34300) / 2  # Resultat en cm
        else:
            distancia = -1

        time.sleep(0.1) #mesura cada 100ms
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
def llums():
    global distancia

    while not aturar.is_set():
        #print(distancia)
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

        time.sleep(0.1) #actualitza cada 100ms
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
# test de leds
def test_leds():
    LEDs = [LED1, LED2, LED3]

    for i in range(3):
        for led in LEDs:
            GPIO.output(led, 1)
        time.sleep(0.1)

        for led in LEDs:
            GPIO.output(led, 0)
        time.sleep(0.1)
#////////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////
test_leds()

fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=llums)

fil_1.start()
fil_2.start()

try:

    while True:
        time.sleep(1) # es pot posar pass perà llavors el bucle consumirà molta CPU

except KeyboardInterrupt: # Missatge de finalització
    
    print("Mesura aturada per l'usuari\n       Aturant el programa...")

    aturar.set()       # 1. Avisem els fils

    fil_1.join()       # 2. Esperem que acabi el fil 1
    fil_2.join()       # 3. Esperem que acabi el fil 2

finally:
    GPIO.cleanup()     # 4. Alliberem els GPIO
    print("Programa finalitzat")