import gradio as gr

from gui.content_automation_ui import GradioContentAutomationUI
from gui.ui_abstract_base import AbstractBaseUI
from gui.ui_components_html import GradioComponentsHTML
from gui.ui_tab_asset_library import AssetLibrary
from gui.ui_tab_config import ConfigUI
from shortGPT.utils.cli import CLI


class ShortGptUI(AbstractBaseUI):
    '''Class for the GUI. This class is responsible for creating the UI and launching the server.'''

    def __init__(self, colab=False):
        super().__init__(ui_name='gradio_shortgpt')
        self.colab = colab
        CLI.display_header()

    def create_interface(self):
        '''Create Gradio interface'''
        with gr.Blocks(css="footer {visibility: hidden}", title="ShortGPT Demo") as shortGptUI:
            with gr.Row(variant='compact'):
                gr.HTML(GradioComponentsHTML.get_html_header())

            self.content_automation = GradioContentAutomationUI(shortGptUI).create_ui()
            self.asset_library_ui = AssetLibrary().create_ui()
            self.config_ui = ConfigUI().create_ui()
        return shortGptUI

    def launch(self):
        '''Launch the server'''
        shortGptUI = self.create_interface()
        shortGptUI.queue(concurrency_count=5, max_size=20).launch(server_port=31415, height=1000, share=self.colab)


if __name__ == "__main__":
    app = ShortGptUI()
    app.launch()
