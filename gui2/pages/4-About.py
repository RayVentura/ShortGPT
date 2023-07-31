import streamlit as st

from gui2.ui_components_html import StreamlitComponentsHTML

st.set_page_config(
    page_title="Abput",
    page_icon="👋",
)
st.write("# Welcome to Streamlit! 👋")

StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)
