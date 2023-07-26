from shortGPT.audio.audio_duration import getAssetDuration
from shortGPT.audio.voice_module import VoiceModule
from shortGPT.engine.abstract_content_engine import AbstractContentEngine
from shortGPT.gpt.gpt_translate import translateContent
from shortGPT.config.languages import Language, ACRONYM_LANGUAGE_MAPPING
from shortGPT.editing_utils.handle_videos import get_aspect_ratio
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep
from shortGPT.editing_utils.captions import getSpeechBlocks, getCaptionsWithTime
from shortGPT.audio.audio_utils import audioToText, getAssetDuration, speedUpAudio
from tqdm import tqdm
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep
import re
import shutil
import os
import datetime

class ContentTranslationEngine(AbstractContentEngine):

    def __init__(self,voiceModule: VoiceModule, src_url: str = "", target_language: Language = Language.ENGLISH, use_captions=False, id=""):
        super().__init__(id, "content_translation", target_language, voiceModule)
        if not id:
            self._db_should_translate = True
            if src_url:
                self._db_src_url = src_url
            self._db_use_captions = use_captions
            self._db_target_language = target_language.value

        self.stepDict = {
            1: self._transcribe_audio,
            2: self._translate_content,
            3: self._generate_translated_audio,
            4: self._edit_and_render_video,
            5: self._add_metadata
        }

    def _transcribe_audio(self):
        video_audio, _ = getAssetDuration(self._db_src_url, isVideo=False)
        self.verifyParameters(content_path=video_audio)
        self.logger(f"1/5 - Transcribing original audio to text...")
        whispered = audioToText(video_audio, model_size='base')
        self._db_speech_blocks = getSpeechBlocks(whispered, silence_time=0.8)
        if (ACRONYM_LANGUAGE_MAPPING.get(whispered['language']) == Language(self._db_target_language)):
            self._db_translated_timed_sentences = self._db_speech_blocks 
            self._db_should_translate = False

        expected_chars = len("".join([text for _, text in self._db_speech_blocks]))
        chars_remaining = self.voiceModule.get_remaining_characters()
        if chars_remaining < expected_chars:
            raise Exception(
                f"Your VoiceModule's key doesn't have enough characters to totally translate this video | Remaining: {chars_remaining} | Number of characters to translate: {expected_chars}")

    def _translate_content(self):
        if(self._db_should_translate):
            self.verifyParameters(_db_speech_blocks=self._db_speech_blocks)

            translated_timed_sentences = []
            for i, ((t1, t2), text) in tqdm(enumerate(self._db_speech_blocks), desc="Translating content"):
                self.logger(f"2/5 - Translating text content - {i+1} / {len(self._db_speech_blocks)}")
                translated_text = translateContent(text, self._db_target_language)
                translated_timed_sentences.append([[t1, t2], translated_text])
            self._db_translated_timed_sentences = translated_timed_sentences

    def _generate_translated_audio(self):
        self.verifyParameters(translated_timed_sentences=self._db_translated_timed_sentences)

        translated_audio_blocks = []
        for i, ((t1, t2), translated_text) in tqdm(enumerate(self._db_translated_timed_sentences), desc="Generating translated audio"):
            self.logger(f"3/5 - Generating translated audio - {i+1} / {len(self._db_translated_timed_sentences)}")
            translated_voice = self.voiceModule.generate_voice(translated_text, self.dynamicAssetDir+f"translated_{i}_{self._db_target_language}.wav")
            if not translated_voice:
                raise Exception('An error happending during audio voice creation')
            final_audio_path = speedUpAudio(translated_voice,self.dynamicAssetDir+f"translated_{i}_{self._db_target_language}_spedup.wav" ,expected_duration=t2-t1 -0.05)
            _, translated_duration = getAssetDuration(final_audio_path, isVideo=False)
            translated_audio_blocks.append([[t1, t1+translated_duration], final_audio_path])
        self._db_audio_bits = translated_audio_blocks

    def _edit_and_render_video(self):
        self.verifyParameters(_db_audio_bits=self._db_audio_bits)
        self.logger(f"4.1 / 5 - Preparing automated editing")
        target_language =  Language(self._db_target_language)
        input_video, video_length = getAssetDuration(self._db_src_url)
        video_audio, _ = getAssetDuration(self._db_src_url, isVideo=False)
        editing_engine = EditingEngine()
        editing_engine.addEditingStep(EditingStep.ADD_BACKGROUND_VIDEO, {'url': input_video, "set_time_start": 0, "set_time_end": video_length})
        last_t2 = 0
        for (t1, t2), audio_path in self._db_audio_bits:
            t2+=-0.05
            editing_engine.addEditingStep(EditingStep.INSERT_AUDIO, {'url': audio_path, 'set_time_start': t1, 'set_time_end': t2})
            if t1-last_t2 >4:
                editing_engine.addEditingStep(EditingStep.EXTRACT_AUDIO, {"url": video_audio, "subclip": {"t_start": last_t2, "t_end": t1}, "set_time_start": last_t2, "set_time_end":  t1})
            last_t2 = t2

        if video_length - last_t2 >4:
            editing_engine.addEditingStep(EditingStep.EXTRACT_AUDIO, {"url": video_audio, "subclip": {"t_start": last_t2, "t_end": video_length}, "set_time_start": last_t2, "set_time_end":  video_length})

        if self._db_use_captions:
            is_landscape = get_aspect_ratio(input_video) > 1
            if not self._db_timed_translated_captions:
                if not self._db_translated_voiceover_path:
                    self.logger(f"4.5 / 5 - Generating captions in {target_language.value}")
                    editing_engine.generateAudio(self.dynamicAssetDir+"translated_voiceover.wav")
                    self._db_translated_voiceover_path = self.dynamicAssetDir+"translated_voiceover.wav"
                whispered_translated = audioToText(self._db_translated_voiceover_path, model_size='base')
                timed_translated_captions = getCaptionsWithTime(whispered_translated, maxCaptionSize=50 if is_landscape else 15, considerPunctuation=True)
                self._db_timed_translated_captions = [[[t1,t2], text] for (t1, t2), text in timed_translated_captions if t2 - t1 <= 4]
            for (t1, t2), text in self._db_timed_translated_captions:
                caption_key = "LANDSCAPE" if is_landscape else "SHORT"
                caption_key += "_ARABIC" if target_language == Language.ARABIC else ""
                caption_type = getattr(EditingStep, f"ADD_CAPTION_{caption_key}")
                editing_engine.addEditingStep(caption_type, {'text': text, "set_time_start": t1, "set_time_end": t2})
    
        self._db_video_path = self.dynamicAssetDir+"translated_content.mp4"

        editing_engine.renderVideo(self._db_video_path, logger=self.logger)

    def _add_metadata(self):
        self.logger(f"5 / 5 - Saving translated video")
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        newFileName = f"videos/{date_str} - " + \
            re.sub(r"[^a-zA-Z0-9 '\n\.]", '', f"translated_content_to_{self._db_target_language}")

        shutil.move(self._db_video_path, newFileName+".mp4")
        self._db_video_path = newFileName+".mp4"
        self._db_ready_to_upload = True
