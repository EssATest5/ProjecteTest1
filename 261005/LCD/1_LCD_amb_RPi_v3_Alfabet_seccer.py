#############################################################################
# 1_LCD_amb_RPi_v2
# Autor: Pedro J
# modificat: 
#	05/10/26 : creació
#
#
#############################################################################

import time
import RPi.GPIO as GPIO
RS = 4
E = 18
D4 = 27
D5 = 22
D6 = 23
D7 = 24
PAUSA = 0.02

########################################################
#L'espai està repetit. Les fletxes està malament el codi l l'esquerra surt dreta
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


FRASE =   " !  #  $  %  &     (  )  *  +  ,  -  .  /  0  1  2  3  4  5  6  7  8  9  :  ;  <  =  >  ?    @  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O    P  Q  R  S  T  U  V  W  X  Y  Z  [     ]  ^  _    '  a  b  c  d  e  f  g  h  i  j  k  l  m  n  o    p  q  r  s  t  u  v  w  x  y  z  {  |  }  >  -"


def modecomandament(valor):
    if valor == False:
         GPIO.output(RS, 1)  
    else:
         GPIO.output(RS,0)
    GPIO.output(E, 0)  
 
def escriu_a_fila_u():
     modecomandament(True)  # El que entrarem sera un comandament
     escriu4bits(0,0,0,0)   # Es posiciona el cursor a l'inici de la filera 1 
     escriu4bits(0,0,0,0)
  
def escriu_a_fila_dos():
     modecomandament(True) # El que entrarem sera un comandament
     escriu4bits(0,0,1,1)  # Es posiciona el cursor a l'inici de la filera 2 
     escriu4bits(0,0,0,0)
              
def escriu4bits(b1,b2,b3,b4):
     GPIO.output(D4, b1)
     GPIO.output(D5, b2)
     GPIO.output(D6, b3)
     GPIO.output(D7, b4)  
     time.sleep(PAUSA)
     GPIO.output(E, 1) 
     GPIO.output(E, 0)       
     time.sleep(PAUSA)

def peripheral_loop() :
    comptador = 0
    for index in range(len(FRASE)):
        if index % 16 == 0:
             if comptador % 2 == 0:
                esborra_la_pantalla()
                escriu_a_fila_u()
             else:
                escriu_a_fila_dos()
             comptador  += 1
        envia_dades_al_display(ALFABET[FRASE[index]])
    esborra_la_pantalla()
    
def esborra_la_pantalla():
    modecomandament(True)# El que entrarem sera un comandament
    time.sleep(PAUSA)
    escriu4bits(0,0,0,0) # Entrem el primer nibble del comandament esborrar pantalla
    escriu4bits(1,0,0,0) # Entrem el segon nibble del comandament esborrar pantalla
 
def envia_dades_al_display(dada):
    modecomandament(False) # El que entrarem sera un caracter per escriure en pantalla.
    escriu4bits(dada[0],dada[1],dada[2], dada[3]) 
    escriu4bits(dada[4],dada[5], dada[6], dada[7]) 
    #GPIO.output(RS, 0)
    #time.sleep(PAUSA)
  
def detencio_pantalla():
    modecomandament(True)# El que entrarem sera un comandament
    escriu4bits(0,0,0,0) # Entrem el Primer nibble del caracter a detencio_pantalla
    escriu4bits(0,0,1,1) # Entrem el Segon nibble del caracter a detencio_pantalla
   
def inicia_pantalla():
   modecomandament(True) # El que entrarem sera la sequencia d'inicializacio
   for index in range(3):
        escriu4bits(1,1,0,0)
   for index in range(2):
        escriu4bits(0,1,0,0)
   escriu4bits(1,0,1,1)   # Canvi a la sequencia inicialitzacio per habilitar dues fileres
   escriu4bits(0,0,0,0)
   escriu4bits(1,1,1,1)
   esborra_la_pantalla()

def peripheral_setup () :
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup([RS,E,D4,D5,D6,D7],GPIO.OUT)
    GPIO.output([RS,E,D4,D5,D6,D7], 0)

def main () :
    peripheral_setup()
    inicia_pantalla()

    while 1 :
        try:
            peripheral_loop()
        except KeyboardInterrupt:
            esborra_la_pantalla()
            detencio_pantalla()
            break

if __name__ == '__main__' :
    main()
