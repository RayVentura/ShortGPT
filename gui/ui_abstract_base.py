
import gradio as gr


class AbstractBaseUI:
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
