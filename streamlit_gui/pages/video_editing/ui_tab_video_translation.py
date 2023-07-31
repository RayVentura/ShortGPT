import traceback

import streamlit as st

from streamlit_gui.asset_components import AssetComponentsUtils
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES, Language)
from shortGPT.engine.content_translation_engine import ContentTranslationEngine


class VideoTranslationUI():
    def __init__(self):
        self.eleven_language_choices = [lang.value.upper() for lang in ELEVEN_SUPPORTED_LANGUAGES]
        self.embedHTML = '<div style="display: flex; overflow-x: auto; gap: 20px;">'
        self.progress_counter = 0
        self.video_translation_ui = None

    def create_ui(self):
        videoType = st.radio("Input your video", ["Youtube link", "Video file"], index=1)
        if videoType == "Youtube link":
            yt_link = st.text_input("Youtube link (https://youtube.com/xyz): ", key="yt_link")
        else:
            video_path = st.file_uploader("Upload video file", type=["mp4", "avi", "mov"])

        tts_engine = st.radio("Text to speech engine", [AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS], index=0, key="tts_engine")

        if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
            language_eleven = st.radio("Language", self.eleven_language_choices, index=0, key="language_eleven")
            voice = st.selectbox(
                "Elevenlabs voice",
                options=AssetComponentsUtils.getElevenlabsVoices(),
                index=AssetComponentsUtils.getElevenlabsVoices().index("Antoni"),
                key="voice_eleven_translator"
            )  # Assuming this is a function that returns the voice choice
        else:
            language_edge = st.selectbox("Language", [lang.value.upper() for lang in Language], index=0, key="language_edge")

        useCaptions = st.checkbox("Caption video", key="use_captions")
        translateButton = st.button("Translate video", key="translate_button")
        progress_bar = st.progress(0, text="Ready for generation")
        if translateButton:
            if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language(language_eleven.lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language(language_edge.lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])
            print(EDGE_TTS_VOICENAME_MAPPING[language]['male'], Language)
            try:
                use_captions: bool = useCaptions
                content_translation_engine = ContentTranslationEngine(voiceModule=voice_module, src_url=yt_link if videoType == "Youtube link" else video_path, target_language=language, use_captions=use_captions)
                num_steps = content_translation_engine.get_total_steps()

                def logger(prog_str):
                    progress_bar.progress(self.progress_counter / (num_steps), prog_str)
                content_translation_engine.set_logger(logger)

                for step_num, step_info in content_translation_engine.makeContent():
                    progress_bar.progress(self.progress_counter / (num_steps), step_info)
                    self.progress_counter += 1

                video_path = content_translation_engine.get_video_output_path()
                file_name = video_path.split("/")[-1].split("\\")[-1]
                self.embedHTML += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <a href="{video_path}" download="{file_name}" style="margin-top: 10px;">
                        <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                    </a>
                </div>'''
                col1, col2 = st.columns(2)
                with col1:
                    vid_download_button = st.markdown(self.embedHTML, unsafe_allow_html=True)
                with col2:
                    my_new_vid = st.video(video_path)

            except Exception as e:
                traceback_str = ''.join(traceback.format_tb(e.__traceback__))
                error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
                print("Error", traceback_str)
                st.write(error_name)
                st.write(traceback_str)
