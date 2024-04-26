from machine import Pin, PWM
from time import sleep

class Motor:
    def __init__(self, motor_pin, b1_pin, b2_pin, frequency):
        # Configura o pino do motor como saída e inicializa o PWM no mesmo pino
        self.motor_pin = Pin(motor_pin, Pin.OUT)
        self.pwm = PWM(motor_pin)
        
        # Configura os pinos de direção como saídas
        self.b1_pin = Pin(b1_pin, Pin.OUT)
        self.b2_pin = Pin(b2_pin, Pin.OUT)
        self.b1_pin.value(False)
        self.b2_pin.value(False)
        
        # Configura a frequência do PWM para o valor inicial
        self.pwm.freq(frequency)
    
    @property
    def frequency(self):
        # Retorna a frequência atual do PWM
        return self.pwm.freq()
    
    @frequency.setter
    def frequency(self, value):
        # Ajusta a frequência do PWM
        self.pwm.freq(value)
        
    def set_motor_speed(self, speed_percentage):
        """
        Ajusta a velocidade do motor de acordo com o percentual fornecido.
        :param speed_percentage: Um valor de 0 (parado) a 100 (velocidade máxima)
        """
        if 0 <= speed_percentage <= 100:
            # Calcula o ciclo de trabalho com base no percentual de velocidade
            duty_cycle = int((speed_percentage / 100) * 1023)
            self.pwm.duty(duty_cycle)
        else:
            print("Por favor, insira um valor entre 0 e 100.")
            
    def forward(self, speed_percentage, seconds):
        # Define a direção para frente e ajusta a velocidade
        self.b1_pin.value(True)
        sleep(0.05)
        self.set_motor_speed(speed_percentage)
        sleep(seconds)
        # Para o motor após o tempo especificado
        self.b1_pin.value(False)
        self.set_motor_speed(0)
            
    def backward(self, speed_percentage, seconds):
        # Define a direção para trás e ajusta a velocidade
        self.b2_pin.value(True)
        sleep(0.05)
        self.set_motor_speed(speed_percentage)
        sleep(seconds)
        # Para o motor após o tempo especificado
        self.b2_pin.value(False)
        self.set_motor_speed(0)

# Instanciação dos objetos de motor
right_motor = Motor(27, 33, 26, 5000)
left_motor = Motor(12, 13, 2, 5000)

if __name__ == '__main__':
    # Testa as funções de movimento dos motores
    right_motor.forward(100, 2)
    right_motor.backward(100, 2)
    left_motor.forward(100, 2)
    left_motor.backward(100, 2)

