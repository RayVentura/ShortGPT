import os
import platform
import subprocess

import gradio as gr

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


def getBackgroundVideoChoices():
    df = AssetDatabase.get_df()
    choices = list(df.loc['background video' == df['type']]['name'])[:20]
    return choices


def getBackgroundMusicChoices():
    df = AssetDatabase.get_df()
    choices = list(df.loc['background music' == df['type']]['name'])[:20]
    return choices


def getElevenlabsVoices():
    api_key = ApiKeyManager.get_api_key("ELEVEN LABS")
    voices = list(reversed(ElevenLabsAPI(api_key).get_voices().keys()))
    return voices


def start_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


EDGE_TTS = "Free EdgeTTS (medium quality)"
ELEVEN_TTS = "ElevenLabs(High Quality)"

background_video_checkbox = gr.CheckboxGroup(choices=getBackgroundVideoChoices(), interactive=True, label="Choose background video")
background_music_checkbox = gr.CheckboxGroup(choices=getBackgroundMusicChoices(), interactive=True, label="Choose background music")
voiceChoice = gr.Radio(getElevenlabsVoices(), label="Elevenlabs voice", value="Antoni", interactive=True)
voiceChoiceTranslation = gr.Radio(getElevenlabsVoices(), label="Elevenlabs voice", value="Antoni", interactive=True)
