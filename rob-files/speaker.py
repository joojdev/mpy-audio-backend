import machine
import time

def play_wav(filename, pwm_pin):
    pwm_pin = machine.Pin(pwm_pin)
    pwm = machine.PWM(pwm_pin)
    
    frequency = 40000
    delay = 1 / 40000
    
    pwm.init(freq=frequency, duty=0)
    buffer_size = 2048
    
    with open(filename, 'rb') as f:
        wav_header = f.read(44)
        
        buffer = f.read(buffer_size)
        buffer_index = 0
        
        while buffer:
            while buffer_index < len(buffer):
                byte = buffer[buffer_index]
                buffer_index += 1
                
                sample = byte
                duty_cycle = int((sample / 255) * 1023)
                pwm.duty(duty_cycle)
                
                time.sleep(delay)
            
            buffer = f.read(buffer_size)
            buffer_index = 0
        
    pwm.deinit()
