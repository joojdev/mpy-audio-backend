from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter

def prepare_audio(filename):
    audio = AudioSegment.from_file(filename)

    audio = low_pass_filter(audio, 3000)
    audio = high_pass_filter(audio, 300)

    # Ajustes finais da taxa de amostra, largura de amostra e número de canais
    audio = audio.set_frame_rate(8000).set_sample_width(1).set_channels(1)

    # Ajuste de volume
    audio += 7

    audio.export(filename, format='wav', codec='pcm_u8')

