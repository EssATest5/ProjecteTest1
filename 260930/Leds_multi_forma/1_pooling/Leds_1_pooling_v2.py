#############################################################################
# Leds_1_pooling_v2 Amb funcions
#Autor: Pedro J
#modificat: 
#	28/09/26 : creació
#	Afegint procediments
#############################################################################


import RPi.GPIO as GPIO
from time import sleep

# Definim el pin utilitzant la numeració GPIO (BCM)
led_D1  = 17
led_D2  = 25
pausa = 1


# Configuració dels pins
GPIO.setmode(GPIO.BCM)       # Fes servir  la numeració de Broadcom (GPIO)
GPIO.setup( [led_D1,led_D2],  GPIO.OUT) # Configura el pins com a sortida . Des de una llista de pins


#print("El pin està parpellejant... Prem Ctrl+C per sortir.")
#////////////////////////////////////////////////////////////////////////////////////
def set_estat(estatD1, estatD2, temps):

	GPIO.output(led_D1, estatD1)
	GPIO.output(led_D2, estatD2)

	sleep(temps)
#////////////////////////////////////////////////////////////////////////////////////

try:
	while True:
		set_estat(GPIO.HIGH, GPIO.LOW, pausa) # Envia corrent (encén)
		set_estat(GPIO.LOW, GPIO.HIGH, pausa)

except KeyboardInterrupt:
		print("\nAturant el programa...")
finally:
		GPIO.cleanup() # Neteja la configuració dels pins al sortir
		print("Pins alliberats correctament.")


