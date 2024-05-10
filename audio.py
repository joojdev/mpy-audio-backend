from espeakng import ESpeakNG
from pydub import AudioSegment
from pydub.effects import low_pass_filter, high_pass_filter
from io import BytesIO

def prepare_audio(content):
  esng = ESpeakNG()
  esng.voice = 'pt-br'
  esng.speed = 150
  esng.pitch = 90

  synthesis = esng.synth_wav(content)

  audio = BytesIO(synthesis)
  audio = AudioSegment.from_wav(audio)

  audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)
  low_pass_filter(audio, 3000)
  high_pass_filter(audio, 300)

  audio += 5

  audio_file = BytesIO()
  audio.export(audio_file, format='wav')
  audio_file.seek(0)

  return audio_file.getvalue()