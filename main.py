from flask import Flask, request
from gpt import generate_speech_answer
from database.driver import create_transaction, search_user

app = Flask(__name__)

@app.get('/')
def homepage():
    with open('index.html', 'r') as file:
        index = file.read()
        file.close()

    return index

@app.post('/prompt')
def convert_text_to_audio():
    key = request.json.get('key')
    text = request.json.get('text')

    if not key:
        return "No key provided!", 400

    if not text:
        return "No text provided!", 400

    user_id = search_user(key)

    if not user_id:
        return "The provided key is invalid!", 400

    print(f' USER > {text}')

    try:
        audio, usage = generate_speech_answer(text)
        create_transaction(user_id, usage.prompt_tokens, usage.completion_tokens)

        return audio, 200
    except Exception as e:
        print(str(e))
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
