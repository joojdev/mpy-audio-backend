import os
from openai import OpenAI
from dotenv import load_dotenv
from audio import prepare_audio
import re
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def demojify(text):
  # Regex para combinar emojis
  emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # símbolos & pictogramas
    "\U0001F680-\U0001F6FF"  # transporte & mapas
    "\U0001F700-\U0001F77F"  # alquimia
    "\U0001F780-\U0001F7FF"  # Geometric shapes extended
    "\U0001F800-\U0001F8FF"  # Supplemental arrows-C
    "\U0001F900-\U0001F9FF"  # suplementar símbolos e pictogramas
    "\U0001FA00-\U0001FA6F"  # Chess symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "\U0000200D"        # zero width joiner
    "\U0000FE0F"        # variation selector
    "]+", flags=re.UNICODE)
  
  return emoji_pattern.sub(r'', text)

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

  audio_file = prepare_audio(demojify(content))

  return audio_file, text_response.usage