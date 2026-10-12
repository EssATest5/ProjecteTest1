#############################################################################
# Leds_3_threads
#Autor: Pedro J
#modificat: 
#	28/09/26 : creació
#	Eliminem la pausa del sleep() i ho fem amb treaths
#############################################################################

####################  OJO a PROTEUS no FUNCIONA EL MULTITHREADING NI MULTIPROCESSING

import RPi.GPIO as GPIO
from time import sleep, time
import threading

# Definim el pin utilitzant la numeració GPIO (BCM)
led_D1  = 17
led_D2  = 25

interval_D1 = 3
interval_D2 = 0.3


# Configuració dels pins
GPIO.setmode(GPIO.BCM)       # Fes servir  la numeració de Broadcom (GPIO)
GPIO.setup( [led_D1,led_D2],  GPIO.OUT) # Configura el pins com a sortida . Des de una llista de pins


#print("El pin està parpellejant... Prem Ctrl+C per sortir.")
#////////////////////////////////////////////////////////////////////////////////////
def blink_D1():

	while True:
		GPIO.output(led_D1, not(GPIO.input(led_D1) ))
		sleep(interval_D1)
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
def blink_D2():

	while True:
		GPIO.output(led_D2, not(GPIO.input(led_D2) ))
		sleep(interval_D2)
#////////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////
try:
	
	
		fil_1 = threading.Thread(target=blink_D1)
		fil_2 = threading.Thread(target=blink_D2)
		
		fil_1.start()
		fil_2.start()
		
		fil_1.join()
		fil_2.join()

except KeyboardInterrupt:
		print("\nAturant el programa...")
finally:
		GPIO.cleanup() # Neteja la configuració dels pins al sortir
		print("Pins alliberats correctament.")


