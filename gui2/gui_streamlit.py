import os
import subprocess

import streamlit as st

from gui2.ui_abstract_base import AbstractBaseUI
from shortGPT.utils.cli import CLI


class ShortGptUI(AbstractBaseUI):
    '''Class for the GUI. This class is responsible for creating the UI and launching the server.'''

    def __init__(self, colab=False):
        super().__init__(ui_name='streamlit_shortgpt')
        self.colab = colab
        CLI.display_header()

    def create_interface(self):
        raise Exception("Please use streamlit run gui2/Welcome.py")

    def launch(self):
        '''Launch the server'''
        self.create_interface()


if __name__ == "__main__":
    app = ShortGptUI()
    app.launch()
