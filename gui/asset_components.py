import os
import platform
import random
import subprocess
import socket

import gradio as gr

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


class AssetComponentsUtils:
    EDGE_TTS = "Free EdgeTTS (lower quality)"
    ELEVEN_TTS = "ElevenLabs(Very High Quality)"


    instance_background_video_checkbox = None
    instance_background_music_checkbox = None
    instance_voiceChoice: dict[gr.Radio] = {}
    instance_voiceChoiceTranslation: dict[gr.Radio] = {}

    @classmethod
    def getBackgroundVideoChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc["background video" == df["type"]]["name"])[:20]
        return choices

    @classmethod
    def getBackgroundMusicChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc["background music" == df["type"]]["name"])[:20]
        return choices

    @classmethod
    def getElevenlabsVoices(cls):
        api_key = ApiKeyManager.get_api_key("ELEVENLABS_API_KEY")
        voices = list(reversed(ElevenLabsAPI(api_key).get_voices().keys()))
        return voices
    
    # @classmethod
    # def start_file(cls, path):
    #     if platform.system() == "Windows":
    #         os.startfile(path)
    #     elif platform.system() == "Darwin":
    #         subprocess.Popen(["open", path])
    #     else:
    #         subprocess.Popen(["xdg-open", path])
    @classmethod
    def start_file(cls, filename):
        file_path = os.path.join("/app/videos", filename)
        if os.path.exists(file_path):
            return f"http://192.168.1.50:31415/file={file_path}" #Local host IP
        return "File not found!"

    @classmethod
    def background_video_checkbox(cls):
        if cls.instance_background_video_checkbox is None:
            choices = cls.getBackgroundVideoChoices()
            cls.instance_background_video_checkbox = gr.CheckboxGroup(
                choices=choices,
                interactive=True,
                label="Choose background video",
                value=random.choice(choices)
            )
        return cls.instance_background_video_checkbox

    @classmethod
    def background_music_checkbox(cls):
        if cls.instance_background_music_checkbox is None:
            choices = cls.getBackgroundMusicChoices()
            cls.instance_background_music_checkbox = gr.CheckboxGroup(
                choices=choices,
                interactive=True,
                label="Choose background music",
                value=random.choice(choices)
            )
        return cls.instance_background_music_checkbox

    @classmethod
    def voiceChoice(cls, provider: str = None):
        if provider == None:
            provider = cls.ELEVEN_TTS
        if cls.instance_voiceChoice.get(provider, None) is None:
            if provider == cls.ELEVEN_TTS:
                cls.instance_voiceChoice[provider] = gr.Radio(
                    cls.getElevenlabsVoices(),
                    label="Elevenlabs voice",
                    value="Chris",
                    interactive=True,
                )
        return cls.instance_voiceChoice[provider]

    @classmethod
    def voiceChoiceTranslation(cls, provider: str = None):
        if provider == None:
            provider = cls.ELEVEN_TTS
        if cls.instance_voiceChoiceTranslation.get(provider, None) is None:
            if provider == cls.ELEVEN_TTS:
                cls.instance_voiceChoiceTranslation[provider] = gr.Radio(
                    cls.getElevenlabsVoices(),
                    label="Elevenlabs voice",
                    value="Chris",
                    interactive=True,
                )
        return cls.instance_voiceChoiceTranslation[provider]
