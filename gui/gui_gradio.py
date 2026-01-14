import os

import gradio as gr

from gui.content_automation_ui import GradioContentAutomationUI
from gui.ui_abstract_base import AbstractBaseUI
from gui.ui_components_html import GradioComponentsHTML
from gui.ui_tab_asset_library import AssetLibrary
from gui.ui_tab_config import ConfigUI
from shortGPT.utils.cli import CLI


def is_running_in_docker():
    return os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)


class ShortGptUI(AbstractBaseUI):

    def __init__(self, colab=False):
        super().__init__(ui_name='gradio_shortgpt')
        self.colab = colab or is_running_in_docker()
        CLI.display_header()

    def create_interface(self):
        '''Create Gradio interface'''
        with gr.Blocks(title="ShortGPT Demo") as shortGptUI:
            with gr.Row(variant='compact'):
                gr.HTML(GradioComponentsHTML.get_html_header())

            self.content_automation = GradioContentAutomationUI(shortGptUI).create_ui()
            self.asset_library_ui = AssetLibrary().create_ui()
            self.config_ui = ConfigUI().create_ui()
        return shortGptUI

    def launch(self):
        '''Launch the server'''
        shortGptUI = self.create_interface()
        if not getattr(self, 'colab', False):
                    print("\n\n********************* STARTING SHORGPT **********************")
                    print("\nShortGPT is running here 👉 http://localhost:31415\n")
                    print("********************* STARTING SHORGPT **********************\n\n")
        shortGptUI.queue().launch(server_port=31415, allowed_paths=["public/","videos/","fonts/"], share=self.colab, server_name="0.0.0.0", theme=gr.themes.Default(spacing_size=gr.themes.sizes.spacing_sm))



if __name__ == "__main__":
    app = ShortGptUI()
    app.launch()


import signal

def signal_handler(sig, frame):
    print("Closing Gradio server...")
    import gradio as gr
    gr.close_all()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)