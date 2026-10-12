#############################################################################
# Leds_2_time_slicing
#Autor: Pedro J
#modificat: 
#	28/09/26 : creació
#	Eliminem la pausa del sleep() i introduim Time Slicing
#############################################################################


import RPi.GPIO as GPIO
from time import sleep, time

# Definim el pin utilitzant la numeració GPIO (BCM)
led_D1  = 17
led_D2  = 25

interval_D1 = 2
interval_D2 = 0.2

darrer_temps_D1 = time() # Captura el temps actual pel diode D1
darrer_temps_D2 = time() # Captura el temps actual pel diode D2



# Configuració dels pins
GPIO.setmode(GPIO.BCM)       # Fes servir  la numeració de Broadcom (GPIO)
GPIO.setup( [led_D1,led_D2],  GPIO.OUT) # Configura el pins com a sortida . Des de una llista de pins


#print("El pin està parpellejant... Prem Ctrl+C per sortir.")
#////////////////////////////////////////////////////////////////////////////////////
def actualitza_estat():

	ara_temps  = time()
	global darrer_temps_D1
	global darrer_temps_D2
	if  (ara_temps - darrer_temps_D1) >= interval_D1:
		GPIO.output(led_D1, not(GPIO.input(led_D1) ))
		darrer_temps_D1 = ara_temps

	if  (ara_temps - darrer_temps_D2) >= interval_D2:
		GPIO.output(led_D2, not(GPIO.input(led_D2) ))
		darrer_temps_D2 = ara_temps


#////////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////
try:
	
	darrer_temps_D1 = time() # Captura el temps actual pel diode D1
	darrer_temps_D2 = time() # Captura el temps actual pel diode D2

	while True:
		actualitza_estat() # Envia corrent (encén)

		sleep(0.01) #per no tornar boja la CPU

except KeyboardInterrupt:
		print("\nAturant el programa...")
finally:
		GPIO.cleanup() # Neteja la configuració dels pins al sortir
		print("Pins alliberats correctament.")


