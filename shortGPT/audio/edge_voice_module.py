from shortGPT.audio.voice_module import VoiceModule
import asyncio
import edge_tts
from shortGPT.audio.edge_TTS_voices import EdgeTTSLanguage, language_to_voice_name
class EdgeTTSVoiceModule(VoiceModule):
    def __init__(self, voiceName):
        self.voiceName = voiceName
        super().__init__()

    def update_usage(self):
        return None

    def get_remaining_characters(self):
        return None

    def generate_voice(self, text, outputfile):
        loop = asyncio.get_event_loop()

        if loop.is_running():
            loop.create_task(self.async_generate_voice(text, outputfile))
        else:
            loop.run_until_complete(self.async_generate_voice(text, outputfile))

    async def async_generate_voice(self, text, outputfile):
        communicate = edge_tts.Communicate(text, self.voiceName)
        with open(outputfile, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        return outputfile