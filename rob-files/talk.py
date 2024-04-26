import machine
import time

def play_wav(filename, frequency, delay, pwm, buffer_size=1024):
    # Open the WAV file
    with open(filename, 'rb') as f:
        # Skip the WAV header (first 44 bytes usually)
        wav_header = f.read(44)
        
        # Preload buffer
        buffer = f.read(buffer_size)
        buffer_index = 0
        
        # Read and play each sample from buffer
        while buffer:
            while buffer_index < len(buffer):
                byte = buffer[buffer_index]
                buffer_index += 1
                
                # Convert byte to PWM duty cycle
                sample = byte
                duty_cycle = int((sample / 255) * 1023)
                pwm.duty(duty_cycle)
                
                # Wait before playing next sample
                time.sleep(delay)
            
            # Reload buffer
            buffer = f.read(buffer_size)
            buffer_index = 0

def main():
    # Define the PWM pin connected to the speaker
    pwm_pin = machine.Pin(25)
    pwm = machine.PWM(pwm_pin)

    # Setup frequency and playback delay based on audio sample rate
    frequency = 40000  # Set a higher PWM frequency to minimize audible PWM noise
    delay = 1 / 8000   # Corresponds to the sample rate of the audio file
    
    # Initialize the PWM
    pwm.init(freq=frequency, duty=0)
    
    # Play the WAV file
    play_wav('audio.wav', frequency, delay, pwm, buffer_size=1024)

    # Cleanup
    pwm.deinit()

if __name__ == "__main__":
    main()
