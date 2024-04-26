from flask import Flask, request
from gpt import generate_speech_answer
import json

app = Flask(__name__)

@app.get('/')
def homepage():
    with open('index.html', 'r') as file:
        index = file.read()
        file.close()

    return index

@app.post('/prompt')
def convert_text_to_audio():
    text = request.json.get('text')

    print(f' USER > {text}')

    if not text:
        return "No text provided", 400

    try:
        generate_speech_answer(text)

        file = open('audio.wav', 'rb')
        audio = file.read()
        file.close()

        return audio, 200
    except Exception as e:
        print(e)
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
