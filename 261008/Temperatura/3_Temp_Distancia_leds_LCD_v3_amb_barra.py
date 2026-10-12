#############################################################################
# 3_Temp+Distancia+leds+LCD_v3
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
#   08/10/26 : Afegim un sensor de temperatura. Ara el LCD mostrara la temperatura i l'humitat
#   09/10/26 : Mostra temperatura a linia u i humitat a linia dos
#   11/10/26 : Eliminació de ALFABET i reemplaç per funció que obte el ordinal del ASCII permutant els 4 bis superiors pels inferiors
#
#############################################################################

import RPi.GPIO as GPIO
import time
import threading
import Adafruit_DHT

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
#els de Sensor temperatura DHT11
SENSOR_TEMP = 6
MODEL_DHT = Adafruit_DHT.DHT11

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

# Variables Globals
# Variable compartida pels dos fils
distancia = -1 #incicialment infinit ( segons el meu codi)
DHT_humitat = 0.0
DHT_temp = 0.0

# Senyal compartit per indicar als fils que han de parar
aturar = threading.Event()


########################################################
#  Funcions per LCD
# Variables per LCD
LCD_PAUSA = 0.001 #LCD_PAUSA = 0.02

###Modificada de l'original que era un array de valors fitxes
#ordre dels bits per aquest LCD: b4,b5,b6,b7,b0,b1,b2,b3
def LCD_alfabet(cQuin_caracter):
    iTemp = ord(cQuin_caracter) #el numero ASCII amb 8 bits, en principi
    cResult = ((iTemp >> 4) & 1, (iTemp >> 5) & 1, (iTemp >> 6) & 1, (iTemp >> 7) & 1, iTemp & 1, (iTemp >> 1) & 1, (iTemp >> 2) & 1, (iTemp >> 3) & 1 )
    return cResult

# Caracters personalitzats per a la barra: codis 0..4 = 1..5 pixels.
CARACTERS_BARRA = (
    (0b00010000,) * 8,
    (0b00011000,) * 8,
    (0b00011100,) * 8,
    (0b00011110,) * 8,
    (0b00011111,) * 8
)

def LCD_envia_byte(valor, es_dada=False):
    GPIO.output(RS, GPIO.HIGH if es_dada else GPIO.LOW)
    LCD_escriu4bits((valor >> 4) & 1, (valor >> 5) & 1,
                    (valor >> 6) & 1, (valor >> 7) & 1)
    LCD_escriu4bits(valor & 1, (valor >> 1) & 1,
                    (valor >> 2) & 1, (valor >> 3) & 1)
    time.sleep(0.003 if (not es_dada and valor in (0x01, 0x02)) else 0.0001)

def LCD_comanda(valor):
    LCD_envia_byte(valor, False)

def LCD_dada(valor):
    LCD_envia_byte(valor, True)

def LCD_crea_caracters_barra():
    for numero, files in enumerate(CARACTERS_BARRA):
        LCD_comanda(0x40 | (numero * 8))
        for fila in files:
            LCD_dada(fila)

def LCD_mostra_barra(valor, maxim=400, linia=2):
    if maxim <= 0:
        raise ValueError("maxim ha de ser superior a zero")
    valor = max(0, min(valor, maxim))
    pixels = int(round((valor / maxim) * 80))
    LCD_esborra_linia(linia)
    LCD_posiciona_cursor(linia, 0)
    complets, restants = divmod(pixels, 5)
    for _ in range(complets):
        LCD_dada(4)
    if complets < 16 and restants:
        LCD_dada(restants - 1)
        complets += 1
    while complets < 16:
        LCD_dada(ord(' '))
        complets += 1

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
   # Seqüència d'inicialització del programa de prova que funciona.
   LCD_modecomandament(True)
   GPIO.output(E, GPIO.LOW)
   time.sleep(0.05)
   LCD_escriu4bits(1,1,0,0)
   time.sleep(0.005)
   LCD_escriu4bits(1,1,0,0)
   time.sleep(0.005)
   LCD_escriu4bits(1,1,0,0)
   time.sleep(0.001)
   LCD_escriu4bits(0,1,0,0)
   LCD_comanda(0x28)
   LCD_comanda(0x08)
   LCD_comanda(0x01)
   LCD_comanda(0x06)
   LCD_comanda(0x0C)

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
        LCD_envia_dades_al_display(LCD_alfabet(cadena[index]))
   
##/////// Aquestes son meves. No verifico error poso per defecte la 1
#----------------------------------------------------------------------------------
#    Posiciona el cursor del LCD. quina_linia: 1 o 2  columna: de 0 a 15
def LCD_posiciona_cursor(quina_linia, quina_columna):
    if (quina_columna<0) or (quina_columna >15): # per defecte es 0 
        quina_columna = 0 
        
    if quina_linia == 2: # Adreça inicial de cada línia Per defecte o valor erroni es la 1
        adreca = 0x40 + quina_columna
    else:
        adreca = 0x00 + quina_columna

    LCD_modecomandament(True)  # El que entrarem sera un comandament
    
    comanda = 0x80 | adreca
    # Enviar primer els 4 bits de més pes (bits 7..4)
    LCD_escriu4bits(
        (comanda >> 4) & 1,
        (comanda >> 5) & 1,
        (comanda >> 6) & 1,
        (comanda >> 7) & 1
    )

    # Enviar després els 4 bits de menys pes (bits 3..0)
    LCD_escriu4bits(
        (comanda >> 0) & 1,
        (comanda >> 1) & 1,
        (comanda >> 2) & 1,
        (comanda >> 3) & 1
    )

#   Esborra una linia
def LCD_esborra_linia(quina_linia):
    if (quina_linia<1) or ( quina_linia>2):
        quina_linia = 1 # per defecte la 1 en cas de error
        
    LCD_posiciona_cursor(quina_linia,0)
    for index in range(16):
        LCD_envia_dades_al_display(LCD_alfabet(' '))
    # Torna a posicionar al principi
    LCD_posiciona_cursor(quina_linia,0)
         

##  Envia una cadena a una linia 
def LCD_envia_Cadena_a_linia(cadena, quina_linia):
    if quina_linia == 2:
       LCD_esborra_linia(2) 
    else: # per defecte la 1
       LCD_esborra_linia(1)
        
    for index in range(len(cadena)):
        LCD_envia_dades_al_display(LCD_alfabet(cadena[index]))
        
#----------------------------------------------------------------------------------


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
def fluxe_mesura_distancia():
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
def fluxe_llums():
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
def fluxe_mesura_temp():
    global DHT_humitat, DHT_temp
    
    while not aturar.is_set():
        DHT_humitat, DHT_temp = Adafruit_DHT.read_retry(MODEL_DHT, SENSOR_TEMP)
        #print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(DHT_temp, DHT_humitat))
        time.sleep(2)
    
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

#////////////////////////////////////////////////////////////////////////////////
def DHT_inicia():
    global DHT_humitat, DHT_temp
    # femm una primera lectura que normalment es lenta. 
    DHT_humitat, DHT_temp = Adafruit_DHT.read_retry(MODEL_DHT, SENSOR_TEMP)
#////////////////////////////////////////////////////////////////////////////////

#/// M A I N ////////////////////////////////////////////////////////////////////
LCD_inicia_pantalla()
LCD_crea_caracters_barra()
LCD_envia_Cadena("Test en marxa...")
DHT_inicia() 
test_leds(10, 0.05) #cinc vegades i 0.1 temps

fil_distancia = threading.Thread(target=fluxe_mesura_distancia)
fil_llums = threading.Thread(target=fluxe_llums)
fil_temp = threading.Thread(target=fluxe_mesura_temp)

fil_distancia.start()
fil_llums.start()
fil_temp.start()

try:
    
    while True:
        # Codi per mostrar distancia al LCD
        time.sleep(1) # es pot posar pass perà llavors el bucle consumirà molta CPU
        if distancia!=-1:
            LCD_envia_Cadena_a_linia(f"Dst: {round(distancia,2)} cm",1 )
            LCD_mostra_barra(distancia, maxim=400, linia=2)
        else:
            LCD_envia_Cadena_a_linia("Dst: ?",1 )
            LCD_envia_Cadena_a_linia("No detecta...",2 )
        time.sleep(3)
        
        # Codi per mostrar temperatura i humitat
        LCD_envia_Cadena_a_linia(f"Temp: {DHT_temp} "+chr(223)+"C",1)
        LCD_envia_Cadena_a_linia(f"Hum : {DHT_humitat} %",2)
        time.sleep(3)

except KeyboardInterrupt: # Missatge de finalització
    print("Mesura aturada per l'usuari\n       Aturant el programa...")

    aturar.set()       # 1. Avisem els fils

    fil_distancia.join()       # 2. Esperem que acabi el fil 1
    fil_llums.join()       # 3. Esperem que acabi el fil 2
    fil_temp.join()

finally:
    LCD_esborra_la_pantalla()
    LCD_detencio_pantalla()
    GPIO.cleanup()     # 4. Alliberem els GPIO
    print("Programa finalitzat")