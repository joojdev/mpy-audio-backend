from machine import Pin, PWM
import time

class Speaker:
    def __init__(self, speaker_pin, duty):
        # Inicializa o pino do alto-falante como um pino de PWM e armazena o ciclo de trabalho.
        self.speaker_pin = PWM(Pin(speaker_pin))
        self.duty = duty
        
        # Define uma lista de notas musicais com suas respectivas frequências.
        self.notes = [('do', 264), ('re', 300), ('mi', 330), ('fa', 352), 
                      ('sol', 396), ('la', 440), ('si', 495)]

    def play(self, note, duration=0.2):
        # Encontra a frequência para a nota fornecida.
        for name, freq in self.notes:
            if name == note:
                # Configura a frequência e o ciclo de trabalho para o PWM.
                self.speaker_pin.freq(freq)
                self.speaker_pin.duty(self.duty)
                # Toca a nota por 80% da duração.
                time.sleep(duration * 0.8)
                self.speaker_pin.duty(0)  # Silencia o alto-falante temporariamente
                time.sleep(duration * 0.2)
                break

if __name__ == '__main__':
    speaker = Speaker(25, 2)  # Define o pino 25 para o alto-falante com um ciclo de trabalho de 50%
    
    # Toca uma sequência de notas
    speaker = Speaker(25, 2)
    speaker.play('do')
    speaker.play('re')
    speaker.play('mi')
    speaker.play('fa')
    time.sleep(0.2)
    speaker.play('fa')
    speaker.play('fa')
    time.sleep(0.3)
    speaker.play('do')
    speaker.play('re')
    speaker.play('do')
    speaker.play('re')
    time.sleep(0.2)
    speaker.play('re')
    speaker.play('re')
    time.sleep(0.3)
    speaker.play('do')
    speaker.play('sol')
    speaker.play('fa')
    speaker.play('mi')
    time.sleep(0.2)
    speaker.play('mi')
    speaker.play('mi')
    time.sleep(0.3)
    speaker.play('do')
    speaker.play('re')
    speaker.play('mi')
    speaker.play('fa')
    time.sleep(0.2)
    speaker.play('fa')
    speaker.play('fa')
