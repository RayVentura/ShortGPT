import traceback
import gradio as gr
from gui.asset_components import voiceChoiceTranslation, start_file, EDGE_TTS, ELEVEN_TTS
from shortGPT.config.api_db import get_api_key
from shortGPT.engine.content_translation_engine import ContentTranslationEngine
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.languages import EDGE_TTS_VOICENAME_MAPPING, ELEVEN_SUPPORTED_LANGUAGES, Language
import time
eleven_language_choices = [lang.value.upper() for lang in ELEVEN_SUPPORTED_LANGUAGES]
import gradio as gr
import os
import time

ERROR_TEMPLATE = """
<div style='text-align: center; background: #9fcbc3; color: #3f4039; 
padding: 20px; border-radius: 5px; margin: 10px;'>
    <h2 style='margin: 0;'>ERROR | {error_message}</h2>
    <p style='margin: 10px 0;'>Traceback Info : {stack_trace}</p>
    <p style='margin: 10px 0;'>If the problem persists, don't hesitate to 
contact our support. We're here to assist you.</p>
    <a href='https://discord.gg/qn2WJaRH' target='_blank' 
style='background: #3f4039; color: #fff; border: none; padding: 10px 20px; 
border-radius: 5px; cursor: pointer; text-decoration: none;'>Get Help on Discord</a>
</div>"""


def create_video_translation_ui(shortGptUI: gr.Blocks):
    def translate_video(
            videoType,
            yt_link,
            video_path,
            tts_engine, 
            language_eleven,
            language_edge,
            use_captions: bool,
            voice: str,
            progress=gr.Progress()):
        if tts_engine == ELEVEN_TTS:
            language = Language(language_eleven.lower().capitalize())
            voice_module = ElevenLabsVoiceModule(get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
        elif tts_engine == EDGE_TTS:
            language = Language(language_edge.lower().capitalize())
            voice_module = EdgeTTSVoiceModule( EDGE_TTS_VOICENAME_MAPPING[language]['male'])
        print(EDGE_TTS_VOICENAME_MAPPING[language]['male'], Language)
        embedHTML = '<div style="display: flex; overflow-x: auto; gap: 20px;">'
        progress_counter = 0
        try:
            content_translation_engine = ContentTranslationEngine(voiceModule=voice_module, src_url=yt_link if videoType=="Youtube link" else video_path, target_language=language, use_captions=use_captions )
            num_steps = content_translation_engine.get_total_steps()
            def logger(prog_str):
                progress(progress_counter / (num_steps),f"Translating your video - {prog_str}")
            content_translation_engine.set_logger(logger)
            
            for step_num, step_info in content_translation_engine.makeContent():
                progress(progress_counter / (num_steps),f"Translating your video - {step_info}")
                progress_counter += 1

            video_path = content_translation_engine.get_video_output_path()
            current_url = shortGptUI.share_url+"/" if shortGptUI.share else shortGptUI.local_url
            file_url_path = f"{current_url}file={video_path}"
            file_name = video_path.split("/")[-1].split("\\")[-1]
            embedHTML += f'''
            <div style="display: flex; flex-direction: column; align-items: center;">
                <video width="{500}"  style="max-height: 100%;" controls>
                    <source src="{file_url_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                </a>
            </div>'''
            return embedHTML + '</div>', gr.Button.update(visible=True), gr.update(visible=False)

        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize()+ " : " +f"{e.args[0]}"
            print("Error", traceback_str)
            return embedHTML + '</div>', gr.Button.update(visible=True), gr.update(value=ERROR_TEMPLATE.format(error_message=error_name, stack_trace=traceback_str), visible=True)
        
        
        
        
    with gr.Row(visible=False) as video_translation_ui:
        with gr.Column():
            videoType = gr.Radio(["Youtube link", "Video file"], label="Input your video", value="Video file", interactive=True)
            video_path = gr.Video(source="upload", interactive=True, width=533.33, height=300)
            yt_link = gr.Textbox(label="Youtube link (https://youtube.com/xyz): ", interactive=True, visible=False)
            videoType.change(lambda x: (gr.update(visible= x == "Video file"), gr.update(visible= x == "Youtube link")), [videoType], [video_path, yt_link] )
            tts_engine = gr.Radio([ELEVEN_TTS, EDGE_TTS], label="Text to speech engine", value=ELEVEN_TTS, interactive=True)
            
            with gr.Column(visible=True) as eleven_tts:
                language_eleven = gr.Radio(eleven_language_choices, label="Language", value="ENGLISH", interactive=True)
                voiceChoiceTranslation.render()
            with gr.Column(visible=False) as edge_tts:
                language_edge = gr.Dropdown([lang.value.upper() for lang in Language], label="Language", value="ENGLISH", interactive=True)
            tts_engine.change(lambda x: (gr.update(visible= x==ELEVEN_TTS), gr.update(visible= x==EDGE_TTS)), tts_engine, [eleven_tts, edge_tts])
            
            useCaptions = gr.Checkbox(label="Caption video", value=False)

            translateButton = gr.Button(label="Create Shorts")

            generation_error = gr.HTML(visible=False)
            video_folder = gr.Button("📁", visible=True)
            output = gr.HTML()

        video_folder.click(lambda _: start_file(os.path.abspath("videos/")))
        translateButton.click(inspect_create_inputs, inputs=[videoType, video_path, yt_link,  ], outputs=[generation_error]).success(translate_video, inputs=[
            videoType, yt_link, video_path, tts_engine, language_eleven,language_edge, useCaptions, voiceChoiceTranslation
        ], outputs=[output, video_folder, generation_error])
    return video_translation_ui



def inspect_create_inputs(videoType, video_path, yt_link):
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
    return gr.update(visible=False)

def update_progress(progress, progress_counter, num_steps, num_shorts, stop_event):
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        dynamic = int(3649 * elapsed_time / 600)
        progress(progress_counter / (num_steps * num_shorts), f"Rendering progress - {dynamic}/3649")
        time.sleep(0.1)  # update every 0.1 second
