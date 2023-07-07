from shortGPT.audio.audio_duration import getAssetDuration
from shortGPT.gpt import facts_gpt, gpt_editing, gpt_translate, gpt_yt
from shortGPT.audio import audio_utils
from shortGPT.editing_utils import captions, editing_images
from shortGPT.editing_utils.handle_videos import extract_random_clip_from_video
from shortGPT.engine.abstract_short_engine import AbstractShortEngine, Language
from shortGPT.engine.abstract_content_short_engine import AbstractContentShortEngine
from shortGPT.editing_framework.editing_flow import EditingFlow, EditingStep, Flow
import re
import shutil
import os
import datetime

class FactsShortEngine(AbstractContentShortEngine):
    # Mapping of variable names to database paths
    def __init__(self, facts_type: str, background_video_name: str, background_music_name: str,short_id="",
                 num_images=None, watermark=None, language:Language = Language.ENGLISH):
        super().__init__(short_id, "facts_shorts", language)
        if (num_images):
            self._db_num_images = num_images
        if (watermark):
            self._db_watermark = watermark
        self._db_facts_type = facts_type
        self._db_background_video_name = background_video_name
        self._db_background_music_name = background_music_name
        
        self.stepDict = {
            1:  self._generateFactsScript,
            2:  self._generateTempAudio,
            3:  self._speedUpAudio,
            4:  self._timeCaptions,
            5:  self._generateImageSearchTerms,
            6:  self._generateImageUrls,
            7: self._chooseBackgroundMusic,
            8: self._chooseBackgroundVideo,
            9: self._editAndRenderShort,
            10: self._addYoutubeMetadata
        }

    def _generateFactsScript(self):
        self._db_script = facts_gpt.generateFacts(self._db_facts_type)


    def _generateTempAudio(self):
        if (self._db_temp_audio_path):
            return
        self.verifyParameters(text=self._db_script)
        if not self._db_voice_character:
            if (self._db_voice_gender == 'male'):
                self._db_voice_character = "Antoni"
            else:
                self._db_voice_character = "Bella"
        script = self._db_script
        if (self._db_language != Language.ENGLISH.value):
            self._db_translated_script = gpt_translate.translateContent(script, self._db_language)
            script = self._db_translated_script
        self._db_temp_audio_path = self.voiceModule.generate_voice(
            script, self.dynamicAssetDir + "temp_audio_path.wav", self._db_voice_character)

    def _speedUpAudio(self):
        if (self._db_audio_path):
            return
        self.verifyParameters(tempAudioPath=self._db_temp_audio_path)
        self._db_audio_path = audio_utils.speedUpAudio(
            self._db_temp_audio_path, self.dynamicAssetDir+"audio_voice.wav")

    def _timeCaptions(self):
        self.verifyParameters(audioPath=self._db_audio_path)
        whisper_analysis = audio_utils.audioToText(self._db_audio_path)
        self._db_timed_captions = captions.getCaptionsWithTime(
            whisper_analysis)

    def _generateImageSearchTerms(self):
        self.verifyParameters(captionsTimed=self._db_timed_captions)
        if self._db_num_images:
            self._db_timed_image_searches = gpt_editing.getImageQueryPairs(
                self._db_timed_captions, n=self._db_num_images)

    def _generateImageUrls(self):
        if self._db_timed_image_searches:
            self._db_timed_image_urls = editing_images.getImageUrlsTimed(
                self._db_timed_image_searches)

    def _chooseBackgroundMusic(self):
        self._db_background_music_url = self.assetStore.getAssetLink(self._db_background_music_name)

    def _chooseBackgroundVideo(self):
        self._db_background_video_url = self.assetStore.getAssetLink(
            self._db_background_video_name)
        self._db_background_video_duration = self.assetStore.getAssetDuration(
            self._db_background_video_name)

    def _editAndRenderShort(self):
        self.verifyParameters(
                              voiceover_audio_url=self._db_audio_path,
                              video_duration=self._db_background_video_duration,
                              background_video_url=self._db_background_video_url, music_url=self._db_background_music_url)
        if not self._db_voiceover_duration:
            self.logger("Rendering short: (1/4) preparing voice asset...")
            self._db_audio_path, self._db_voiceover_duration = getAssetDuration(
                self._db_audio_path, isVideo=False)
        if not self._db_background_trimmed:
            self.logger("Rendering short: (2/4) preparing background video asset...")
            self._db_background_trimmed = extract_random_clip_from_video(
                self._db_background_video_url, self._db_background_video_duration, self._db_voiceover_duration, self.dynamicAssetDir + "clipped_background.mp4")
        outputPath = self.dynamicAssetDir+"rendered_video.mp4"
        if not (os.path.exists(outputPath)):
            self.logger("Rendering short: (3/4) Starting automated editing...")
            videoEditor = EditingFlow()
            videoEditor.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {
                                       'url': self._db_audio_path})
            videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {'url': self._db_background_music_url,
                                                                          'loop_background_music': self._db_voiceover_duration,
                                                                          "volume_percentage": 0.11})
            videoEditor.addEditingStep(EditingStep.CROP_1920x1080, {
                                       'url': self._db_background_trimmed})
            videoEditor.addEditingStep(EditingStep.ADD_SUBSCRIBE_ANIMATION)

            if self._db_watermark:
                videoEditor.addEditingStep(EditingStep.ADD_WATERMARK, {
                                           'text': self._db_watermark})
            
            caption_type = EditingStep.ADD_CAPTION_ARABIC if self._db_language == Language.ARABIC.value else EditingStep.ADD_CAPTION 
            for timing, text in self._db_timed_captions:
                videoEditor.addEditingStep(caption_type, {'text': text.upper(),
                                                                     'set_time_start': timing[0],
                                                                     'set_time_end': timing[1]})
            if self._db_num_images:
                for timing, image_url in self._db_timed_image_urls:
                    videoEditor.addEditingStep(EditingStep.SHOW_IMAGE, {'url': image_url,
                                                                        'set_time_start': timing[0],
                                                                        'set_time_end': timing[1]})

            videoEditor.renderVideo(outputPath, logger=self.logger)

        self._db_video_path = outputPath

    def _addYoutubeMetadata(self):
        
        self._db_yt_title, self._db_yt_description = gpt_yt.generate_title_description_dict(self._db_script)

        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        newFileName = f"videos/{date_str} - " + \
            re.sub(r"[^a-zA-Z0-9 '\n\.]", '', self._db_yt_title)

        shutil.move(self._db_video_path, newFileName+".mp4")
        with open(newFileName+".txt", "w", encoding="utf-8") as f:
            f.write(
                f"---Youtube title---\n{self._db_yt_title}\n---Youtube description---\n{self._db_yt_description}")
        self._db_video_path = newFileName+".mp4"
        self._db_ready_to_upload = True
