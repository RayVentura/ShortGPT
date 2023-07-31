
import streamlit as st

from streamlit_gui.ui_components_html import StreamlitComponentsHTML

st.set_page_config(
    page_title="ShortGPT - video automation",
    page_icon="🎬",
    layout="wide"
)
StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)


class WelcomePageUI():

    def __init__(self):
        super().__init__()
        self.title = "Home"
        self.icon = "🏠"
        self.description = "Home"
        self.page_config = {
            "page_title": self.title,
            "page_icon": self.icon
        }

    def create_ui(self):
        StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)
        st.markdown(""""
        <div align="center">
            <img src="https://github.com/RayVentura/ShortGPT/assets/121462835/083c8dc3-bac5-42c1-a08d-3ff9686d18c5" alt="ShortGPT-logo" style="border-radius: 20px;" width="22%"/>
        </div>
        <div align="center">
            <h1>🚀🎬 ShortGPT</h1>
        </div>
        <div align="center">
            <h4>⚡ Automating video and short content creation with AI ⚡</h4>
        </div>
        """, unsafe_allow_html=True)


WelcomePageUI().create_ui()
