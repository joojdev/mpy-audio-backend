from espeakng import ESpeakNG
from pydub import AudioSegment
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

  audio += 5

  audio_file = BytesIO()
  audio.export(audio_file, format='wav')
  audio_file.seek(0)

  return audio_file.getvalue()