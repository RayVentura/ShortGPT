import gradio as gr

from gui.asset_library_ui import AssetLibrary
from gui.config_ui import ConfigUI
from gui.content_automation_ui import GradioContentAutomationUI
from gui.gradio_components_html import GradioComponentsHTML
from shortGPT.utils.cli import CLI


class BaseUI:
    '''Base class for the GUI. This class is responsible for creating the UI and launching the server.'''
    max_choices = 20
    ui_asset_dataframe = gr.Dataframe(interactive=False)
    LOGO_PATH = "http://localhost:31415/file=public/logo.png"
    LOGO_DIM = 64

    def __init__(self, ui_name='default'):
        self.ui_name = ui_name
        self.content_automation = None
        self.asset_library_ui = None
        self.config_ui = None

    def create_interface(self):
        raise NotImplementedError


class ShortGptUI(BaseUI):
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

            gradio_content_automation_ui = GradioContentAutomationUI(shortGptUI)
            self.content_automation = gradio_content_automation_ui.create_content_automation()
            self.asset_library_ui = AssetLibrary().create_asset_library_ui()
            self.config_ui = ConfigUI().create_config_ui()
        return shortGptUI

    def launch(self):
        '''Launch the server'''
        shortGptUI = self.create_interface()
        shortGptUI.queue(concurrency_count=5, max_size=20).launch(server_port=31415, height=1000, share=self.colab)


if __name__ == "__main__":
    app = ShortGptUI()
    app.launch()
