import gradio as gr
from gui.config_ui import create_config_ui
from gui.asset_library_ui import create_asset_library_ui
from gui.content_automation_ui import create_content_automation
max_choices = 20
ui_asset_dataframe = gr.Dataframe(interactive=False)
LOGO_PATH = "http://localhost:31415/file=public/logo.png"
LOGO_DIM = 64 
def run_app():
    with gr.Blocks(css="footer {visibility: hidden}", title="ShortGPT Demo" ) as shortGptUI:
        with gr.Row(variant='compact'):
            gr.HTML(f'''
                <div style="display: flex; align-items: center;">
                    <h1 style="margin-left: 0px; font-size: 35px;">ShortGPT</h1>
                </div>
            ''')
        content_automation = create_content_automation()
        asset_library_ui = create_asset_library_ui()
        config_ui = create_config_ui()

    shortGptUI.queue(concurrency_count=5, max_size=20).launch(server_port=31415, height=1000)

if __name__ == "__main__":
    run_app()