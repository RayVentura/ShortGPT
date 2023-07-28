import time

import gradio as gr

from gui.asset_components import (getElevenlabsVoices, voiceChoice,
                                  voiceChoiceTranslation)
from shortGPT.api_utils.eleven_api import ElevenLabsAPI
from shortGPT.config.api_db import ApiKeyManager


class ConfigUI:
    def __init__(self):
        self.api_key_manager = ApiKeyManager()
        eleven_key = self.api_key_manager.get_api_key('ELEVEN LABS')
        self.eleven_labs_api = ElevenLabsAPI(eleven_key) if eleven_key else None

    def on_show(self, button_text, textbox, button):
        '''Show or hide the API key'''
        if button_text == "Show":
            return gr.Textbox.update(type="text"), gr.Button.update(value="Hide")
        return gr.Textbox.update(type="password"), gr.Button.update(value="Show")

    def verify_eleven_key(self, eleven_key, remaining_chars):
        '''Verify the ElevenLabs API key'''
        if (eleven_key and self.api_key_manager.get_api_key('ELEVEN LABS') != eleven_key):
            try:
                self.eleven_labs_api = ElevenLabsAPI(eleven_key)
                print(self.eleven_labs_api)
                return self.eleven_labs_api.get_remaining_characters()
            except Exception as e:
                raise gr.Error(e.args[0])
        return remaining_chars

    def save_keys(self, openai_key, eleven_key, pexels_key):
        '''Save the keys in the database'''
        if (self.api_key_manager.get_api_key('OPENAI') != openai_key):
            self.api_key_manager.set_api_key("OPENAI", openai_key)
        if (self.api_key_manager.get_api_key('PEXELS') != pexels_key):
            self.api_key_manager.set_api_key("PEXELS", pexels_key)
        if (self.api_key_manager.get_api_key('ELEVEN LABS') != eleven_key):
            self.api_key_manager.set_api_key("ELEVEN LABS", eleven_key)
            new_eleven_voices = getElevenlabsVoices()
            return gr.Textbox.update(value=openai_key),\
                gr.Textbox.update(value=eleven_key),\
                gr.Textbox.update(value=pexels_key),\
                gr.Radio.update(choices=new_eleven_voices),\
                gr.Radio.update(choices=new_eleven_voices)

        return gr.Textbox.update(value=openai_key),\
            gr.Textbox.update(value=eleven_key),\
            gr.Textbox.update(value=pexels_key),\
            gr.Radio.update(visible=True),\
            gr.Radio.update(visible=True)

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
        return gr.Button.update(value="save")

    def create_config_ui(self):
        '''Create the config UI'''
        with gr.Tab("Config") as config_ui:
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        openai_textbox = gr.Textbox(value=self.api_key_manager.get_api_key("OPENAI"), label=f"OPENAI API KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        show_openai_key = gr.Button("Show", size="sm", scale=1)
                        show_openai_key.click(self.on_show, [show_openai_key], [openai_textbox, show_openai_key])
                    with gr.Row():
                        eleven_labs_textbox = gr.Textbox(value=self.api_key_manager.get_api_key("ELEVEN LABS"), label=f"ELEVEN LABS API KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        eleven_characters_remaining = gr.Textbox(value=self.get_eleven_remaining(), label=f"CHARACTERS REMAINING", show_label=True, interactive=False, type="text", scale=40)
                        show_eleven_key = gr.Button("Show", size="sm", scale=1)
                        show_eleven_key.click(self.on_show, [show_eleven_key], [eleven_labs_textbox, show_eleven_key])
                    with gr.Row():
                        pexels_textbox = gr.Textbox(value=self.api_key_manager.get_api_key("PEXELS"), label=f"PEXELS KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        show_pexels_key = gr.Button("Show", size="sm", scale=1)
                        show_pexels_key.click(self.on_show, [show_pexels_key], [pexels_textbox, show_pexels_key])
                    save_button = gr.Button("save", size="sm", scale=1)
                    save_button.click(self.verify_eleven_key, [eleven_labs_textbox, eleven_characters_remaining], [eleven_characters_remaining]).success(
                        self.save_keys, [openai_textbox, eleven_labs_textbox, pexels_textbox], [openai_textbox, eleven_labs_textbox, pexels_textbox, voiceChoice, voiceChoiceTranslation])
                    save_button.click(lambda _: gr.Button.update(value="Keys Saved !"), [], [save_button])
                    save_button.click(self.back_to_normal, [], [save_button])
        return config_ui
