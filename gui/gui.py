import gradio as gr
from gui.config_ui import create_config_ui
from gui.asset_library_ui import create_asset_library_ui
from gui.short_automation_ui import create_short_automation_ui
max_choices = 20
ui_asset_dataframe = gr.Dataframe(interactive=False)
    
def run_app():
    with gr.Blocks(css="footer {visibility: hidden}", title="shortGPT UI" ) as shortGptUI:
        short_automation_ui = create_short_automation_ui()
        asset_library_ui = create_asset_library_ui()
        config_ui = create_config_ui()

    shortGptUI.queue(concurrency_count=5, max_size=20).launch(server_port=31415, height=1000)

if __name__ == "__main__":
    run_app()