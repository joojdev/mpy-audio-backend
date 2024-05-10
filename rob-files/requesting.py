import urequests
import ujson

url = 'http://192.168.11.212:5000'

def fetch_audio(prompt):
    data = {
        'text': prompt
    }
    json_data = ujson.dumps(data)
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = urequests.post(f'{url}/prompt', data=json_data.encode('ascii'), headers=headers, stream=True)
    
        if response.status_code == 200:
            with open('audio.wav', 'wb') as file:
                chunk_size = 1024  # 1KB per chunk, adjust based on your needs
                while True:
                    chunk = response.raw.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
            print(f"Áudio baixado com sucesso!")
            return True
        else:
            print("Falha ao baixar áudio:", response.status_code)
            return False
    except Exception as e:
        print("Falha ao baixar áudio:", e)
        return False
    response.close()
