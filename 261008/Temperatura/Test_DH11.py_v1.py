
#############################################################################
# 1_Distancia+leds+LCD_v1
# Autor: Pedro J
# modificat: 
#	02/10/26 : creació
#   02/10/26 : Per evitar que si el sensor no respon es quedi bloquejat esperant resposta es modifica el codi
#               que envia i rep el puls
#	            Afegim leds segons distancia.
#   05/10/26 : Per verificar que durant una no detecció no es quedi en blocle aturat , en cas que no detecti res o estigui sempre detectant, els led faran pampallugues
#              per això poso un parametre a la funció test_leds que indica quantes panpallugues i frequencia
#               Tampe s'introdueix la funció echo_timeout(estat) per evitar duplicitat de codi en esperes de recpció del pols
#   06/10/26 : Afegim les funcions del LCD per mostrar per pantalla el missatge de distancia.
#   07/10/26 : Integrat tot amb threats. Modificacions de depuració
#
#############################################################################

import RPi.GPIO as GPIO
import sys
import Adafruit_DHT

sensor = 11
pin = 6


try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        
except KeyboardInterrupt:
    print(" Aturant el programa...")
    
finally: 
    GPIO.cleanup()     # 4. Alliberem els GPIO
    