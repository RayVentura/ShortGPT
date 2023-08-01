import os
import time
import traceback

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES, Language)
from shortGPT.engine.multi_language_translation_engine import MultiLanguageTranslationEngine


class VideoTranslationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.eleven_language_choices = [lang.value.upper() for lang in ELEVEN_SUPPORTED_LANGUAGES]
        self.embedHTML = '<div style="display: flex; overflow-x: auto; gap: 20px;">'
        self.progress_counter = 0
        self.video_translation_ui = None

    def create_ui(self):
        with gr.Row(visible=False) as video_translation_ui:
            with gr.Column():
                videoType = gr.Radio(["Youtube link", "Video file"], label="Input your video", value="Youtube link", interactive=True)
                video_path = gr.Video(source="upload", interactive=True, width=533.33, height=300, visible=False)
                yt_link = gr.Textbox(label="Youtube link (https://youtube.com/xyz): ", interactive=True, visible=False)
                videoType.change(lambda x: (gr.update(visible=x == "Video file"), gr.update(visible=x == "Youtube link")), [videoType], [video_path, yt_link])
                tts_engine = gr.Radio([AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS], label="Text to speech engine", value=AssetComponentsUtils.ELEVEN_TTS, interactive=True)

                with gr.Column(visible=True) as eleven_tts:
                    language_eleven = gr.CheckboxGroup(self.eleven_language_choices, label="Language", value="ENGLISH", interactive=True)
                    AssetComponentsUtils.voiceChoiceTranslation()
                with gr.Column(visible=False) as edge_tts:
                    language_edge = gr.CheckboxGroup([lang.value.upper() for lang in Language], label="Language", value="ENGLISH", interactive=True)
                tts_engine.change(lambda x: (gr.update(visible=x == AssetComponentsUtils.ELEVEN_TTS), gr.update(visible=x == AssetComponentsUtils.EDGE_TTS)), tts_engine, [eleven_tts, edge_tts])

                useCaptions = gr.Checkbox(label="Caption video", value=False)

                translateButton = gr.Button(label="Create Shorts")

                generation_error = gr.HTML(visible=False)
                video_folder = gr.Button("📁", visible=True)
                output = gr.HTML()

            video_folder.click(lambda _: AssetComponentsUtils.start_file(os.path.abspath("videos/")))
            translateButton.click(self.inspect_create_inputs, inputs=[videoType, video_path, yt_link, tts_engine, language_eleven, language_edge, ], outputs=[generation_error]).success(self.translate_video, inputs=[
                videoType, yt_link, video_path, tts_engine, language_eleven, language_edge, useCaptions, AssetComponentsUtils.voiceChoiceTranslation()
            ], outputs=[output, video_folder, generation_error])
        self.video_translation_ui = video_translation_ui
        return self.video_translation_ui

    def translate_video(self, videoType, yt_link, video_path, tts_engine, language_eleven, language_edge, use_captions: bool, voice: str, progress=gr.Progress()) -> str:
        if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
            languages = [Language(lang.lower().capitalize()) for lang in language_eleven]
        elif tts_engine == AssetComponentsUtils.EDGE_TTS:
            languages = [Language(lang.lower().capitalize()) for lang in language_edge]
        try:
            for i, language in enumerate(languages):
                if tts_engine == AssetComponentsUtils.EDGE_TTS:
                    voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])
                if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                    voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
                content_translation_engine = MultiLanguageTranslationEngine(voiceModule=voice_module, src_url=yt_link if videoType == "Youtube link" else video_path, target_language=language, use_captions=use_captions)
                num_steps = content_translation_engine.get_total_steps()
                def logger(prog_str):
                    progress(self.progress_counter / (num_steps), f"Translating your video ({i+1}/{len(languages)}) - {prog_str}")
                content_translation_engine.set_logger(logger)

                for step_num, step_info in content_translation_engine.makeContent():
                    progress(self.progress_counter / (num_steps), f"Translating your video ({i+1}/{len(languages)}) - {step_info}")
                    self.progress_counter += 1

                video_path = content_translation_engine.get_video_output_path()
                current_url = self.shortGptUI.share_url+"/" if self.shortGptUI.share else self.shortGptUI.local_url
                file_url_path = f"{current_url}file={video_path}"
                file_name = video_path.split("/")[-1].split("\\")[-1]
                self.embedHTML += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <video width="{500}"  style="max-height: 100%;" controls>
                        <source src="{file_url_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                        <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                    </a>
                </div>'''
                yield "<div>"+self.embedHTML + '</div>', gr.Button.update(visible=True), gr.update(visible=False)

        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print("Error", traceback_str)
            error_html = GradioComponentsHTML.get_html_error_template().format(error_message=error_name, stack_trace=traceback_str)
            return self.embedHTML + '</div>', gr.Button.update(visible=True), gr.update(value=error_html, visible=True)

    def inspect_create_inputs(self, videoType, video_path, yt_link,  tts_engine, language_eleven, language_edge,):
        supported_extensions = ['.mp4', '.avi', '.mov']  # Add more supported video extensions if needed
        print(videoType, video_path, yt_link)
        if videoType == "Youtube link":
            if not yt_link.startswith("https://youtube.com/") and not yt_link.startswith("https://www.youtube.com/"):
                raise gr.Error('Invalid YouTube URL. Please provide a valid URL. Link example: https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        else:
            if not video_path or not os.path.exists(video_path):
                raise gr.Error('You must drag and drop a valid video file.')

            file_ext = os.path.splitext(video_path)[-1].lower()
            if file_ext not in supported_extensions:
                raise gr.Error('Invalid video file. Supported video file extensions are: {}'.format(', '.join(supported_extensions)))
        if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
            if not len(language_eleven) >0:
                raise gr.Error('You must select one or more target languages')
        if tts_engine == AssetComponentsUtils.EDGE_TTS:
            if not len(language_edge) >0:
                raise gr.Error('You must select one or more target languages')
        return gr.update(visible=False)


def update_progress(progress, progress_counter, num_steps, num_shorts, stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        dynamic = int(3649 * elapsed_time / 600)
        progress(progress_counter / (num_steps * num_shorts), f"Rendering progress - {dynamic}/3649")
        time.sleep(0.1)  # update every 0.1 second
