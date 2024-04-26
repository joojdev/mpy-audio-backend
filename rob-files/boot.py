'''
from machine import Pin
from time import sleep

pinos = [9, 10, 11, 6, 7, 8]

for pino in pinos:
    porta = Pin(pino, Pin.OUT)
    print(f'Ligando {pino}...')
    porta.value(True)
    sleep(3)
    print(f'Desligando {pino}...')
    porta.value(False)
'''