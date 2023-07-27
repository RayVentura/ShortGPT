import gradio as gr

from gui.short_automation_ui import ShortAutomationUI
from gui.video_automation_ui import VideoAutomationUI
from gui.video_translation_ui import VideoTranslationUI


class GradioContentAutomationUI:
    def __init__(self, shortGPTUI):
        self.shortGPTUI = shortGPTUI
        self.content_automation_ui = None

    def create_content_automation(self):
        with gr.Tab("Content Automation") as self.content_automation_ui:
            gr.Markdown("# 🏆 Content Automation 🚀")
            gr.Markdown("## Choose your desired automation task.")
            choice = gr.Radio(['🎬 Automate the creation of shorts', '🎞️ Automate a video with stock assets', '📹 Automate video translation'], label="Choose an option")
            video_automation_ui = VideoAutomationUI(self.shortGPTUI).create_video_automation_ui()
            short_automation_ui = ShortAutomationUI(self.shortGPTUI).create_short_automation_ui()
            video_translation_ui = VideoTranslationUI(self.shortGPTUI).create_video_translation_ui()
            choice.change(lambda x: (gr.update(visible=x == choice.choices[1]), gr.update(visible=x == choice.choices[0]), gr.update(
                visible=x == choice.choices[2])), [choice], [video_automation_ui, short_automation_ui, video_translation_ui])
        return self.content_automation_ui
