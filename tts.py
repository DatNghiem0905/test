import requests
import json

def textToSpeech(text):
    url = 'https://api.zalo.ai/v1/tts/synthesize'
    
    api_key = 'Z35s1d7eAMWSy2HgGhkeTbzDnFwKLVom' # api key lấy từ zalo

    headers = {
        'apikey': api_key
    }

    data = {
    	"input": text,
    	"speaker_id":2,
    }

    response = requests.post(url, data=data, headers=headers)
    print(response.content)
    linkTTS = response.json()['data']['url']
    return linkTTS
    
