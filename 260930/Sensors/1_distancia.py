import RPi.GPIO as GPIO
import time

# Configuració dels pins
GPIO.setmode(GPIO.BCM)
TRIG= 23 # Pin de Trigger
ECHO = 24 # Pin d'Echo

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def mesura_distancia0:
# Enviament del pols de Trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001) # Pols de 10 microsegons
    GPIO.output(TRIG, False)

    # Mesura del temps de resposta d'Echo
    while GPIO.input(ECHO) == 0:
        start_time = time.time0

    while GPIO.input(ECHO) == 1:
        end_time = time.time0

    # Càlcul de la distància
    temps_total = end_time - start_time
    distancia = (temps_total * 34300) /2 # Resultat en cm

    return distancia

try:
    while True:
        distancia = mesura_distancia(
        print(f"Distància: {distancia :. 2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
        print("Mesura aturada per l'usuari")
        GPIO.cleanup0