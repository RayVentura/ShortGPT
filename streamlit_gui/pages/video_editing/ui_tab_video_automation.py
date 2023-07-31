import time
import traceback
from enum import Enum

import streamlit as st
from click import progressbar
from streamlit_chat import message as streamlit_chat_message

from streamlit_gui.ui_components_html import StreamlitComponentsHTML
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


class VideoAutomationUI:
    def __init__(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.voice_module = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False

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

    def make_video(self, script, voice_module, isVertical):
        videoEngine = ContentVideoEngine(voiceModule=voice_module, script=script, isVerticalFormat=isVertical)
        num_steps = videoEngine.get_total_steps()
        progress_counter = 0

        def logger(prog_str):
            progressbar.progress(progress_counter, f"Creating video - {progress_counter} - {prog_str}")

        videoEngine.set_logger(logger)
        for step_num, step_info in videoEngine.makeContent():
            progressbar.progress(progress_counter, f"Creating video - {progress_counter} - {step_info}")
            progress_counter += 1

        video_path = videoEngine.get_video_output_path()
        return video_path

    def reset_components(self):
        return self.initialize_conversation()

    def chatbot_conversation(self):
        def respond(message):
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
                    st.write("Your video is being made now! 🎬")
                    try:
                        video_path = self.make_video(self.script, self.voice_module, self.isVertical)
                        file_name = video_path.split("/")[-1].split("\\")[-1]
                        self.video_html = f'''
                            <div style="display: flex; flex-direction: column; align-items: center;">
                                <video width="{600}" height="{300}" style="max-height: 100%;" controls>
                                    <source src="{video_path}" type="video/mp4">
                                    Your browser does not support the video tag.
                                </video>
                                <a href="{video_path}" download="{file_name}" style="margin-top: 10px;">
                                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                                </a>
                            </div>'''
                        st.markdown(self.video_html, unsafe_allow_html=True)
                        bot_message = "Your video is completed !🎬. Scroll down below to open its file location."
                    except Exception as e:
                        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
                        st.write("We encountered an error while making this video ❌")
                        st.write(error_name)
                        st.write(traceback_str)

                else:
                    self.state = Chatstate.ASK_CORRECTION  # change self.state to ASK_CORRECTION
                    bot_message = "Explain me what you want different in the script"
            elif self.state == Chatstate.ASK_CORRECTION:  # new self.state
                self.script = self.correct_script(self.script, message)  # call generateScript with correct=True
                self.state = Chatstate.ASK_SATISFACTION
                bot_message = f"📝 Here is your corrected script: \n\n--------------\n{self.script}\n\n・Are you satisfied with the script and ready to proceed with creating the video? Please respond with 'YES' or 'NO'. 👍👎"
            return bot_message

        return respond


    def initialize_conversation(self):
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False

        prompt = "🤖 Welcome to ShortGPT! 🚀 I'm a python framework aiming to simplify and automate your video editing tasks.\nLet's get started! 🎥🎬\n\n Do you want your video to be in landscape or vertical format? (landscape OR vertical)"
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": prompt})
        st.session_state.setdefault(
            'past',
            ['plan text with line break',
             'play the song "Dancing Vegetables"',
             'show me image of cat',
             'and video of it',
             'show me some markdown sample',
             'table in markdown']
        )
        st.session_state.setdefault(
            'generated',
            [{'type': 'normal', 'data': 'Line 1 \n Line 2 \n Line 3'},
             {'type': 'normal', 'data': f'<audio controls src="{prompt}"></audio>'}]
        )

    def reset_conversation(self):
        '''
        Reset the conversation to the initial state
        '''
        self.state = Chatstate.ASK_ORIENTATION
        self.isVertical = None
        self.language = None
        self.script = ""
        self.video_html = ""
        self.videoVisible = False

    def create_ui(self):
        '''
        Create the video automation UI
        '''

        def on_input_change():
            user_input = st.session_state.user_input
            st.session_state.past.append(user_input)
            st.session_state.generated.append("The messages from Bot\nWith new line")

        def on_btn_click():
            del st.session_state.past[:]
            del st.session_state.generated[:]

        st.title("Video Automation")

        chat_placeholder = st.empty()
        self.initialize_conversation()
        with chat_placeholder.container():
            for i in range(len(st.session_state['generated'])):
                streamlit_chat_message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
                streamlit_chat_message(
                    st.session_state['generated'][i]['data'],
                    key=f"{i}",
                    allow_html=True,
                    is_table=True if st.session_state['generated'][i]['type'] == 'table' else False
                )

            st.button("Clear message", on_click=on_btn_click)

        with st.container():
            st.text_input("User Input:", on_change=on_input_change, key="user_input")

            """
            while True:
                message = st.text_input("You: ", key="chatbot_input2")
                respond = self.chatbot_conversation()
                bot_message = respond(message)
                st.write("Bot: " + bot_message)

                if self.state == Chatstate.MAKE_VIDEO:
                    try:
                        video_path = self.make_video(self.script, self.voice_module, self.isVertical)
                        st.video(video_path)
                        st.write("Your video is completed !🎬. Scroll down below to open its file location.")
                    except Exception as e:
                        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                        error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
                        errorVisible = True
                        st_content_automation_ui_error_template = StreamlitComponentsHTML.get_html_error_template()
                        error_html = st_content_automation_ui_error_template.format(error_message=error_name, stack_trace=traceback_str)
                        st.write("We encountered an error while making this video ❌")
                        st.write(error_html)
                    break
                """
