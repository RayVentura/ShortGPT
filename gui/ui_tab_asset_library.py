import os
import re
import shutil

import gradio as gr

from gui.asset_components import AssetComponentsUtils
from gui.ui_abstract_component import AbstractComponentUI
from shortGPT.config.asset_db import AssetDatabase


class AssetLibrary(AbstractComponentUI):
    def __init__(self):
        pass

    def create_ui(self):
        '''Create the asset library UI'''
        with gr.Tab("Asset library") as asset_library_ui:
            with gr.Column():
                with gr.Accordion("➕ Add your own local assets or from Youtube", open=False) as accordion:
                    remote = "Add youtube video / audio"
                    local = "Add local video / audio / image    "
                    assetFlows = gr.Radio([remote, local], label="", value=remote)
                    with gr.Column(visible=True) as youtubeFlow:
                        asset_name = gr.Textbox(label="Name (required)")
                        asset_type = gr.Radio(["background video", "background music"], value="background video", label="Type")
                        youtube_url = gr.Textbox(label="URL (https://youtube.com/xyz)")
                        add_youtube_link = gr.Button("ADD")

                    with gr.Column(visible=False) as localFileFlow:
                        local_upload_name = gr.Textbox(label="Name (required)")
                        upload_type = gr.Radio(["background video", "background music", "image"], value="background video", interactive=True, label="Type")
                        video_upload = gr.Video(visible=True, source="upload", type="filepath", interactive=True)
                        audio_upload = gr.Audio(visible=False, source="upload", type="filepath", interactive=True)
                        image_upload = gr.Image(visible=False, source="upload", type="filepath", interactive=True)
                        upload_button = gr.Button("ADD")
                        upload_type.change(lambda x: (gr.update(visible='video' in x),
                                                      gr.update(visible=any(type in x for type in ['audio', 'music'])),
                                                      gr.update(visible=x == 'image')),
                                           [upload_type], [video_upload, audio_upload, image_upload])
                    assetFlows.change(lambda x: (gr.update(visible=x == remote), gr.update(visible=x == local)), [assetFlows], [youtubeFlow, localFileFlow])
                with gr.Row():
                    with gr.Column(scale=3):
                        asset_dataframe_ui = gr.Dataframe(self.__fulfill_df, interactive=False)
                        video_choise = gr.Radio(["background video", "background music"], value="background video", label="Type")
                    with gr.Column(scale=2):
                        gr.Markdown("Preview")
                        asset_preview_ui = gr.HTML(self.__get_first_preview)
                        delete_button = gr.Button("🗑️ Delete", scale=0, variant="primary")
                        delete_button.click(self.__delete_clicked, [delete_button], [asset_dataframe_ui, asset_preview_ui, delete_button, AssetComponentsUtils.background_video_checkbox(), AssetComponentsUtils.background_music_checkbox()])
                        asset_dataframe_ui.select(self.__preview_asset, [asset_dataframe_ui], [asset_preview_ui, delete_button])

                add_youtube_link.click(
                    self.__verify_youtube_asset_inputs, [asset_name, youtube_url, asset_type], []).success(self.__add_youtube_asset, [asset_name, youtube_url, asset_type], [asset_dataframe_ui, asset_preview_ui, delete_button, accordion, AssetComponentsUtils.background_video_checkbox(), AssetComponentsUtils.background_music_checkbox()]).success(lambda: gr.update(open=False), [accordion])

                upload_button.click(
                    self.__verify_and_upload_local_asset, [upload_type, local_upload_name, video_upload, audio_upload, image_upload, ], []).success(self.__upload_local_asset, [upload_type, local_upload_name, video_upload, audio_upload, image_upload, ], [asset_dataframe_ui, asset_preview_ui, delete_button, accordion, AssetComponentsUtils.background_video_checkbox(), AssetComponentsUtils.background_music_checkbox()]).success(lambda: gr.update(open=False), [accordion])

        return asset_library_ui

    def __fulfill_df(self):
        '''Get the dataframe of assets'''
        return AssetDatabase.get_df()

    def __verify_youtube_asset_inputs(self, asset_name, yt_url, type):
        if not asset_name or not re.match("^[A-Za-z0-9 _-]*$", asset_name):
            raise gr.Error('Invalid asset name. Please provide a valid name that you will recognize (Only use letters and numbers)')
        if not yt_url.startswith("https://youtube.com/") and not yt_url.startswith("https://www.youtube.com/"):
            raise gr.Error('Invalid YouTube URL. Please provide a valid URL.')
        if AssetDatabase.asset_exists(asset_name):
            raise gr.Error('An asset already exists with this name, please choose a different name.')

    def __validate_asset_name(self, asset_name):
        '''Validate asset name'''
        if not asset_name or not re.match("^[A-Za-z0-9 _-]*$", asset_name):
            raise gr.Error('Invalid asset name. Please provide a valid name that you will recognize (Only use letters and numbers)')
        if AssetDatabase.asset_exists(asset_name):
            raise gr.Error('An asset already exists with this name, please choose a different name.')

    def __validate_youtube_url(self, yt_url):
        '''Validate YouTube URL'''
        if not yt_url.startswith("https://youtube.com/") and not yt_url.startswith("https://www.youtube.com/"):
            raise gr.Error('Invalid YouTube URL. Please provide a valid URL.')

    def __verify_and_add_youtube_asset(self, asset_name, yt_url, type):
        '''Verify and add a youtube asset to the database'''
        self.__validate_asset_name(asset_name)
        self.__validate_youtube_url(yt_url)
        return self.__add_youtube_asset(asset_name, yt_url, type)

    def __add_youtube_asset(self, asset_name, yt_url, type):
        '''Add a youtube asset'''
        AssetDatabase.add_remote_asset(asset_name, type, yt_url)
        latest_df = AssetDatabase.get_df()
        return gr.DataFrame.update(value=latest_df), gr.HTML.update(value=self.__get_asset_embed(latest_df, 0)),\
            gr.update(value=f"🗑️ Delete {latest_df.iloc[0]['name']}"),\
            gr.Accordion.update(open=False),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundVideoChoices(), interactive=True),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundMusicChoices(), interactive=True)

    def __get_first_preview(self):
        '''Get the first preview'''
        return self.__get_asset_embed(AssetDatabase.get_df(), 0)

    def __delete_clicked(self, button_name):
        '''Delete an asset'''
        asset_name = button_name.split("🗑️ Delete ")[-1]
        AssetDatabase.remove_asset(asset_name)
        data = AssetDatabase.get_df()
        if len(data) > 0:
            return gr.update(value=data),\
                gr.HTML.update(value=self.__get_asset_embed(data, 0)),\
                gr.update(value=f"🗑️ Delete {data.iloc[0]['name']}"),\
                gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundVideoChoices(), interactive=True),\
                gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundMusicChoices(), interactive=True)
        return gr.Dataframe.update(value=data),\
            gr.HTML.update(visible=True),\
            gr.Button.update(value="🗑️ Delete"),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundVideoChoices(), interactive=True),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundMusicChoices(), interactive=True)

    def __preview_asset(self, data, evt: gr.SelectData):
        '''Preview the asset with the given name'''
        html_embed = self.__get_asset_embed(data, evt.index[0])
        return gr.HTML.update(value=html_embed), gr.update(value=f"🗑️ Delete {data.iloc[evt.index[0]]['name']}")

    def __get_asset_embed(self, data, row):
        '''Get the embed html for the asset at the given row'''
        embed_height = 300
        embed_width = 300
        asset_link = data.iloc[row]['link']

        if 'youtube.com' in asset_link:
            asset_link_split = asset_link.split('?v=')
            if asset_link_split[0] == asset_link:
                asset_link_split = asset_link.split('/')
                # if the last character is a /, remove it
                if asset_link_split[-1] == '/':
                    asset_link_split = asset_link_split[:-1]
                asset_link_split = asset_link_split[-1]
            else:
                asset_link_split = asset_link_split[-1]
            asset_link = f"https://youtube.com/embed/{asset_link_split}"
            embed_html = f'<iframe width="{embed_width}" height="{embed_height}" src="{asset_link}"></iframe>'
        elif 'public/' in asset_link:
            asset_link = f"http://localhost:31415/file={asset_link}"
            file_ext = asset_link.split('.')[-1]

            if file_ext in ['mp3', 'wav', 'ogg']:
                audio_type = 'audio/mpeg' if file_ext == 'mp3' else f'audio/{file_ext}'
                embed_html = f'<audio controls><source src="{asset_link}" type="{audio_type}">Your browser does not support the audio tag.</audio>'
            elif file_ext in ['mp4', 'webm', 'ogg', 'mov']:
                video_type = 'video/mp4' if file_ext == 'mp4' else f'video/{file_ext}'
                embed_html = f'<video width="{embed_width}" height="{embed_height}" style="max-height: 100%;" controls><source src="{asset_link}" type="{video_type}">Your browser does not support the video tag.</video>'
            elif file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                embed_html = f'<img src="{asset_link}" width="{embed_width}" height="{embed_height}">'
            else:
                embed_html = 'Unsupported file type'
        return embed_html

    @staticmethod
    def __clean_filename(filename):
        '''Clean the filename'''
        return re.sub('[\\\\/:*?"<>|]', '', filename)

    def __verify_and_upload_local_asset(self, upload_type, upload_name, video_path, audio_path, image_path):
        '''Verify and upload a local asset to the database'''
        self.__validate_asset_name(upload_name)
        path_dict = {
            'video': video_path,
            'background video': video_path,
            'audio': audio_path,
            'background music': audio_path,
            'image': image_path
        }
        if not os.path.exists(path_dict[upload_type]):
            raise gr.Error(f'The file does not exist at the given path.')
        return self.__upload_local_asset(upload_type, upload_name, video_path, audio_path, image_path)

    def __upload_local_asset(self, upload_type, upload_name, video_path, audio_path, image_path):
        '''Upload a local asset to the database'''
        path_dict = {
            'video': video_path,
            'background video': video_path,
            'audio': audio_path,
            'background music': audio_path,
            'image': image_path
        }
        new_path = "public/" + self.__clean_filename(upload_name) + "." + path_dict[upload_type].split(".")[-1]
        shutil.move(path_dict[upload_type], new_path)
        AssetDatabase.add_local_asset(upload_name, upload_type, new_path)
        latest_df = AssetDatabase.get_df()
        return gr.DataFrame.update(value=latest_df), gr.HTML.update(value=self.__get_asset_embed(latest_df, 0)),\
            gr.update(value=f"🗑️ Delete {latest_df.iloc[0]['name']}"),\
            gr.Accordion.update(open=False),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundVideoChoices(), interactive=True),\
            gr.CheckboxGroup.update(choices=AssetComponentsUtils.getBackgroundMusicChoices(), interactive=True)
