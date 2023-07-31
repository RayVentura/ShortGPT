import time

import streamlit as st

from streamlit_gui.asset_components import AssetComponentsUtils
from streamlit_gui.ui_components_html import StreamlitComponentsHTML
from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager

st.set_page_config(
    page_title="Configuration",
    page_icon="⚙️",
)

StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)


class ConfigUI():
    def __init__(self):
        self.api_key_manager = ApiKeyManager()
        eleven_key = self.api_key_manager.get_api_key('ELEVEN LABS')
        self.eleven_labs_api = ElevenLabsAPI(eleven_key) if eleven_key else None

    def on_show(self, button_text, textbox):
        '''Show or hide the API key'''
        if button_text == "Show":
            textbox.type = "text"
            return "Hide"
        textbox.type = "password"
        return "Show"

    def verify_eleven_key(self, eleven_key, remaining_chars):
        '''Verify the ElevenLabs API key'''
        if (eleven_key and self.api_key_manager.get_api_key('ELEVEN LABS') != eleven_key):
            try:
                self.eleven_labs_api = ElevenLabsAPI(eleven_key)
                print(self.eleven_labs_api)
                return self.eleven_labs_api.get_remaining_characters()
            except Exception as e:
                raise st.Error(e.args[0])
        return remaining_chars

    def save_keys(self, openai_key, eleven_key, pexels_key):
        '''Save the keys in the database'''
        if (self.api_key_manager.get_api_key('OPENAI') != openai_key):
            self.api_key_manager.set_api_key("OPENAI", openai_key)
        if (self.api_key_manager.get_api_key('PEXELS') != pexels_key):
            self.api_key_manager.set_api_key("PEXELS", pexels_key)
        if (self.api_key_manager.get_api_key('ELEVEN LABS') != eleven_key):
            self.api_key_manager.set_api_key("ELEVEN LABS", eleven_key)
            new_eleven_voices = AssetComponentsUtils.getElevenlabsVoices()
            return openai_key, eleven_key, pexels_key, new_eleven_voices, new_eleven_voices
        return openai_key, eleven_key, pexels_key, True, True

    def get_eleven_remaining(self,):
        '''Get the remaining characters from ElevenLabs API'''
        if (self.eleven_labs_api):
            try:
                return self.eleven_labs_api.get_remaining_characters()
            except Exception as e:
                return e.args[0]
        return ""

    def back_to_normal(self):
        '''Back to normal after 3 seconds'''
        time.sleep(3)
        return "save"

    def create_ui(self):
        '''Create the config UI'''
        st.title("Configuration")
        st.write("Here you can configure your API keys and set your configuration.")
        StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)

        openai_key = st.text_input("OPENAI API KEY", value=self.api_key_manager.get_api_key("OPENAI"), type="password")
        eleven_key = st.text_input("ELEVEN LABS API KEY", value=self.api_key_manager.get_api_key("ELEVEN LABS"), type="password")
        remaining_chars = st.text_input("ELEVEN LABS CHARACTERS REMAINING", value=self.get_eleven_remaining(), disabled=True)
        pexels_key = st.text_input("PEXELS KEY", value=self.api_key_manager.get_api_key("PEXELS"), type="password")

        save_button = st.button("Save")
        if save_button:
            try:
                save_button = "Saving..."
                remaining_chars = self.verify_eleven_key(eleven_key, remaining_chars)
                openai_key, eleven_key, pexels_key, voice_choice, voice_choice_translation = self.save_keys(openai_key, eleven_key, pexels_key)
                st.success("Keys saved successfully !")
            except Exception as e:
                st.error("Error while saving keys !")
                st.error(e.args[0])
            finally:
                save_button = self.back_to_normal()

        return openai_key, eleven_key, pexels_key, remaining_chars, save_button


ConfigUI().create_ui()
