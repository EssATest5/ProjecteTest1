#!/usr/bin/env python3
# Prova mínima de 5 caràcters personalitzats per a un LCD 1602A
# GPIO BCM: RS=4, E=18, D4=27, D5=22, D6=23, D7=24

import RPi.GPIO as GPIO
import time

RS, E = 4, 18
D4, D5, D6, D7 = 27, 22, 23, 24
PAUSA = 0.001

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

    
def escriu4bits(b4, b5, b6, b7):
    GPIO.output(D4, b4)
    GPIO.output(D5, b5)
    GPIO.output(D6, b6)
    GPIO.output(D7, b7)
    time.sleep(PAUSA)
    GPIO.output(E, GPIO.HIGH)
    time.sleep(PAUSA)
    GPIO.output(E, GPIO.LOW)
    time.sleep(PAUSA)

def envia_byte(valor):
    # El LCD rep primer els bits 7..4 i després els bits 3..0.
    escriu4bits((valor >> 4) & 1, (valor >> 5) & 1,
                (valor >> 6) & 1, (valor >> 7) & 1)
    escriu4bits(valor & 1, (valor >> 1) & 1,
                (valor >> 2) & 1, (valor >> 3) & 1)

def comanda(valor):
    GPIO.output(RS, GPIO.LOW)
    envia_byte(valor)
    time.sleep(0.003 if valor in (0x01, 0x02) else 0.0001)

def dada(valor):
    GPIO.output(RS, GPIO.HIGH)
    envia_byte(valor)
    time.sleep(0.0001)

def inicialitza_lcd():
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.05)

    # Seqüència d'inicialització HD44780 en mode de 4 bits.
    escriu4bits(1, 1, 0, 0)
    time.sleep(0.005)
    escriu4bits(1, 1, 0, 0)
    time.sleep(0.005)
    escriu4bits(1, 1, 0, 0)
    time.sleep(0.001)
    escriu4bits(0, 1, 0, 0)

    comanda(0x28)  # 4 bits, 2 línies, matriu 5x8
    comanda(0x08)  # pantalla apagada durant configuració
    comanda(0x01)  # esborrar pantalla
    comanda(0x06)  # avançar cursor
    comanda(0x0C)  # pantalla encesa, cursor apagat

def crea_caracters_barra():
    for numero in range(5)
        #selecciona la adreça CGRAM del caracter
        files in enumerate(CARACTERS_BARRA):
        comanda(0x40 | (numero * 8))  # adreça CGRAM
        for fila in range(8):
            LCD_dada(CARACTERS_BARRA[numero][fila])

def mostra_caracter(numero):
    comanda(0x01)
    comanda(0x80)       # primera fila, primera columna
    dada(ord(str(numero)))
    dada(ord(':'))
    dada(numero)        # codi del caràcter personalitzat 0..4
    time.sleep(0.5)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([RS, E, D4, D5, D6, D7], GPIO.OUT, initial=GPIO.LOW)
    try:
        inicialitza_lcd()
        crea_caracters_barra()
        while True:
            for numero in range(5):
                mostra_caracter(numero)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
