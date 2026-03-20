import json
import os

import requests

from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.api_db import ApiKeyManager

MINIMAX_TTS_VOICES = {
    'English_Graceful_Lady': 'Graceful Lady (EN)',
    'English_Insightful_Speaker': 'Insightful Speaker (EN)',
    'English_radiant_girl': 'Radiant Girl (EN)',
    'English_Persuasive_Man': 'Persuasive Man (EN)',
    'English_Lucky_Robot': 'Lucky Robot (EN)',
    'Wise_Woman': 'Wise Woman',
    'cute_boy': 'Cute Boy',
    'lovely_girl': 'Lovely Girl',
    'Friendly_Person': 'Friendly Person',
    'Inspirational_girl': 'Inspirational Girl',
    'Deep_Voice_Man': 'Deep Voice Man',
    'sweet_girl': 'Sweet Girl',
}


class MiniMaxVoiceModule(VoiceModule):
    def __init__(self, api_key, voice_id='English_Graceful_Lady', model='speech-2.8-hd'):
        self.api_key = api_key
        self.voice_id = voice_id
        self.model = model
        self.base_url = 'https://api.minimax.io'
        super().__init__()

    def update_usage(self):
        return None

    def get_remaining_characters(self):
        return 999999999999

    def generate_voice(self, text, outputfile):
        url = f'{self.base_url}/v1/t2a_v2'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }
        payload = {
            'model': self.model,
            'text': text,
            'stream': False,
            'voice_setting': {
                'voice_id': self.voice_id,
                'speed': 1,
                'vol': 1,
                'pitch': 0,
            },
            'audio_setting': {
                'sample_rate': 32000,
                'bitrate': 128000,
                'format': 'mp3',
                'channel': 1,
            },
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'MiniMax TTS error: {response.status_code} {response.text}')

        result = response.json()
        if result.get('base_resp', {}).get('status_code', -1) != 0:
            status_msg = result.get('base_resp', {}).get('status_msg', 'Unknown error')
            raise Exception(f'MiniMax TTS error: {status_msg}')

        hex_audio = result.get('data', {}).get('audio')
        if not hex_audio:
            raise Exception('MiniMax TTS: no audio data in response')

        audio_bytes = bytes.fromhex(hex_audio)
        with open(outputfile, 'wb') as f:
            f.write(audio_bytes)

        return outputfile
