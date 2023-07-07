import requests
import json
import random

def getVoices():
    url = 'https://api.elevenlabs.io/v1/voices'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    voices = {}
    for a in response.json()['voices']:
        voices[a['name']] = a['voice_id']
    return voices

def getCharactersFromKey(key):
    url = 'https://api.elevenlabs.io/v1/user'
    headers = {
            'accept': '*/*',
            'xi-api-key':key,
            'Content-Type': 'application/json'
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sub = response.json()['subscription']
        return sub['character_limit'] - sub['character_count']
    else:
        raise Exception(response.json()['detail']['message'])
def generateVoice(text, character, fileName, stability=0.2, clarity=0.1, api_key=""):
    if not api_key:
        raise Exception("No api key")
    charactersDict = getVoices()
    characters = list(charactersDict.keys())
    if character not in characters:
        print(character, 'is not in the array of characters: ', characters)
    voice_id = charactersDict[character]
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream'
    headers = {
        'accept': '*/*',
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    data = json.dumps({
        "model_id": "eleven_multilingual_v1",
        "text": text,
        "stability": stability,
        "similarity_boost": clarity,
    })
    response = requests.post(url, headers=headers, data=data)
    if(response.status_code == 200):
        with open(fileName, 'wb') as f:
            f.write(response.content)
            return fileName
    else:
        message = response.text
        print(f'Error in response, {response.status_code} , message: {message}')
    return ""

# print(getCharactersFromKey(''))
