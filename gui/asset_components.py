import gradio as gr
from shortGPT.config.asset_db import AssetDatabase

AssetDatabase().sync_local_assets()
def getBackgroundVideoChoices():
    asset_db = AssetDatabase()
    df = asset_db.get_df()
    choices = list(df.loc['background video'  ==  df['type']]['name'])[:20]
    return choices

def getBackgroundMusicChoices():
    asset_db = AssetDatabase()
    df = asset_db.get_df()
    choices = list(df.loc['background music'  ==  df['type']]['name'])[:20]
    return choices


background_video_checkbox = gr.CheckboxGroup(choices=getBackgroundVideoChoices(), interactive=True, label="Choose background video")
background_music_checkbox = gr.CheckboxGroup(choices=getBackgroundMusicChoices(), interactive=True, label="Choose background music")