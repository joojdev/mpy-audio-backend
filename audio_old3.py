from pydub import AudioSegment
import noisereduce as nr
import soundfile as sf

def noise_removal(src, dst):
    # Lendo o áudio com soundfile
    data, rate = sf.read(src)

    # Assegurando que o sinal de áudio está em float32
    if data.dtype != 'float32':
        data = data.astype('float32')

    # Reduzindo o ruído do áudio
    noise_reduced = nr.reduce_noise(y=data, sr=rate, stationary=True)

    # Convertendo o array Numpy reduzido para um objeto AudioSegment
    reduced_audio_segment = AudioSegment(
        data=(noise_reduced * 2**15).astype("int16").tobytes(), # Converter para int16 primeiro
        sample_width=2, # Largura de amostra em bytes (int16 -> 2 bytes)
        frame_rate=rate,
        channels=1 # Mono
    )
    
    # Alterando as características do áudio
    processed_audio = reduced_audio_segment.set_frame_rate(8000) # Definindo a taxa de amostragem para 8 kHz
    processed_audio = processed_audio.set_channels(1) # Certificando que é mono
    processed_audio = processed_audio.set_sample_width(1) # Alterando para 8 bits (1 byte por amostra)

    processed_audio += 7

    # Salvando o áudio processado em formato WAV
    processed_audio.export(dst, format="wav", codec="pcm_u8") # Bitrate reduzido para combinar com 8 bits de amostra

def prepare_audio(filename):
    # Salvando o áudio tratado com um novo nome de arquivo
    noise_removal(filename, filename)
