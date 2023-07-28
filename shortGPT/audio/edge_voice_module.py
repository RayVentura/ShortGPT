import asyncio
import os
from concurrent.futures import ThreadPoolExecutor

import edge_tts

from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       LANGUAGE_ACRONYM_MAPPING, Language)


def run_async_func(loop, func):
    return loop.run_until_complete(func)


class EdgeTTSVoiceModule(VoiceModule):
    def __init__(self, voiceName):
        self.voiceName = voiceName
        super().__init__()

    def update_usage(self):
        return None

    def get_remaining_characters(self):
        return 999999999999

    def generate_voice(self, text, outputfile):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            with ThreadPoolExecutor() as executor:
                loop.run_in_executor(executor, run_async_func, loop, self.async_generate_voice(text, outputfile))

        finally:
            loop.close()
        if not os.path.exists(outputfile):
            print("An error happened during edge_tts audio generation, no output audio generated")
            raise Exception("An error happened during edge_tts audio generation, no output audio generated")
        return outputfile

    async def async_generate_voice(self, text, outputfile):
        try:
            communicate = edge_tts.Communicate(text, self.voiceName)
            with open(outputfile, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
        except Exception as e:
            print("Error generating audio using edge_tts", e)
            raise Exception("An error happened during edge_tts audio generation, no output audio generated", e)
        return outputfile
