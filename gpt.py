import os
from openai import OpenAI
from dotenv import load_dotenv
from audio import prepare_audio
from datetime import datetime
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_speech_answer(prompt):
  timestamp = int(datetime.timestamp(datetime.now()))
  temp_filename = f'temp_output-{timestamp}.wav'

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Seu nome é ROB, você é um robô muito brincalhão!"},
      {"role": "user", "content": prompt}
    ],
    max_tokens=180
  )

  content = response.choices[0].message.content
  print(f' GPT > {content}')

  with client.audio.speech.with_streaming_response.create(
      model='tts-1',
      voice='alloy',
      speed=1,
      response_format='wav',
      input=content
  ) as response:
     response.stream_to_file(temp_filename)

  prepare_audio(temp_filename)

  os.remove(temp_filename)
  return content