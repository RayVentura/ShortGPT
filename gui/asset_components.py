import os
import platform
import subprocess

import gradio as gr

from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.asset_db import AssetDatabase


class AssetComponentsUtils:
    EDGE_TTS = "Free EdgeTTS (lower quality)"
    COQUI_TTS = "Free CoquiTTS (needs a powerful GPU)"
    ELEVEN_TTS = "ElevenLabs(Very High Quality)"

    COQUI_TTS_VOICES = [
        "Claribel Dervla",
        "Daisy Studious",
        "Gracie Wise",
        "Tammie Ema",
        "Alison Dietlinde",
        "Ana Florence",
        "Annmarie Nele",
        "Asya Anara",
        "Brenda Stern",
        "Gitta Nikolina",
        "Henriette Usha",
        "Sofia Hellen",
        "Tammy Grit",
        "Tanja Adelina",
        "Vjollca Johnnie",
        "Andrew Chipper",
        "Badr Odhiambo",
        "Dionisio Schuyler",
        "Royston Min",
        "Viktor Eka",
        "Abrahan Mack",
        "Adde Michal",
        "Baldur Sanjin",
        "Craig Gutsy",
        "Damien Black",
        "Gilberto Mathias",
        "Ilkin Urbano",
        "Kazuhiko Atallah",
        "Ludvig Milivoj",
        "Suad Qasim",
        "Torcull Diarmuid",
        "Viktor Menelaos",
        "Zacharie Aimilios",
        "Nova Hogarth",
        "Maja Ruoho",
        "Uta Obando",
        "Lidiya Szekeres",
        "Chandra MacFarland",
        "Szofi Granger",
        "Camilla Holmström",
        "Lilya Stainthorpe",
        "Zofija Kendrick",
        "Narelle Moon",
        "Barbora MacLean",
        "Alexandra Hisakawa",
        "Alma María",
        "Rosemary Okafor",
        "Ige Behringer",
        "Filip Traverse",
        "Damjan Chapman",
        "Wulf Carlevaro",
        "Aaron Dreschner",
        "Kumar Dahl",
        "Eugenio Mataracı",
        "Ferran Simen",
        "Xavier Hayasaka",
        "Luis Moray",
        "Marcos Rudaski",
    ]

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
    def voiceChoice(cls, provider: str = None):
        if provider == None:
            provider = cls.ELEVEN_TTS
        if cls.instance_voiceChoice.get(provider, None) is None:
            if provider == cls.ELEVEN_TTS:
                print("getting eleven voices")
                cls.instance_voiceChoice[provider] = gr.Radio(
                    cls.getElevenlabsVoices(),
                    label="Elevenlabs voice",
                    value="Antoni",
                    interactive=True,
                )
            elif provider == cls.COQUI_TTS:
                print("getting coqui voices")
                cls.instance_voiceChoice[provider] = gr.Dropdown(
                    cls.COQUI_TTS_VOICES,
                    label="CoquiTTS voice",
                    value="Ana Florence",
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
                    value="Antoni",
                    interactive=True,
                )
            elif provider == cls.COQUI_TTS:
                cls.instance_voiceChoiceTranslation[provider] = gr.Radio(
                    cls.COQUI_TTS_VOICES,
                    label="CoquiTTS voice",
                    value="Ana Florence",
                    interactive=True,
                )
        return cls.instance_voiceChoiceTranslation[provider]
