import os
import platform
import subprocess

import gradio as gr

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


class AssetComponentsUtils:
    EDGE_TTS = "Free EdgeTTS (lower quality)"
    ELEVEN_TTS = "ElevenLabs(Very High Quality)"
    instance_background_video_checkbox = None
    instance_background_music_checkbox = None
    instance_voiceChoice = None
    instance_voiceChoiceTranslation = None

    @classmethod
    def getBackgroundVideoChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc['background video' == df['type']]['name'])[:20]
        return choices

    @classmethod
    def getBackgroundMusicChoices(cls):
        df = AssetDatabase.get_df()
        choices = list(df.loc['background music' == df['type']]['name'])[:20]
        return choices

    @classmethod
    def getElevenlabsVoices(cls):
        api_key = ApiKeyManager.get_api_key("ELEVEN LABS")
        voices = list(reversed(ElevenLabsAPI(api_key).get_voices().keys()))
        return voices

    @classmethod
    def start_file(cls, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    @classmethod
    def background_video_checkbox(cls):
        if cls.instance_background_video_checkbox is None:
            cls.instance_background_video_checkbox = gr.CheckboxGroup(
                choices=cls.getBackgroundVideoChoices(),
                interactive=True,
                label="Choose background video",
            )
        return cls.instance_background_video_checkbox

    @classmethod
    def background_music_checkbox(cls):
        if cls.instance_background_music_checkbox is None:
            cls.instance_background_music_checkbox = gr.CheckboxGroup(
                choices=cls.getBackgroundMusicChoices(),
                interactive=True,
                label="Choose background music",
            )
        return cls.instance_background_music_checkbox

    @classmethod
    def voiceChoice(cls):
        if cls.instance_voiceChoice is None:
            cls.instance_voiceChoice = gr.Radio(
                cls.getElevenlabsVoices(),
                label="Elevenlabs voice",
                value="Antoni",
                interactive=True,
            )
        return cls.instance_voiceChoice

    @classmethod
    def voiceChoiceTranslation(cls):
        if cls.instance_voiceChoiceTranslation is None:
            cls.instance_voiceChoiceTranslation = gr.Radio(
                cls.getElevenlabsVoices(),
                label="Elevenlabs voice",
                value="Antoni",
                interactive=True,
            )
        return cls.instance_voiceChoiceTranslation
