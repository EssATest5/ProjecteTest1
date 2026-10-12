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
import time
import threading

# Definicio de PINS
LED1 = 12
LED2 = 13
LED3 = 16
# del Sendosr de distancia 
TRIG = 17
ECHO = 25
# Els del LCD
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24

# Configuració dels PINS
GPIO.setmode(GPIO.BCM)
#     dels LEDS i Sensor distància
GPIO.setup([TRIG, LED1, LED2, LED3], GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
#     del LCD
GPIO.setwarnings(False)
GPIO.setup([RS,E,D4,D5,D6,D7],GPIO.OUT)
GPIO.output([RS,E,D4,D5,D6,D7], 0)

#definició de temps
durada_puls = 0.00010     # 10 micro segons, funciona amb molts retorns perduts
                          # ho canvio a 50 i va molt millor
durada_timeout_retorn = 0.03      #temp que si se supera es que no es reb el echo

# Variable compartida pels dos fils
distancia = -1 #incicialment infinit ( segons el meu codi)

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()

########################################################
# Variables per LCD
LCD_PAUSA = 0.005 #LCD_PAUSA = 0.02
########################################################
#L'espai està repetit.
ALFABET = {
               " ":(0,1,0,0,0,0,0,0),
               "!":(0,1,0,0,1,0,0,0),
              "\"":(0,1,0,0,0,1,0,0),
               "#":(0,1,0,0,1,1,0,0),
               "$":(0,1,0,0,0,0,1,0),
               "%":(0,1,0,0,1,0,1,0),
               "&":(0,1,0,0,0,1,1,0),
               " ":(0,1,0,0,1,1,1,0),
               "(":(0,1,0,0,0,0,0,1),
               ")":(0,1,0,0,1,0,0,1),
               "*":(0,1,0,0,0,1,0,1),
               "+":(0,1,0,0,1,1,0,1),
               ",":(0,1,0,0,0,0,1,1),
               "-":(0,1,0,0,1,0,1,1),
               ".":(0,1,0,0,0,1,1,1),
               "/":(0,1,0,0,1,1,1,1),
               

               "0":(1,1,0,0,0,0,0,0),
               "1":(1,1,0,0,1,0,0,0),
               "2":(1,1,0,0,0,1,0,0),
               "3":(1,1,0,0,1,1,0,0),
               "4":(1,1,0,0,0,0,1,0),
               "5":(1,1,0,0,1,0,1,0),
               "6":(1,1,0,0,0,1,1,0),
               "7":(1,1,0,0,1,1,1,0),
               "8":(1,1,0,0,0,0,0,1),
               "9":(1,1,0,0,1,0,0,1),
               ":":(1,1,0,0,0,1,0,1),
               ";":(1,1,0,0,1,1,0,1),
               "<":(1,1,0,0,0,0,1,1),
               "=":(1,1,0,0,1,0,1,1),
               ">":(1,1,0,0,0,1,1,1),
               "?":(1,1,0,0,1,1,1,1),

               "@":(0,0,1,0,0,0,0,0),
               "A":(0,0,1,0,1,0,0,0),
               "B":(0,0,1,0,0,1,0,0),
               "C":(0,0,1,0,1,1,0,0),
               "D":(0,0,1,0,0,0,1,0),
               "E":(0,0,1,0,1,0,1,0),
               "F":(0,0,1,0,0,1,1,0),
               "G":(0,0,1,0,1,1,1,0),
               "H":(0,0,1,0,0,0,0,1),
               "I":(0,0,1,0,1,0,0,1),
               "J":(0,0,1,0,0,1,0,1),
               "K":(0,0,1,0,1,1,0,1),
               "L":(0,0,1,0,0,0,1,1),
               "M":(0,0,1,0,1,0,1,1),
               "N":(0,0,1,0,0,1,1,1),
               "O":(0,0,1,0,1,1,1,1),

               "P":(1,0,1,0,0,0,0,0),
               "Q":(1,0,1,0,1,0,0,0),
               "R":(1,0,1,0,0,1,0,0),
               "S":(1,0,1,0,1,1,0,0),
               "T":(1,0,1,0,0,0,1,0),
               "U":(1,0,1,0,1,0,1,0),
               "V":(1,0,1,0,0,1,1,0),
               "W":(1,0,1,0,1,1,1,0),
               "X":(1,0,1,0,0,0,0,1),
               "Y":(1,0,1,0,1,0,0,1),
               "Z":(1,0,1,0,0,1,0,1),
               "[":(1,0,1,0,1,1,0,1),
               " ":(0,1,0,0,0,0,0,0),
               "]":(1,0,1,0,1,0,1,1),
               "^":(1,0,1,0,0,1,1,1),
               "_":(1,0,1,0,1,1,1,1),

               "'":(0,1,1,0,0,0,0,0),
               "a":(0,1,1,0,1,0,0,0),
               "b":(0,1,1,0,0,1,0,0),
               "c":(0,1,1,0,1,1,0,0),
               "d":(0,1,1,0,0,0,1,0),
               "e":(0,1,1,0,1,0,1,0),
               "f":(0,1,1,0,0,1,1,0),
               "g":(0,1,1,0,1,1,1,0),
               "h":(0,1,1,0,0,0,0,1),
               "i":(0,1,1,0,1,0,0,1),
               "j":(0,1,1,0,0,1,0,1),
               "k":(0,1,1,0,1,1,0,1),
               "l":(0,1,1,0,0,0,1,1),
               "m":(0,1,1,0,1,0,1,1),
               "n":(0,1,1,0,0,1,1,1),
               "o":(0,1,1,0,1,1,1,1),

               "p":(1,1,1,0,0,0,0,0),
               "q":(1,1,1,0,1,0,0,0),
               "r":(1,1,1,0,0,1,0,0),
               "s":(1,1,1,0,1,1,0,0),
               "t":(1,1,1,0,0,0,1,0),
               "u":(1,1,1,0,1,0,1,0),
               "v":(1,1,1,0,0,1,1,0),
               "w":(1,1,1,0,1,1,1,0),
               "x":(1,1,1,0,0,0,0,1),
               "y":(1,1,1,0,1,0,0,1),
               "z":(1,1,1,0,0,1,0,1),
               "{":(1,1,1,0,1,1,0,1),
               "|":(1,1,1,0,0,0,1,1),
               "}":(1,1,1,0,1,0,1,1),
               "→":(1,1,1,0,0,1,1,1),
               "←":(1,1,1,0,1,1,1,1)
               
               }
########################################################

########################################################
#  Funcions per LCD
def LCD_modecomandament(valor):
    GPIO.output(RS, not(valor) )
    GPIO.output(E, 0)
    
def LCD_escriu4bits(b1,b2,b3,b4):
     GPIO.output(D4, b1)
     GPIO.output(D5, b2)
     GPIO.output(D6, b3)
     GPIO.output(D7, b4)  
     time.sleep(LCD_PAUSA)
     GPIO.output(E, 1) 
     GPIO.output(E, 0)       
     time.sleep(LCD_PAUSA)

def LCD_escriu_a_fila_u():
     LCD_modecomandament(True)  # El que entrarem sera un comandament
     LCD_escriu4bits(0,0,0,0)   # Es posiciona el cursor a l'inici de la filera 1 
     LCD_escriu4bits(0,0,0,0)
  
def LCD_escriu_a_fila_dos():
     LCD_modecomandament(True) # El que entrarem sera un comandament
     LCD_escriu4bits(0,0,1,1)  # Es posiciona el cursor a l'inici de la filera 2 
     LCD_escriu4bits(0,0,0,0)

def LCD_esborra_la_pantalla():
    LCD_modecomandament(True)# El que entrarem sera un comandament
    time.sleep(LCD_PAUSA)
    LCD_escriu4bits(0,0,0,0) # Entrem el primer nibble del comandament esborrar pantalla
    LCD_escriu4bits(1,0,0,0) # Entrem el segon nibble del comandament esborrar pantalla

def LCD_detencio_pantalla():
    LCD_modecomandament(True)# El que entrarem sera un comandament
    LCD_escriu4bits(0,0,0,0) # Entrem el Primer nibble del caracter a LCD_detencio_pantalla
    LCD_escriu4bits(0,0,1,1) # Entrem el Segon nibble del caracter a LCD_detencio_pantalla

def LCD_inicia_pantalla():
   LCD_modecomandament(True) # El que entrarem sera la sequencia d'inicializacio
   for index in range(3):
        LCD_escriu4bits(1,1,0,0)
   for index in range(2):
        LCD_escriu4bits(0,1,0,0)
   LCD_escriu4bits(1,0,1,1)   # Canvi a la sequencia inicialitzacio per habilitar dues fileres
   LCD_escriu4bits(0,0,0,0)
   LCD_escriu4bits(1,1,1,1)
   LCD_esborra_la_pantalla()

def LCD_envia_dades_al_display(dada):
    LCD_modecomandament(False) # El que entrarem sera un caracter per escriure en pantalla.
    LCD_escriu4bits(dada[0],dada[1],dada[2], dada[3]) 
    LCD_escriu4bits(dada[4],dada[5], dada[6], dada[7]) 

## Aquesta es meva
def LCD_envia_Cadena(cadena) :
    comptador = 0
    LCD_esborra_la_pantalla()
    for index in range(len(cadena)):
        if index % 16 == 0:
             if comptador % 2 == 0:
                LCD_esborra_la_pantalla()
                LCD_escriu_a_fila_u()
             else:
                LCD_escriu_a_fila_dos()
             comptador  += 1
        LCD_envia_dades_al_display(ALFABET[cadena[index]])

########################################################


#////////////////////////////////////////////////////////////////////////////////////
def echo_timeout (estat) :
    inici = time.time()

    while GPIO.input (ECHO) == estat:
        if time. time() - inici > durada_timeout_retorn:
            return True

    return False
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
def mesura_distancia():
    global distancia
    
    while not aturar.is_set(): 
        limit_temps = False
        
        # Envia puls          
        GPIO.output(TRIG, True)
        time.sleep(durada_puls)  
        GPIO.output(TRIG, False)

        # Esperem que ECHO passi de 0 a 1
        if echo_timeout (0) :
            distancia = -1

        else:
            start_time = time.time()

            # Esperem que ECHO passi de 1 a 0
            if echo_timeout (1) :
                distancia = -1

            else:
                end_time = time.time()

                temps_total = end_time - start_time
                distancia = (temps_total * 34300) / 2

        time.sleep(0.1) #mesura cada 100ms
#////////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////////
def llums_i_LCD():
    global distancia

    while not aturar.is_set():
        # Actualitza LEDS        
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

        if distancia > 400: # si no ha pogut mesurar retorna -1
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 1)

        if distancia < 0: # si no ha pogut mesurar retorna -1
            GPIO.output(LED1, 1)
            GPIO.output(LED2, 1)
            GPIO.output(LED3, 1)

        #time.sleep(0.1) #actualitza cada 100ms
        time.sleep(0.5) 
#////////////////////////////////////////////////////////////////////////////////

#////////////////////////////////////////////////////////////////////////////////
# test de leds
def test_leds(vegades, frequencia):
    LEDs = [LED1, LED2, LED3]

    for i in range(vegades):
        for led in LEDs:
            GPIO.output(led, 1)
        time.sleep(frequencia)

        for led in LEDs:
            GPIO.output(led, 0)
        time.sleep(frequencia)
#////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////
LCD_inicia_pantalla()
LCD_envia_Cadena("Test en marxa...")
test_leds(10, 0.05) #cinc vegades i 0.1 temps


fil_1 = threading.Thread(target=mesura_distancia)
fil_2 = threading.Thread(target=llums_i_LCD)

fil_1.start()
fil_2.start()

try:
    
    while True:
        time.sleep(1) # es pot posar pass perà llavors el bucle consumirà molta CPU
        if distancia!=-1:
            LCD_envia_Cadena("Dst: "+str(round(distancia,2)))
        else:
            LCD_envia_Cadena("No detecta..." )   

except KeyboardInterrupt: # Missatge de finalització
    
    print("Mesura aturada per l'usuari\n       Aturant el programa...")

    aturar.set()       # 1. Avisem els fils

    fil_1.join()       # 2. Esperem que acabi el fil 1
    fil_2.join()       # 3. Esperem que acabi el fil 2

finally:
    LCD_esborra_la_pantalla()
    LCD_detencio_pantalla()
    GPIO.cleanup()     # 4. Alliberem els GPIO
    print("Programa finalitzat")