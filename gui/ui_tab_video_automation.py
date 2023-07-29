import os
import traceback
from enum import Enum

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from gui.ui_components_html import GradioComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES, Language)
from shortGPT.engine.content_video_engine import ContentVideoEngine
from shortGPT.gpt import gpt_chat_video


class Chatstate(Enum):
    ASK_ORIENTATION = 1
    ASK_VOICE_MODULE = 2
    ASK_LANGUAGE = 3
    ASK_DESCRIPTION = 4
    GENERATE_SCRIPT = 5
    ASK_SATISFACTION = 6
    MAKE_VIDEO = 7
    ASK_CORRECTION = 8


class VideoAutomationUI(AbstractComponentUI):
    def __init__(self, shortGptUI: gr.Blocks):
        self.shortGptUI = shortGptUI
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.voice_module = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False
        self.video_automation = None
        self.chatbot = None
        self.msg = None
        self.restart_button = None
        self.video_folder = None
        self.errorHTML = None
        self.outHTML = None

    def is_key_missing(self):
        openai_key = ApiKeyManager.get_api_key("OPENAI")
        if not openai_key:
            return "Your OpenAI key is missing. Please go to the config tab and enter the API key."

        pexels_api_key = ApiKeyManager.get_api_key("PEXELS")
        if not pexels_api_key:
            return "Your Pexels API key is missing. Please go to the config tab and enter the API key."

    def generate_script(self, message, language):
        return gpt_chat_video.generateScript(message, language)

    def correct_script(self, script, correction):
        return gpt_chat_video.correctScript(script, correction)

    def make_video(self, script, voice_module, isVertical, progress):
        videoEngine = ContentVideoEngine(voiceModule=voice_module, script=script, isVerticalFormat=isVertical)
        num_steps = videoEngine.get_total_steps()
        progress_counter = 0

        def logger(prog_str):
            progress(progress_counter / (num_steps), f"Creating video - {progress_counter} - {prog_str}")
        videoEngine.set_logger(logger)
        for step_num, step_info in videoEngine.makeContent():
            progress(progress_counter / (num_steps), f"Creating video - {step_info}")
            progress_counter += 1

        video_path = videoEngine.get_video_output_path()
        return video_path

    def reset_components(self):
        return gr.Chatbot.update(value=self.initialize_conversation()), gr.update(visible=True), gr.HTML.update(value="", visible=False), gr.HTML.update(value="", visible=False)

    def chatbot_conversation(self):
        def respond(message, chat_history, progress=gr.Progress()):
            # global self.state, isVertical, voice_module, language, script, videoVisible, video_html
            error_html = ""
            errorVisible = False
            inputVisible = True
            folderVisible = False
            if self.state == Chatstate.ASK_ORIENTATION:
                errorMessage = self.is_key_missing()
                if errorMessage:
                    bot_message = errorMessage
                else:
                    self.isVertical = "vertical" in message.lower() or "short" in message.lower()
                    self.state = Chatstate.ASK_VOICE_MODULE
                    bot_message = "Which voice module do you want to use? Please type 'ElevenLabs' for high quality voice or 'EdgeTTS' for free but medium quality voice."
            elif self.state == Chatstate.ASK_VOICE_MODULE:
                if "elevenlabs" in message.lower():
                    eleven_labs_key = ApiKeyManager.get_api_key("ELEVEN LABS")
                    if not eleven_labs_key:
                        bot_message = "Your Eleven Labs API key is missing. Please go to the config tab and enter the API key."
                        return
                    self.voice_module = ElevenLabsVoiceModule
                    language_choices = [lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES]
                elif "edgetts" in message.lower():
                    self.voice_module = EdgeTTSVoiceModule
                    language_choices = [lang.value for lang in Language]
                else:
                    bot_message = "Invalid voice module. Please type 'ElevenLabs' or 'EdgeTTS'."
                    return
                self.state = Chatstate.ASK_LANGUAGE
                bot_message = f"🌐What language will be used in the video?🌐 Choose from one of these ({', '.join(language_choices)})"
            elif self.state == Chatstate.ASK_LANGUAGE:
                self.language = next((lang for lang in Language if lang.value.lower() in message.lower()), None)
                self.language = self.language if self.language else Language.ENGLISH
                if self.voice_module == ElevenLabsVoiceModule:
                    self.voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), "Antoni", checkElevenCredits=True)
                elif self.voice_module == EdgeTTSVoiceModule:
                    self.voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[self.language]['male'])
                self.state = Chatstate.ASK_DESCRIPTION
                bot_message = "Amazing 🔥 ! 📝Can you describe thoroughly the subject of your video?📝 I will next generate you a script based on that description"
            elif self.state == Chatstate.ASK_DESCRIPTION:
                self.script = self.generate_script(message, self.language.value)
                self.state = Chatstate.ASK_SATISFACTION
                bot_message = f"📝 Here is your generated script: \n\n--------------\n{self.script}\n\n・Are you satisfied with the script and ready to proceed with creating the video? Please respond with 'YES' or 'NO'. 👍👎"
            elif self.state == Chatstate.ASK_SATISFACTION:
                if "yes" in message.lower():
                    self.state = Chatstate.MAKE_VIDEO
                    inputVisible = False
                    yield gr.update(visible=False), gr.Chatbot.update(value=[[None, "Your video is being made now! 🎬"]]), gr.HTML.update(value="", visible=False), gr.HTML.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=False)
                    try:
                        video_path = self.make_video(self.script, self.voice_module, self.isVertical, progress=progress)
                        file_name = video_path.split("/")[-1].split("\\")[-1]
                        current_url = self.shortGptUI.share_url+"/" if self.shortGptUI.share else self.shortGptUI.local_url
                        file_url_path = f"{current_url}file={video_path}"
                        self.video_html = f'''
                            <div style="display: flex; flex-direction: column; align-items: center;">
                                <video width="{600}" height="{300}" style="max-height: 100%;" controls>
                                    <source src="{file_url_path}" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                                <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                                </a>
                            </div>'''
                        self.videoVisible = True
                        folderVisible = True
                        bot_message = "Your video is completed !🎬. Scroll down below to open its file location."
                    except Exception as e:
                        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
                        errorVisible = True
                        gradio_content_automation_ui_error_template = GradioComponentsHTML.get_html_error_template()
                        error_html = gradio_content_automation_ui_error_template.format(error_message=error_name, stack_trace=traceback_str)
                        bot_message = "We encountered an error while making this video ❌"
                        print("Error", traceback_str)
                        yield gr.update(visible=False), gr.Chatbot.update(value=[[None, "Your video is being made now! 🎬"]]), gr.HTML.update(value="", visible=False),
                        gr.HTML.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)

                else:
                    self.state = Chatstate.ASK_CORRECTION  # change self.state to ASK_CORRECTION
                    bot_message = "Explain me what you want different in the script"
            elif self.state == Chatstate.ASK_CORRECTION:  # new self.state
                self.script = self.correct_script(self.script, message)  # call generateScript with correct=True
                self.state = Chatstate.ASK_SATISFACTION
                bot_message = f"📝 Here is your corrected script: \n\n--------------\n{self.script}\n\n・Are you satisfied with the script and ready to proceed with creating the video? Please respond with 'YES' or 'NO'. 👍👎"
            chat_history.append((message, bot_message))
            yield gr.update(value="", visible=inputVisible), gr.Chatbot.update(value=chat_history), gr.HTML.update(value=self.video_html, visible=self.videoVisible), gr.HTML.update(value=error_html, visible=errorVisible), gr.update(visible=folderVisible), gr.update(visible=True)

        return respond

    def initialize_conversation(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False
        return [[None, "🤖 Welcome to ShortGPT! 🚀 I'm a python framework aiming to simplify and automate your video editing tasks.\nLet's get started! 🎥🎬\n\n Do you want your video to be in landscape or vertical format? (landscape OR vertical)"]]

    def reset_conversation(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False

    def create_ui(self):
        with gr.Row(visible=False) as self.video_automation:
            with gr.Column():
                self.chatbot = gr.Chatbot(self.initialize_conversation, height=365)
                self.msg = gr.Textbox()
                self.restart_button = gr.Button("Restart")
                self.video_folder = gr.Button("📁", visible=False)
                self.video_folder.click(lambda _: AssetComponentsUtils.start_file(os.path.abspath("videos/")))
                respond = self.chatbot_conversation()

            self.errorHTML = gr.HTML(visible=False)
            self.outHTML = gr.HTML(visible=False)
            self.restart_button.click(self.reset_components, [], [self.chatbot, self.msg, self.errorHTML, self.outHTML])
            self.restart_button.click(self.reset_conversation, [])
            self.msg.submit(respond, [self.msg, self.chatbot], [self.msg, self.chatbot, self.outHTML, self.errorHTML, self.video_folder, self.restart_button])
        return self.video_automation
