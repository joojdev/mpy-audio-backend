from pydub import AudioSegment
import soundfile as sf
from scipy.signal import butter, lfilter

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def noise_removal(src, dst):
    # Lendo o áudio com soundfile
    data, rate = sf.read(src)

    # Assegurando que o sinal de áudio está em float32
    if data.dtype != 'float32':
        data = data.astype('float32')

    # Reduzindo o ruído do áudio
    # data = nr.reduce_noise(y=data, sr=rate, stationary=True)
    data = butter_bandpass_filter(data, 300, 3000, rate, order=6)
    data = butter_lowpass_filter(data, 3000, rate, order=6)

    # Convertendo o array Numpy reduzido para um objeto AudioSegment
    reduced_audio_segment = AudioSegment(
        data=(data * 2**15).astype("int16").tobytes(), # Converter para int16 primeiro
        sample_width=2, # Largura de amostra em bytes (int16 -> 2 bytes)
        frame_rate=rate,
        channels=1 # Mono
    )

    # reduced_audio_segment.export("copy_" + dst, format="wav", codec="pcm_u8") # Bitrate reduzido para combinar com 8 bits de amostra
    
    # Alterando as características do áudio
    processed_audio = reduced_audio_segment.set_frame_rate(8000) # Definindo a taxa de amostragem para 8 kHz
    processed_audio = processed_audio.set_channels(1) # Certificando que é mono
    processed_audio = processed_audio.set_sample_width(1) # Alterando para 8 bits (1 byte por amostra)

    processed_audio += 12

    # Salvando o áudio processado em formato WAV
    processed_audio.export(dst, format="wav", codec="pcm_u8") # Bitrate reduzido para combinar com 8 bits de amostra

def prepare_audio(filename):
    # Salvando o áudio tratado com um novo nome de arquivo
    noise_removal(filename, filename)
    # os.system(f'cp {filename} copy_{filename}')
