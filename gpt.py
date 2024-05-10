import os
from openai import OpenAI
from dotenv import load_dotenv
from audio import prepare_audio
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_speech_answer(prompt):
  text_response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Seu nome é ROB, você é um robô muito brincalhão!"},
      # {"role": "system", "content": "Your name is Robby, and you are an educational robot."},
      {"role": "user", "content": prompt}
    ],
    max_tokens=180
  )

  content = text_response.choices[0].message.content
  print(f' GPT > {content}')

  audio_file = prepare_audio(content)

  return audio_file, text_response.usage