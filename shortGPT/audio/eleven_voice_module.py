from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.audio.voice_module import VoiceModule


class ElevenLabsVoiceModule(VoiceModule):
    def __init__(self, api_key, voiceName, checkElevenCredits):
        self.api_key = api_key
        self.voiceName = voiceName
        self.remaining_credits = None
        self.update_usage()
        if checkElevenCredits and self.get_remaining_characters() < 1200:
            raise Exception(f"Your ElevenLabs API KEY doesn't have enough credits ({self.remaining_credits} character remaining). Minimum required: 1200 characters (equivalent to a 45sec short)")
        super().__init__()

    def update_usage(self):
        self.remaining_credits = ElevenLabsAPI(self.api_key).get_remaining_characters()
        return self.remaining_credits

    def get_remaining_characters(self):
        return self.remaining_credits if self.remaining_credits else ElevenLabsAPI(self.api_key).get_remaining_characters

    def generate_voice(self, text, outputfile):
        if self.get_remaining_characters() >= len(text):
            file_path = ElevenLabsAPI(self.api_key).generate_voice(text=text, character=self.voiceName, fileName=outputfile)
            self.update_usage()
            return file_path
        else:
            raise Exception(f"You cannot generate {len(text)} characters as your ElevenLabs key has only {self.remaining_credits} characters remaining")
