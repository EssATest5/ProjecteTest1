
##  FONT: https://www.digikey.es/en/maker/tutorials/2022/create-custom-characters-using-a-common-16x2-liquid-crystal-display?srsltid=AU7gw4Xo7YFZXrFTHImdTRMfMI7cskDilLgJmx0vWFYanQsfVCDefMkQ

import time
import RPi.GPIO as GPIO
import random
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24






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
# Variables per LCD
LCD_PAUSA = 0.001 #LCD_PAUSA = 0.02

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

def peripheral_setup () :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([RS,E,D4,D5,D6,D7],GPIO.OUT)
    GPIO.output([RS,E,D4,D5,D6,D7], 0)







# ------------------------------
# CARACTERS PERSONALITZATS BARRA
# ------------------------------

# Cada caracter ocupa 5 pixels d'amplada.
# Cada fila té 5 pixels útils.EL caracter nomès es veu 7 posicións però cal definir 8 docns la matriu es de 8x5
# 1 = pixel encès
# 0 = pixel apagat
# es fan servir els 5 bits de menor pes la resta es indiferent
# Creem 5 caracters: 1, 2, 3, 4 i 5 pixels d'amplada.
CARACTERS_BARRA = (
    (0b00010000, 0b00010000, 0b00010000, 0b00010000,
     0b00010000, 0b00010000, 0b00010000, 0b00010000),  # 1 pixel

    (0b00011000, 0b00011000, 0b00011000, 0b00011000,
     0b00011000, 0b00011000, 0b00011000, 0b00011000),  # 2 pixels

    (0b00011100, 0b00011100, 0b00011100, 0b00011100,
     0b00011100, 0b00011100, 0b00011100, 0b00011100),  # 3 pixels

    (0b00011110, 0b00011110, 0b00011110, 0b00011110,
     0b00011110, 0b00011110, 0b00011110, 0b00011110),  # 4 pixels

    (0b00011111, 0b00011111, 0b00011111, 0b00011111,
     0b00011111, 0b00011111, 0b00011111, 0b00011111)   # 5 pixels
)

def LCD_envia_byte(dada):
    # envia un byte ( 8 bits) 
    # Extreu els bits un a un desplaçancat cap a al dreta
    # Primer enviem els 4 bits ALTS
    LCD_escriu4bits(
        (dada >> 4) & 0x01,
        (dada >> 5) & 0x01,
        (dada >> 6) & 0x01,
        (dada >> 7) & 0x01
    )

    # Després enviem els 4 bits BAIXOS
    LCD_escriu4bits(
        dada & 0x01,
        (dada >> 1) & 0x01,
        (dada >> 2) & 0x01,
        (dada >> 3) & 0x01
    )


def LCD_crea_caracters_barra():
    """Carrega els 5 caracters de la barra a la CGRAM del LCD."""
    LCD_modecomandament(True)

    # CGRAM comença a l'adreça 0x40.
    # Cada caracter ocupa 8 bytes.
    for numero_caracter, caracter in enumerate(CARACTERS_BARRA):
        adreca = 0x40 + (numero_caracter * 8)

        LCD_envia_byte(adreca)

        for fila in caracter:
            LCD_modecomandament(False)
            LCD_envia_byte(fila)

        LCD_modecomandament(True)


def LCD_escriu_caracter_personalitzat(numero):
    """Escriu un dels caracters personalitzats 0..4."""
    LCD_modecomandament(False)
    LCD_envia_byte(numero)


def LCD_escriu_text(text):
    """Escriu text utilitzant l'ALFABET existent."""
    for caracter in text:
        if caracter in ALFABET:
            LCD_envia_dades_al_display(ALFABET[caracter])


def LCD_escriu_barra(valor, maxim):
    """
    Dibuixa la barra a la fila superior.

    valor = valor actual (per exemple, distancia en cm)
    maxim = valor que correspon a la barra completa

    La línia té 16 caracters x 5 pixels = 80 pixels.
    """
    if valor < 0:
        valor = 0

    if maxim <= 0:
        maxim = 1

    if valor > maxim:
        valor = maxim

    # Convertim el valor a 0..80 pixels.
    pixels = round((valor / maxim) * 80)

    LCD_escriu_a_fila_u()

    # 16 caracters, 5 pixels cadascun.
    caracters_complets = pixels // 5
    pixels_restants = pixels % 5

    # Caracters complets.
    for _ in range(caracters_complets):
        LCD_escriu_caracter_personalitzat(4)

    # Ultim caracter parcial, si n'hi ha.
    if pixels_restants > 0:
        # CGRAM 0..4 corresponen a 1..5 pixels.
        LCD_escriu_caracter_personalitzat(pixels_restants - 1)

    # Omplim la resta de la línia amb espais.
    for _ in range(16 - caracters_complets - (1 if pixels_restants > 0 else 0)):
        LCD_escriu_text(" ")

    # Tornem a la primera posició de la segona fila.
    LCD_escriu_a_fila_dos()

    
def LCD_mostra_dada_amb_barra(distancia):
    # La barra representa la distancia entre 0 i DISTANCIA_MAXIMA.
    global DISTANCIA_MAXIMA

    LCD_esborra_la_pantalla()

    if distancia != -1:
        # Primera fila: barra proporcional a la distancia.
        print(round(distancia))
        LCD_escriu_barra(round(distancia), DISTANCIA_MAXIMA)

        # Segona fila: valor numeric.
        LCD_escriu_text(f"{round(distancia,2)} CM")
    else:
        # Si no hi ha lectura, mantenim la barra buida.
        LCD_escriu_a_fila_u()
        LCD_escriu_text(" " * 16)

        LCD_escriu_a_fila_dos()
        LCD_escriu_text("NO DISPONIBLE")


################################# MAIN ###################################
try:
    peripheral_setup()
    
    DISTANCIA_MAXIMA = 400 #400 cm 
     
    
    LCD_inicia_pantalla()
    LCD_crea_caracters_barra()

    LCD_escriu_barra(100,200)
    exit()

    while True:

        distancia = random.randint(0,400)
        LCD_escriu_barra(33,400)
        #LCD_mostra_dada_amb_barra(distancia)
            
        time.sleep(0.5)
        
       

except KeyboardInterrupt:

    print("Finalitza programa")
    GPIO.cleanup()
