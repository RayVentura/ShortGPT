import numpy as np
import streamlit as st

from streamlit_gui.pages.video_editing.ui_tab_short_automation import ShortAutomationUI
from streamlit_gui.pages.video_editing.ui_tab_video_automation import VideoAutomationUI
from streamlit_gui.pages.video_editing.ui_tab_video_translation import \
    VideoTranslationUI
from streamlit_gui.ui_components_html import StreamlitComponentsHTML

st.set_page_config(
    page_title="Video Engine",
    page_icon="🎬",
    layout="wide"
)
StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)

st.write("# Video Engine 🎬")
st.write("## Welcome to the Video Engine! 🚀")
st.write("### 🏆 Content Automation 🚀")
st.write("Choose your desired automation task.")

tab1, tab2, tab3 = st.tabs(["🎬 Automate the creation of shorts", "🎞️ Automate a video with stock assets", "📹 Automate video translation"])

with tab1:
    ShortAutomationUI().create_ui()
with tab2:
    VideoAutomationUI().create_ui()
with tab3:
    VideoTranslationUI().create_ui()
