from flask import Flask, request
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.get('/')
def homepage():
    with open('index.html', 'r') as file:
        index = file.read()
        file.close()

    return index

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    try:
        audio = AudioSegment.from_file(file)
        audio = audio.set_frame_rate(8000).set_sample_width(1).set_channels(1)

        file = open('audio.wav', 'wb')
        audio.export(file, format="wav")
        file.close()

        return 'Success!', 200
    except Exception as e:
        return str(e), 500

@app.get('/audio.wav')
def get_audio():
    if os.path.exists('audio.wav'):
        audio = open('audio.wav', 'rb')
        content = audio.read()
        audio.close()

        return content
    else:
        return 'File not found!', 404

if __name__ == '__main__':
    app.run(debug=True)
