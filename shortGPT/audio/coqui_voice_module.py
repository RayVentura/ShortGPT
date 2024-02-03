import os
from concurrent.futures import ThreadPoolExecutor

from TTS.api import TTS

from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import (
    EDGE_TTS_VOICENAME_MAPPING,
    LANGUAGE_ACRONYM_MAPPING,
    Language,
)
from torch.cuda import is_available


def run_async_func(loop, func):
    return loop.run_until_complete(func)


class CoquiVoiceModule(VoiceModule):
    def __init__(self, voiceName, language="en"):
        self.voiceName = voiceName
        self.device = "cuda" if is_available() else "cpu"
        self.language = language
        os.environ["COQUI_TOS_AGREED"] = "1"
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        super().__init__()

    def update_usage(self):
        return None

    def get_remaining_characters(self):
        return 999999999999

    def generate_voice(self, text, outputfile):
        try:
            self.tts.to(self.device)
            self.tts.tts_to_file(
                text=text,
                file_path=outputfile,
                speaker=self.voiceName,
                language=self.language,
                split_sentences=True,
            )
        except Exception as e:
            print("Error generating audio using coqui audio", e)
            raise Exception(
                "An error happened during coqui audio generation, no output audio generated",
                e,
            )
        if not os.path.exists(outputfile):
            print(
                "An error happened during coqui audio generation, no output audio generated"
            )
            raise Exception(
                "An error happened during coqui audio generation, no output audio generated"
            )
        return outputfile
