from pydub import AudioSegment
from pydub.effects import normalize, low_pass_filter, high_pass_filter

def prepare_audio(filename):
    audio = AudioSegment.from_file(filename)
    modified_audio = normalize(audio)
  
    modified_audio = low_pass_filter(modified_audio, 4000)
    modified_audio = high_pass_filter(modified_audio, 400)

    modified_audio = modified_audio.set_frame_rate(8000).set_sample_width(1).set_channels(1)

    modified_audio += 7

    modified_audio.export(filename, format='wav', codec='pcm_u8')