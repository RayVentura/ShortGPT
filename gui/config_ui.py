import gradio as gr
import time
from shortGPT.config.api_db import get_api_key, set_api_key
from shortGPT.api_utils.eleven_api import getCharactersFromKey
def onShow(button_text):
    if button_text == "Show":
        return gr.Textbox.update(type="text"), gr.Button.update(value="Hide")
    return gr.Textbox.update(type="password"), gr.Button.update(value="Show")
def verify_eleven_key(eleven_key, remaining_chars):
    if (eleven_key and get_api_key('ELEVEN LABS') != eleven_key):
        try:
            return getCharactersFromKey(eleven_key)
        except Exception as e:
            raise gr.Error(e.args[0])
    return remaining_chars
def saveKeys(openai_key, eleven_key, pexels_key):
    if (get_api_key('OPENAI') != openai_key):
        set_api_key("OPENAI", openai_key)
    if (get_api_key('ELEVEN LABS') != eleven_key):
        set_api_key("ELEVEN LABS", eleven_key)
    if (get_api_key('PEXELS') != pexels_key):
        set_api_key("PEXELS", pexels_key)
    return  gr.Textbox.update(value=openai_key),\
            gr.Textbox.update(value=eleven_key),\
            gr.Textbox.update(value=pexels_key)

def getElevenRemaining(key):
    if(key):
        try:
            return getCharactersFromKey(key)
        except Exception as e:
             return e.args[0]
    return ""
def create_config_ui():
    with gr.Tab("Config") as config_ui:
        with gr.Row():
            with gr.Column():
                with gr.Row():
                        openai_textbox = gr.Textbox(value=get_api_key("OPENAI"), label=f"OPENAI API KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        show_openai_key = gr.Button("Show", size="sm", scale=1)
                        show_openai_key.click(onShow, [show_openai_key], [openai_textbox, show_openai_key])
                with gr.Row():
                        eleven_labs_textbox = gr.Textbox(value=get_api_key("ELEVEN LABS"), label=f"ELEVEN LABS API KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        eleven_characters_remaining = gr.Textbox(value=getElevenRemaining(get_api_key("ELEVEN LABS")), label=f"CHARACTERS REMAINING", show_label=True, interactive=False, type="text", scale=40)
                        show_eleven_key = gr.Button("Show", size="sm", scale=1)
                        show_eleven_key.click(onShow, [show_eleven_key], [eleven_labs_textbox, show_eleven_key])
                with gr.Row():
                        pexels_textbox = gr.Textbox(value=get_api_key("PEXELS"), label=f"PEXELS KEY", show_label=True, interactive=True, show_copy_button=True, type="password", scale=40)
                        show_pexels_key = gr.Button("Show", size="sm", scale=1)
                        show_pexels_key.click(onShow, [show_pexels_key], [pexels_textbox, show_pexels_key])
                save_button =  gr.Button("save", size="sm", scale=1)
                def back_to_normal():
                    time.sleep(3)
                    return gr.Button.update(value="save")
                save_button.click(verify_eleven_key, [eleven_labs_textbox, eleven_characters_remaining], [eleven_characters_remaining]).success(saveKeys, [openai_textbox, eleven_labs_textbox, pexels_textbox], [openai_textbox, eleven_labs_textbox, pexels_textbox])
                save_button.click(lambda _ : gr.Button.update(value="Keys Saved !"), [], [save_button])
                save_button.click(back_to_normal, [], [save_button])
    return config_ui