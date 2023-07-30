import os
import platform
import subprocess

import streamlit as st

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


class AssetComponentsUtils:
    EDGE_TTS = "Free EdgeTTS (medium quality)"
    ELEVEN_TTS = "ElevenLabs(High Quality)"

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
        background_video_choice = st.multiselect(
            "Choose background video",
            options=cls.getBackgroundVideoChoices(),
            key="background_video_checkbox"
        )
        return background_video_choice
