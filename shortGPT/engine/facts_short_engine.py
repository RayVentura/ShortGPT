from shortGPT.audio.voice_module import VoiceModule
from shortGPT.gpt import facts_gpt
from shortGPT.config.languages import Language
from shortGPT.engine.content_short_engine import ContentShortEngine


class FactsShortEngine(ContentShortEngine):

    def __init__(self, voiceModule: VoiceModule, facts_type: str, background_video_name: str, background_music_name: str,short_id="",
                 num_images=None, watermark=None, language:Language = Language.ENGLISH):
        super().__init__(short_id=short_id, short_type="facts_shorts", background_video_name=background_video_name, background_music_name=background_music_name,
                 num_images=num_images, watermark=watermark, language=language, voiceModule=voiceModule)
        
        self._db_facts_type = facts_type

    def _generateScript(self):
        """
        Implements Abstract parent method to generate the script for the Facts short.
        """
        self._db_script = facts_gpt.generateFacts(self._db_facts_type)

