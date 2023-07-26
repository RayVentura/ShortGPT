from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import Language
from shortGPT.engine.content_short_engine import ContentShortEngine
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep, Flow
from shortGPT.gpt import reddit_gpt, gpt_voice
import os


class RedditShortEngine(ContentShortEngine):
    # Mapping of variable names to database paths
    def __init__(self,voiceModule: VoiceModule, background_video_name: str, background_music_name: str,short_id="",
                 num_images=None, watermark=None, language:Language = Language.ENGLISH):
        super().__init__(short_id=short_id, short_type="reddit_shorts", background_video_name=background_video_name, background_music_name=background_music_name,
                 num_images=num_images, watermark=watermark, language=language, voiceModule=voiceModule)
    
    def __generateRandomStory(self):
        question = reddit_gpt.getInterestingRedditQuestion()
        script = reddit_gpt.createRedditScript(question)
        return script

    def __getRealisticStory(self, max_tries=3):
        current_realistic_score = 0
        current_try = 0
        current_generated_script = ""
        while (current_realistic_score < 6 and current_try < max_tries) or len(current_generated_script) > 1000:
            new_script = self.__generateRandomStory()
            new_realistic_score = reddit_gpt.getRealisticness(new_script)
            if new_realistic_score >= current_realistic_score:
                current_generated_script = new_script
                current_realistic_score = new_realistic_score
            current_try += 1
        return current_generated_script, current_try

    def _generateScript(self):
        """
        Implements Abstract parent method to generate the script for the reddit short
        """
        self.logger("Generating reddit question & entertaining story")
        self._db_script, _ = self.__getRealisticStory(max_tries=1)
        self._db_reddit_question = reddit_gpt.getQuestionFromThread(
            self._db_script)

    def _prepareCustomAssets(self):
        """
        Override parent method to generate custom reddit image asset
        """
        self.logger("Rendering short: (3/4) preparing custom reddit image...")
        self.verifyParameters(question=self._db_reddit_question,)
        title, header, n_comments, n_upvotes = reddit_gpt.generateRedditPostMetadata(
            self._db_reddit_question)
        imageEditingEngine = EditingEngine()
        imageEditingEngine.ingestFlow(Flow.WHITE_REDDIT_IMAGE_FLOW, {
            "username_text": header,
            "ncomments_text": n_comments,
            "nupvote_text": n_upvotes,
            "question_text": title
        })
        imageEditingEngine.renderImage(
            self.dynamicAssetDir+"redditThreadImage.png")
        self._db_reddit_thread_image = self.dynamicAssetDir+"redditThreadImage.png"
    
    def _editAndRenderShort(self):
        """
        Override parent method to customize video rendering sequence by adding a Reddit image
        """
        self.verifyParameters(
                              voiceover_audio_url=self._db_audio_path,
                              video_duration=self._db_background_video_duration, 
                              music_url=self._db_background_music_url)
        
        outputPath = self.dynamicAssetDir+"rendered_video.mp4"
        if not (os.path.exists(outputPath)):
            self.logger("Rendering short: Starting automated editing...")
            videoEditor = EditingEngine()
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
            videoEditor.addEditingStep(EditingStep.ADD_REDDIT_IMAGE, {
                                       'url': self._db_reddit_thread_image})
            
            caption_type = EditingStep.ADD_CAPTION_SHORT_ARABIC if self._db_language == Language.ARABIC.value else EditingStep.ADD_CAPTION_SHORT 
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

