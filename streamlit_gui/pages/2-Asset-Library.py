import os
import re
import shutil

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from streamlit_gui.ui_components_html import StreamlitComponentsHTML
from shortGPT.config.asset_db import AssetDatabase

st.set_page_config(
    page_title="Assets",
    page_icon="📁",
    layout="wide"
)

StreamlitComponentsHTML.add_logo("assets/img/logo.png", st)


class AssetLibrary:
    def __init__(self):
        pass

    def create_ui(self):
        '''Create the asset library UI'''
        st.title("Asset library")
        accordion = st.expander("➕ Add your own local assets or from Youtube", False)

        with accordion:
            remote = "Add youtube video / audio"
            local = "Add local video / audio / image"
            assetFlows = st.radio("Select mode", [remote, local], format_func=lambda x: x)

            if assetFlows == remote:
                asset_name = st.text_input("Name (required)")
                asset_type = st.radio("Type", ["background video", "background music"])
                youtube_url = st.text_input("URL (https://youtube.com/xyz)")
                add_youtube_link = st.button("ADD")
                if add_youtube_link:
                    self.__verify_and_add_youtube_asset(asset_name, youtube_url, asset_type)

            if assetFlows == local:
                local_upload_name = st.text_input("Name (required)")
                upload_type = st.radio("Type", ["background video", "background music", "image"])
                uploaded_file = st.file_uploader("Upload File", type=["mp4", "mp3", "jpg", "png", "wav", "ogg"])
                upload_button = st.button("ADD")
                if upload_button and uploaded_file is not None:
                    self.__verify_and_upload_local_asset(upload_type, local_upload_name, uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            # Data table
            data = self.__fulfill_df()
            # Configure grid options using GridOptionsBuilder
            builder = GridOptionsBuilder.from_dataframe(data)
            builder.configure_pagination(enabled=False)
            builder.configure_selection(selection_mode='single', use_checkbox=False)
            grid_options = builder.build()
            return_value = AgGrid(data, gridOptions=grid_options, height=500, width='100%')

        with col2:
            if return_value['selected_rows']:
                item_name = return_value['selected_rows'][0]['name']
                item_source = return_value['selected_rows'][0]['source']
                item_type = return_value['selected_rows'][0]['type']
                item_link = return_value['selected_rows'][0]['link']

                st.write("Selected asset preview:")
                self.__get_asset_embed(item_link)
            else:
                st.write("Last added asset preview:")
                item_link = data.iloc[0]['link']
                self.__get_asset_embed(data, 0)
            delete_button = st.button("🗑️ Delete")
            if delete_button:
                self.__delete_clicked(item_name)
                # force refresh the page
                st.experimental_rerun()

    def __fulfill_df(self):
        '''Get the dataframe of assets'''
        return AssetDatabase.get_df()

    def __verify_youtube_asset_inputs(self, asset_name, yt_url, type):
        if not asset_name or not re.match("^[A-Za-z0-9 _-]*$", asset_name):
            raise ValueError('Invalid asset name. Please provide a valid name that you will recognize (Only use letters and numbers)')
        if not yt_url.startswith("https://youtube.com/") and not yt_url.startswith("https://www.youtube.com/"):
            raise ValueError('Invalid YouTube URL. Please provide a valid URL.')
        if AssetDatabase.asset_exists(asset_name):
            raise ValueError('An asset already exists with this name, please choose a different name.')

    def __validate_asset_name(self, asset_name):
        '''Validate asset name'''
        if not asset_name or not re.match("^[A-Za-z0-9 _-]*$", asset_name):
            raise ValueError('Invalid asset name. Please provide a valid name that you will recognize (Only use letters and numbers)')
        if AssetDatabase.asset_exists(asset_name):
            raise ValueError('An asset already exists with this name, please choose a different name.')

    def __validate_youtube_url(self, yt_url):
        '''Validate YouTube URL'''
        if not yt_url.startswith("https://youtube.com/") and not yt_url.startswith("https://www.youtube.com/"):
            raise ValueError('Invalid YouTube URL. Please provide a valid URL.')

    def __verify_and_add_youtube_asset(self, asset_name, yt_url, type):
        '''Verify and add a youtube asset to the database'''
        self.__validate_asset_name(asset_name)
        self.__validate_youtube_url(yt_url)
        return self.__add_youtube_asset(asset_name, yt_url, type)

    def __add_youtube_asset(self, asset_name, yt_url, type):
        '''Add a youtube asset'''
        AssetDatabase.add_remote_asset(asset_name, type, yt_url)

    def __get_first_preview(self):
        '''Get the first preview'''
        return self.__get_asset_embed(AssetDatabase.get_df(), 0)

    def __delete_clicked(self, item_name):
        '''Delete an asset'''
        AssetDatabase.remove_asset(item_name)

    def __get_asset_embed(self, item_link, embed_height: int = 300, embed_width: int = 300) -> str:
        asset_link = item_link
        if 'youtube.com' in asset_link:
            print(f"Loading youtube video: {asset_link}")
            st.video(asset_link)
        elif 'public/' in asset_link:
            asset_link = os.path.abspath(asset_link)
            file_ext = asset_link.split('.')[-1]
            if file_ext in ['mp3', 'wav', 'ogg']:
                print(f"Loading audio: {asset_link}")
                st.audio(asset_link, format=file_ext, start_time=0)
            elif file_ext in ['mp4', 'webm', 'ogg', 'mov']:
                print(f"Loading video: {asset_link}")
                st.video(asset_link)
            elif file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                print(f"Loading image: {asset_link}")
                from PIL import Image
                st.image(Image.open(asset_link), width=embed_width)

    @staticmethod
    def __clean_filename(filename):
        '''Clean the filename'''
        return re.sub('[\\\\/:*?"<>|]', '', filename)

    def __verify_and_upload_local_asset(self, upload_type, upload_name, uploaded_file):
        '''Verify and upload a local asset to the database'''
        self.__validate_asset_name(upload_name)
        return self.__upload_local_asset(upload_type, upload_name, uploaded_file)

    def __upload_local_asset(self, upload_type, upload_name, uploaded_file):
        '''Upload a local asset to the database'''
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        # ... (uploading part needs to be done according to your storage system)
        raise NotImplementedError("Uploading local assets is not yet implemented")


AssetLibrary().create_ui()
