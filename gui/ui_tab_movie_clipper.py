import os
import traceback

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import Language
from shortGPT.engine.movie_clipper_engine import MovieClipperEngine


class MovieClipperUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI

    def is_key_missing(self):
        openai_key = ApiKeyManager.get_api_key("OPENAI_API_KEY")
        gemini_key = ApiKeyManager.get_api_key("GEMINI_API_KEY")
        if not openai_key and not gemini_key:
            return "Your Gemini or OpenAI key is missing. Please go to the config tab and enter the API key."
        return None

    def create_ui(self):
        with gr.Row(visible=False) as movie_clipper_ui:
            with gr.Column():
                gr.Markdown("## 🎬 MovieClipper Engine")
                gr.Markdown("Upload a video or provide a URL. The AI will detect interesting moments with dialogue/scenes and create short clips with subtitles in 16:9 format.")
                
                with gr.Row():
                    with gr.Column():
                        video_file = gr.File(
                            label="Upload Video File",
                            file_types=[".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v"],
                            type="filepath"
                        )
                        video_url = gr.Textbox(
                            label="Or Enter Video URL (YouTube, etc.)",
                            placeholder="https://youtube.com/watch?v=..."
                        )
                    
                    with gr.Column():
                        num_clips = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            label="Number of Clips to Extract"
                        )
                        min_clip_duration = gr.Slider(
                            minimum=10,
                            maximum=45,
                            value=15,
                            step=5,
                            label="Minimum Clip Duration (seconds)"
                        )
                        max_clip_duration = gr.Slider(
                            minimum=20,
                            maximum=90,
                            value=45,
                            step=5,
                            label="Maximum Clip Duration (seconds)"
                        )
                        language = gr.Dropdown(
                            choices=[lang.value for lang in Language],
                            value=Language.ENGLISH.value,
                            label="Caption Language"
                        )
                        watermark = gr.Textbox(
                            label="Watermark Text (optional)",
                            placeholder="@yourhandle"
                        )
                
                process_btn = gr.Button("🎥 Extract Clips", variant="primary")
                
                status_text = gr.Markdown("", visible=True)
                error_html = gr.HTML(visible=False)
                output_files = gr.File(
                    label="Generated Clips",
                    file_count="multiple",
                    visible=False
                )
                video_folder_btn = gr.Button("📁 Open Videos Folder", visible=False)
                
                def on_process(video_file, video_url, num_clips, min_clip_duration, max_clip_duration, language, watermark, progress=gr.Progress()):
                    try:
                        yield (
                            gr.update(value="⏳ **Starting processing...**"),
                            gr.update(visible=False),
                            gr.update(visible=False),
                            gr.update(visible=False)
                        )
                        
                        error_msg = self.is_key_missing()
                        if error_msg:
                            raise gr.Error(error_msg)
                        
                        if video_file:
                            video_path = video_file
                        elif video_url:
                            video_path = video_url
                        else:
                            raise gr.Error("Please provide a video file or URL")
                        
                        if min_clip_duration >= max_clip_duration:
                            raise gr.Error("Minimum duration must be less than maximum duration")
                        
                        lang_map = {lang.value: lang for lang in Language}
                        selected_language = lang_map.get(language, Language.ENGLISH)
                        
                        engine = MovieClipperEngine(
                            video_path=video_path,
                            num_clips=int(num_clips),
                            min_clip_duration=int(min_clip_duration),
                            max_clip_duration=int(max_clip_duration),
                            watermark=watermark if watermark else None,
                            language=selected_language
                        )
                        
                        num_steps = engine.get_total_steps()
                        
                        for step_num, step_info in engine.makeContent():
                            progress((step_num) / num_steps, step_info)
                            yield (
                                gr.update(value=f"⏳ **Step {step_num}/{num_steps}:** {step_info}"),
                                gr.update(visible=False),
                                gr.update(visible=False),
                                gr.update(visible=False)
                            )
                        
                        video_paths = engine.get_all_video_paths()
                        
                        yield (
                            gr.update(value=f"✅ **Done!** Generated {len(video_paths)} clips."),
                            gr.update(visible=False),
                            gr.update(value=video_paths, visible=True),
                            gr.update(visible=True)
                        )
                    except Exception as e:
                        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        error_name = type(e).__name__ + ": " + str(e.args[0] if e.args else e)
                        error_template = GradioComponentsHTML.get_html_error_template()
                        error_content = error_template.format(error_message=error_name, stack_trace=traceback_str)
                        yield (
                            gr.update(value="❌ **Error occurred**"),
                            gr.update(value=error_content, visible=True),
                            gr.update(visible=False),
                            gr.update(visible=False)
                        )
                
                process_btn.click(
                    on_process,
                    inputs=[video_file, video_url, num_clips, min_clip_duration, max_clip_duration, language, watermark],
                    outputs=[status_text, error_html, output_files, video_folder_btn]
                )
                
                video_folder_btn.click(
                    lambda: AssetComponentsUtils.start_file(os.path.abspath("videos/"))
                )
        
        return movie_clipper_ui
