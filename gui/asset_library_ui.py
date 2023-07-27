import re

import gradio as gr

from gui.asset_components import (background_music_checkbox,
                                  background_video_checkbox,
                                  getBackgroundMusicChoices,
                                  getBackgroundVideoChoices)
from shortGPT.config.asset_db import AssetDatabase


class AssetLibrary:
    def __init__(self):
        pass

    def create_asset_library_ui(self):
        '''Create the asset library UI'''
        with gr.Tab("Asset library") as asset_library_ui:
            with gr.Column():
                with gr.Accordion("Add your own video / audio / image", open=False) as accordion:
                    with gr.Column(visible=True):
                        asset_name = gr.Textbox(label="Name (required)")
                        asset_type = gr.Radio(["background video", "background music"], value="background video", label="Type")
                        youtube_url = gr.Textbox(label="URL (https://youtube.com/xyz)")
                        add_youtube_link = gr.Button("ADD")
                with gr.Row():
                    with gr.Column(scale=3):
                        asset_dataframe_ui = gr.Dataframe(self.fulfill_df, interactive=False)
                    with gr.Column(scale=2):
                        gr.Markdown("Preview")
                        asset_preview_ui = gr.HTML(self._get_first_preview)
                        delete_button = gr.Button("🗑️ Delete", scale=0, variant="primary")
                        delete_button.click(self.delete_clicked, [delete_button], [asset_dataframe_ui, asset_preview_ui, delete_button, background_video_checkbox, background_music_checkbox])
                        asset_dataframe_ui.select(self.preview_asset, [asset_dataframe_ui], [asset_preview_ui, delete_button])
                add_youtube_link.click(self.verify_youtube_asset_inputs, [asset_name, youtube_url, asset_type], []).success(self.add_youtube_asset, [asset_name, youtube_url,
                                                                                                                                                     asset_type], [asset_dataframe_ui, asset_preview_ui, delete_button, accordion, background_video_checkbox, background_music_checkbox])
        return asset_library_ui

    def fulfill_df(self):
        '''Get the asset dataframe'''
        return AssetDatabase.get_df()

    def verify_youtube_asset_inputs(self, asset_name, yt_url, type):
        if not asset_name or not re.match("^[A-Za-z0-9 _-]*$", asset_name):
            raise gr.Error('Invalid asset name. Please provide a valid name that you will recognize (Only use letters and numbers)')
        if not yt_url.startswith("https://youtube.com/") and not yt_url.startswith("https://www.youtube.com/"):
            raise gr.Error('Invalid YouTube URL. Please provide a valid URL.')
        if AssetDatabase.asset_exists(asset_name):
            raise gr.Error('An asset already exists with this name, please choose a different name.')

    def add_youtube_asset(self, asset_name, yt_url, type):
        '''Add a youtube asset'''
        AssetDatabase.add_remote_asset(asset_name, type, yt_url)
        latest_df = AssetDatabase.get_df()
        return gr.DataFrame.update(value=latest_df), gr.HTML.update(value=self.get_asset_embed(latest_df, 0)),\
            gr.update(value=f"🗑️ Delete {latest_df.iloc[0]['name']}"),\
            gr.Accordion.update(open=False),\
            gr.CheckboxGroup.update(choices=getBackgroundVideoChoices(), interactive=True),\
            gr.CheckboxGroup.update(choices=getBackgroundMusicChoices(), interactive=True)

    def _get_first_preview(self):
        '''Get the first preview'''
        return self.get_asset_embed(AssetDatabase.get_df(), 0)

    def delete_clicked(self, button_name):
        '''Delete an asset'''
        asset_name = button_name.split("🗑️ Delete ")[-1]
        AssetDatabase.remove_asset(asset_name)
        data = AssetDatabase.get_df()
        if len(data) > 0:
            return gr.update(value=data),\
                gr.HTML.update(value=self.get_asset_embed(data, 0)),\
                gr.update(value=f"🗑️ Delete {data.iloc[0]['name']}"),\
                gr.CheckboxGroup.update(choices=getBackgroundVideoChoices(), interactive=True),\
                gr.CheckboxGroup.update(choices=getBackgroundMusicChoices(), interactive=True)
        return gr.Dataframe.update(value=data),\
            gr.HTML.update(visible=True),\
            gr.Button.update(value="🗑️ Delete"),\
            gr.CheckboxGroup.update(choices=getBackgroundVideoChoices(), interactive=True),\
            gr.CheckboxGroup.update(choices=getBackgroundMusicChoices(), interactive=True)

    def preview_asset(self, data, evt: gr.SelectData):
        '''Preview an asset'''
        html_embed = self.get_asset_embed(data, evt.index[0])
        return gr.HTML.update(value=html_embed), gr.update(value=f"🗑️ Delete {data.iloc[evt.index[0]]['name']}")

    def get_asset_embed(self, data, row):
        '''Get the asset embed'''
        embed_height = 300
        embed_width = 300
        asset_link = data.iloc[row]['link']

        if 'youtube.com' in asset_link:
            asset_link = f"https://youtube.com/embed/{asset_link.split('?v=')[-1]}"
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
