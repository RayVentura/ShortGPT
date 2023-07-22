import gradio as gr
from shortGPT.config.asset_db import AssetDatabase
from shortGPT.config.api_db import get_api_key
from shortGPT.api_utils.eleven_api import getVoices
AssetDatabase().sync_local_assets()
def getBackgroundVideoChoices():
    asset_db = AssetDatabase()
    df = asset_db.get_df()
    choices = list(df.loc['background video'  ==  df['type']]['name'])[:20]
    return choices

def getBackgroundMusicChoices():
    asset_db = AssetDatabase()
    df = asset_db.get_df()
    choices = list(df.loc['background music'  ==  df['type']]['name'])[:20]
    return choices

def getElevenlabsVoices():
    api_key = get_api_key("ELEVEN LABS")
    voices = list(reversed(getVoices(api_key).keys()))
    return voices

background_video_checkbox = gr.CheckboxGroup(choices=getBackgroundVideoChoices(), interactive=True, label="Choose background video")
background_music_checkbox = gr.CheckboxGroup(choices=getBackgroundMusicChoices(), interactive=True, label="Choose background music")
voiceChoice = gr.Radio(getElevenlabsVoices(), label="Elevenlabs voice", value="Antoni", interactive=True)
voiceChoiceTranslation = gr.Radio(getElevenlabsVoices(), label="Elevenlabs voice", value="Antoni", interactive=True)
import os, platform, subprocess

def start_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])