import network
import time
from machine import Pin
from time import sleep
from speaker import play_wav
from requesting import fetch_audio
import os

ssid = 'IoT'
password = 'iot@2023'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

if not sta_if.isconnected():
    sta_if.disconnect()
    sta_if.connect('IoT', 'iot@2023')

    print(f'Conectando na rede {ssid}...', end='')

    while not sta_if.isconnected():
        print('.', end='')
        time.sleep(1)

    print('')
    print(f'Conectado com sucesso na rede {ssid}!')

play_wav('success.wav', 25)

def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

playing = False

def handle_interrupt(pin, prompt):
    pin.irq(handler=None)
    global playing
    if not playing:
        playing = True
        
        if not fetch_audio(prompt):
            play_wav('error.wav', 25)
        else:
            play_wav('audio.wav', 25)
            
        pin.irq(trigger=Pin.IRQ_RISING, handler=lambda _ : handle_interrupt(pin, prompt))
        playing = False
        
#def play_sound(pin):
#    pin.irq(handler=None)
#    play_wav('music.wav', 25)

button1 = Pin(14, Pin.IN)
#button1.irq(trigger=Pin.IRQ_RISING, handler=play_sound)
button1.irq(trigger=Pin.IRQ_RISING, handler=lambda _ : handle_interrupt(button1, 'Me conte uma piada engraçada.'))

button2 = Pin(15, Pin.IN)
button2.irq(trigger=Pin.IRQ_RISING, handler=lambda _ : handle_interrupt(button2, 'Me faça um poema.'))
