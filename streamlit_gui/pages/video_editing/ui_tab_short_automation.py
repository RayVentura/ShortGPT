import traceback

import streamlit as st

from streamlit_gui.asset_components import AssetComponentsUtils
from streamlit_gui.ui_components_html import StreamlitComponentsHTML
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.api_db import ApiKeyManager
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       ELEVEN_SUPPORTED_LANGUAGES, Language)
from shortGPT.engine.facts_short_engine import FactsShortEngine
from shortGPT.engine.reddit_short_engine import RedditShortEngine


class ShortAutomationUI:
    def __init__(self):
        self.progress_counter = 0

    def create_ui(self):
        '''Create the asset library UI'''
        st.title("Short Automation")
        print("Loading Short Automation UI...")
        numShorts = st.number_input("Number of shorts", min_value=1, value=1)
        short_type_radio_items = ["Reddit Story shorts", "Historical Facts shorts", "Scientific Facts shorts", "Custom Facts shorts"]
        short_type_radio_btn = st.radio("Type of shorts generated", short_type_radio_items, format_func=lambda x: x)
        facts_subject = st.text_input("Write a subject for your facts (example: Football facts)") if short_type_radio_btn == "Custom Facts shorts" else None

        tts_engine_radio_items = [AssetComponentsUtils.ELEVEN_TTS, AssetComponentsUtils.EDGE_TTS]
        tts_engine_radio_btn = st.radio("Text to speech engine", tts_engine_radio_items)
        self.tts_engine = tts_engine_radio_btn

        language_eleven_radio_btn = None
        language_edge_radio_btn = None
        language_eleven_voice_selected = None

        if tts_engine_radio_btn == AssetComponentsUtils.ELEVEN_TTS:
            language_eleven_radio_items = [lang.value for lang in ELEVEN_SUPPORTED_LANGUAGES]
            language_eleven_radio_btn = st.radio("Language", language_eleven_radio_items)
            language_eleven_voice_selected = st.selectbox(
                "Elevenlabs voice",
                options=AssetComponentsUtils.getElevenlabsVoices(),
                index=AssetComponentsUtils.getElevenlabsVoices().index("Antoni")
            )
        elif tts_engine_radio_btn == AssetComponentsUtils.EDGE_TTS:
            language_edge_radio_items = [lang.value.upper() for lang in Language]
            language_edge_radio_btn = st.selectbox("Language", language_edge_radio_items)

        useImages = st.checkbox("Use images", value=True)
        numImages_radio_items = [5, 10, 25]
        numImages_radio_btn = st.radio("Number of images per short", numImages_radio_items) if useImages else None

        addWatermark = st.checkbox("Add watermark")
        watermark = st.text_input("Watermark (your channel name)") if addWatermark else None

        background_video_list = st.multiselect(
            "Choose background video",
            options=AssetComponentsUtils.getBackgroundVideoChoices(),
            key="background_video_checkbox"
        )

        background_music_list = st.multiselect(
            "Choose background music",
            options=AssetComponentsUtils.getBackgroundMusicChoices(),
            key="background_music_checkbox"
        )

        createButton = st.button("Create Shorts")
        progress_bar = st.progress(0, text="Ready for generation")
        if createButton:
            self._validate_inputs(background_video_list, background_music_list, watermark, short_type_radio_btn, facts_subject)
            self.create_short(numShorts,
                              short_type_radio_btn,
                              tts_engine_radio_btn,
                              language_eleven_radio_btn,
                              language_edge_radio_btn,
                              numImages_radio_btn,
                              watermark,
                              background_video_list,
                              background_music_list,
                              facts_subject,
                              language_eleven_voice_selected,
                              progress_bar
                              )

    def _validate_inputs(self, background_video_list, background_music_list, watermark, short_type, facts_subject):
        '''
        Inspect the inputs for creating a short
        '''
        if short_type is not None and short_type == "Custom Facts shorts":
            if not facts_subject:
                raise ValueError("Please write down your facts short's subject")
        if not background_video_list:
            raise ValueError("Please select at least one background video.")

        if not background_music_list:
            raise ValueError("Please select at least one background music.")

        if watermark is not None and watermark != "":
            if not watermark.replace(" ", "").isalnum():
                raise ValueError("Watermark should only contain letters and numbers.")
            if len(watermark) > 25:
                raise ValueError("Watermark should not exceed 25 characters.")
            if len(watermark) < 3:
                raise ValueError("Watermark should be at least 3 characters long.")

        openai_key = ApiKeyManager.get_api_key("OPENAI")
        if not openai_key:
            raise ValueError("OPENAI API key is missing. Please go to the config tab and enter the API key.")
        eleven_labs_key = ApiKeyManager.get_api_key("ELEVEN LABS")

        if self.tts_engine is not None and self.tts_engine == AssetComponentsUtils.ELEVEN_TTS and not eleven_labs_key:
            raise ValueError("ELEVEN LABS API key is missing. Please go to the config tab and enter the API key.")

    def create_short(self, numShorts, short_type, tts_engine, language_eleven, language_edge, numImages, watermark,  background_video_list, background_music_list, facts_subject, voice, progress=None):
        '''
        Create a short
        '''
        try:
            numShorts = int(numShorts)
            numImages = int(numImages) if numImages else None
            background_videos = (background_video_list * ((numShorts // len(background_video_list)) + 1))[:numShorts]
            background_musics = (background_music_list * ((numShorts // len(background_music_list)) + 1))[:numShorts]
            if tts_engine == AssetComponentsUtils.ELEVEN_TTS:
                language = Language(language_eleven.lower().capitalize())
                voice_module = ElevenLabsVoiceModule(ApiKeyManager.get_api_key('ELEVEN LABS'), voice, checkElevenCredits=True)
            elif tts_engine == AssetComponentsUtils.EDGE_TTS:
                language = Language(language_edge.lower().capitalize())
                voice_module = EdgeTTSVoiceModule(EDGE_TTS_VOICENAME_MAPPING[language]['male'])

            for i in range(numShorts):
                shortEngine = self.create_short_engine(short_type=short_type, voice_module=voice_module, language=language, numImages=numImages, watermark=watermark,
                                                       background_video=background_videos[i], background_music=background_musics[i], facts_subject=facts_subject)
                num_steps = shortEngine.get_total_steps()

                def logger(prog_str):
                    progress.progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {prog_str}")
                shortEngine.set_logger(logger)

                for step_num, step_info in shortEngine.makeContent():
                    print(step_info)
                    progress.progress(self.progress_counter / (num_steps * numShorts), f"Making short {i+1}/{numShorts} - {step_info}")
                    self.progress_counter += 1

                video_path = shortEngine.get_video_output_path()
                current_url = self.shortGptUI.share_url+"/" if self.shortGptUI.share else self.shortGptUI.local_url
                file_url_path = f"{current_url}file={video_path}"
                file_name = video_path.split("/")[-1].split("\\")[-1]
                self.embedHTML += f'''
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <video width="{250}" height="{500}" style="max-height: 100%;" controls>
                        <source src="{file_url_path}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                        <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                    </a>
                </div>'''
                st.markdown(f"## Short {i+1}/{numShorts} created!")
                st.markdown(f"### Download link: {file_url_path}")
                st.markdown(self.embedHTML, unsafe_allow_html=True)
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            error_name = type(e).__name__.capitalize() + " : " + f"{e.args[0]}"
            print("Error", traceback_str)
            error_html = StreamlitComponentsHTML.get_html_error_template().format(error_message=error_name, stack_trace=traceback_str)
            st.markdown(error_html, unsafe_allow_html=True)

    def create_short_engine(self, short_type, voice_module, language, numImages, watermark, background_video, background_music, facts_subject):
        '''
        Creates a short engine based on the short type
        '''
        print("Creating short engine")
        print(f"--> Short type: {short_type}")
        print(f"--> Voice module: {voice_module}")
        print(f"--> Language: {language}")
        print(f"--> Num images: {numImages}")
        print(f"--> Watermark: {watermark}")
        print(f"--> Background video: {background_video}")
        print(f"--> Background music: {background_music}")
        print(f"--> Facts subject: {facts_subject}")

        if short_type == "Reddit Story shorts":
            print(f"-- --> Reddit Story shorts")
            return RedditShortEngine(voice_module, background_video_name=background_video, background_music_name=background_music, num_images=numImages, watermark=watermark, language=language)
        if "fact" in short_type.lower():
            print(f"-- --> Fact Story shorts")
            if "custom" in short_type.lower():
                print(f"-- --> Fact Story shorts (custom)")
                facts_subject = facts_subject
            else:
                facts_subject = short_type
            return FactsShortEngine(voice_module, facts_type=facts_subject, background_video_name=background_video, background_music_name=background_music, num_images=50, watermark=watermark, language=language)
        raise Exception(f"Short type does not have a valid short engine: {short_type}")
