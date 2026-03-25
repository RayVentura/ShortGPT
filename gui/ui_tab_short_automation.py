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
                                       ELEVEN_SUPPORTED_LANGUAGES,
                                       LANGUAGE_ACRONYM_MAPPING,
                                       Language)
from shortGPT.engine.facts_short_engine import FactsShortEngine
from shortGPT.engine.reddit_short_engine import RedditShortEngine
from shortGPT.api_utils.upload_post_api import UploadPostAPI


class ShortAutomationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.embedHTML = '<div style="display: flex; overflow-x: auto; gap: 20px;">'
        self.progress_counter = 0
        self.short_automation = None

    def create_ui(self):
        with gr.Row(visible=False) as short_automation:
            with gr.Column():
                numShorts = gr.Number(label="Number of shorts", minimum=1, value=1)
                short_type = gr.Radio(["Reddit Story shorts", "Historical Facts shorts", "Scientific Facts shorts", "Custom Facts shorts"], label="Type of shorts generated", value="Reddit Story shorts", interactive=True)
                facts_subject = gr.Textbox(label="Write a subject for your facts (example: Football facts)", interactive=True, visible=False)
                short_type.change(lambda x: gr.update(visible=x == "Custom Facts shorts"), [short_type], [facts_subject])
                tts_engine = gr.Radio([AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS], label="Text to speech engine", value=AssetComponentsUtils.EDGE_TTS, interactive=True)
                self.tts_engine = tts_engine.value
                with gr.Column(visible=False) as eleven_tts:
                    language_eleven = gr.Radio([lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES], label="Language", value="English", interactive=True)
                    voice_eleven = AssetComponentsUtils.voiceChoice(provider=AssetComponentsUtils.ELEVEN_TTS)
                with gr.Column(visible=True) as edge_tts:
                    language_edge = gr.Dropdown([lang.value.upper() for lang in Language], label="Language", value="ENGLISH", interactive=True)
                def tts_engine_change(x):
                    self.tts_engine = x
                    return gr.update(visible=x == AssetComponentsUtils.ELEVEN_TTS), gr.update(visible=x == AssetComponentsUtils.EDGE_TTS)
                tts_engine.change(tts_engine_change, tts_engine, [eleven_tts, edge_tts])

                useImages = gr.Checkbox(label="Use images", value=True)
                numImages = gr.Radio([5, 10, 25], value=10, label="Number of images per short", visible=True, interactive=True)
                useImages.change(lambda x: gr.update(visible=x), useImages, numImages)

                addWatermark = gr.Checkbox(label="Add watermark")
                watermark = gr.Textbox(label="Watermark (your channel name)", visible=False)
                addWatermark.change(lambda x: gr.update(visible=x), [addWatermark], [watermark])

                # Upload-Post cross-posting option
                crosspost_enabled = gr.Checkbox(label="📱 Cross-post to TikTok/Instagram (via Upload-Post)", value=False)
                with gr.Column(visible=False) as crosspost_options:
                    crosspost_platforms = gr.CheckboxGroup(
                        ["tiktok", "instagram"], 
                        label="Platforms", 
                        value=["tiktok", "instagram"]
                    )
                    crosspost_caption = gr.Textbox(
                        label="Caption (optional - will use video title if empty)",
                        placeholder="Your caption here... #shorts #viral",
                        lines=2
                    )
                crosspost_enabled.change(lambda x: gr.update(visible=x), [crosspost_enabled], [crosspost_options])

                AssetComponentsUtils.background_video_checkbox()
                AssetComponentsUtils.background_music_checkbox()
                createButton = gr.Button("Create Shorts")

                generation_error = gr.HTML(visible=False)
                video_folder = gr.Button("📁", visible=True)
                output = gr.HTML('<div style="min-height: 80px;"></div>')

            video_folder.click(lambda _: AssetComponentsUtils.start_file(os.path.abspath("videos/")))

            createButton.click(self.inspect_create_inputs, inputs=[AssetComponentsUtils.background_video_checkbox(), AssetComponentsUtils.background_music_checkbox(), watermark, short_type, facts_subject, crosspost_enabled], outputs=[generation_error]).success(self.create_short, inputs=[
                numShorts,
                short_type,
                tts_engine,
                language_eleven,
                language_edge,
                numImages,
                watermark,
                AssetComponentsUtils.background_video_checkbox(),
                AssetComponentsUtils.background_music_checkbox(),
                facts_subject,
                voice_eleven,
                crosspost_enabled,
                crosspost_platforms,
                crosspost_caption,
            ], outputs=[output, video_folder, generation_error])
        self.short_automation = short_automation
        return self.short_automation

    def crosspost_video(self, video_path: str, title: str, platforms: list, custom_caption: str = None):
        """Cross-post video to TikTok/Instagram via Upload-Post API."""
        api_key = ApiKeyManager.get_api_key("UPLOAD_POST_API_KEY")
        username = ApiKeyManager.get_api_key("UPLOAD_POST_USERNAME")
        
        if not api_key or not username:
            return None, "Upload-Post API key or username not configured"
        
        caption = custom_caption if custom_caption else title
        
        try:
            upload_post = UploadPostAPI(api_key, username)
            result = upload_post.upload_video(
                video_path=video_path,
                title=caption,
                platforms=platforms
            )
            
            if result.get('success'):
                return result.get('request_id'), None
            else:
                return None, result.get('error', 'Unknown error')
        except Exception as e:
            return None, str(e)

    def create_short(self, numShorts, short_type, tts_engine, language_eleven, language_edge, numImages, watermark, background_video_list, background_music_list, facts_subject, voice_eleven, crosspost_enabled, crosspost_platforms, crosspost_caption, progress=gr.Progress()):
        '''Creates a short'''

        try:
            numShorts = int(numShorts)
            numImages = int(numImages) if numImages else None
            background_videos = (background_video_list * ((numShorts // len(background_video_list)) + 1))[:numShorts]
            background_musics = (background_music_list * ((numShorts // len(background_music_list)) + 1))[:numShorts]
            if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language(language_eleven.lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVENLABS_API_KEY'), voice_eleven, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language(language_edge.lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])
            for i in range(numShorts):
                shortEngine = self.create_short_engine(short_type=short_type, voice_module=voice_module, language=language, numImages=numImages, watermark=watermark,
                                                       background_video=background_videos[i], background_music=background_musics[i], facts_subject=facts_subject)
                num_steps = shortEngine.get_total_steps()

                def logger(prog_str):
                    progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {prog_str}")
                shortEngine.set_logger(logger)

                for step_num, step_info in shortEngine.makeContent():
                    print(step_num, step_info,self.progress_counter )
                    progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {step_info}")
                    self.progress_counter += 1

                video_path = shortEngine.get_video_output_path()
                current_url = self.shortGptUI.share_url+"/" if self.shortGptUI.share else self.shortGptUI.local_url
                file_url_path = f"{current_url}gradio_api/file={video_path}"
                file_name = video_path.split("/")[-1].split("\\")[-1]
                
                # Cross-post to TikTok/Instagram if enabled
                crosspost_status = ""
                if crosspost_enabled and crosspost_platforms:
                    progress(0.95, f"Cross-posting to {', '.join(crosspost_platforms)}...")
                    request_id, error = self.crosspost_video(
                        video_path=video_path,
                        title=file_name.replace('.mp4', ''),
                        platforms=crosspost_platforms,
                        custom_caption=crosspost_caption if crosspost_caption else None
                    )
                    if request_id:
                        crosspost_status = f'<p style="color: green; font-size: 0.9em;">✅ Cross-posted to {", ".join(crosspost_platforms)}</p>'
                    else:
                        crosspost_status = f'<p style="color: orange; font-size: 0.9em;">⚠️ Cross-post failed: {error}</p>'
                
                self.embedHTML += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <video width="{250}" height="{500}" style="max-height: 100%;" controls>
                        <source src="{file_url_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                        <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                    </a>
                    {crosspost_status}
                </div>'''
                yield self.embedHTML + '</div>', gr.update(visible=True), gr.update(visible=False)
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print("Error", traceback_str)
            error_html = GradioComponentsHTML.get_html_error_template().format(error_message=error_name, stack_trace=traceback_str)
            yield self.embedHTML + '</div>', gr.update(visible=True), gr.update(value=error_html, visible=True)

    def inspect_create_inputs(self, background_video_list, background_music_list, watermark, short_type, facts_subject, crosspost_enabled, progress=gr.Progress()):
        if short_type == "Custom Facts shorts":
            if not facts_subject:
                raise gr.Error("Please write down your facts short's subject")
        if not background_video_list:
            raise gr.Error("Please select at least one background video.")

        if not background_music_list:
            raise gr.Error("Please select at least one background music.")

        if watermark != "":
            if not watermark.replace(" ", "").isalnum():
                raise gr.Error("Watermark should only contain letters and numbers.")
            if len(watermark) > 25:
                raise gr.Error("Watermark should not exceed 25 characters.")
            if len(watermark) < 3:
                raise gr.Error("Watermark should be at least 3 characters long.")

        openai_key = ApiKeyManager.get_api_key("OPENAI_API_KEY")
        gemini_key = ApiKeyManager.get_api_key("GEMINI_API_KEY")
        if not openai_key and not gemini_key:
            raise gr.Error("GEMINI OR OPENAI API key is missing. Please go to the config tab and enter the API key.")
        eleven_labs_key = ApiKeyManager.get_api_key("ELEVENLABS_API_KEY")
        if self.tts_engine == AssetComponentsUtils.ELEVEN_TTS and not eleven_labs_key:
            raise gr.Error("ELEVENLABS_API_KEY API key is missing. Please go to the config tab and enter the API key.")
        
        # Check Upload-Post credentials if cross-posting is enabled
        if crosspost_enabled:
            upload_post_key = ApiKeyManager.get_api_key("UPLOAD_POST_API_KEY")
            upload_post_user = ApiKeyManager.get_api_key("UPLOAD_POST_USERNAME")
            if not upload_post_key or not upload_post_user:
                raise gr.Error("Upload-Post API key or username is missing. Please go to the config tab and enter them, or disable cross-posting.")
        
        return gr.update(visible=False)

    def create_short_engine(self, short_type, voice_module, language, numImages, watermark, background_video, background_music, facts_subject):
        if short_type == "Reddit Story shorts":
            return RedditShortEngine(voice_module, background_video_name=background_video, background_music_name=background_music, num_images=numImages, watermark=watermark, language=language)
        if "fact" in short_type.lower():
            if "custom" in short_type.lower():
                facts_subject = facts_subject
            else:
                facts_subject = short_type
            return FactsShortEngine(voice_module, facts_type=facts_subject, background_video_name=background_video, background_music_name=background_music, num_images=numImages, watermark=watermark, language=language)
        raise gr.Error(f"Short type does not have a valid short engine: {short_type}")
