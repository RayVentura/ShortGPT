from shortGPT.config.path_utils import get_program_path
import os
magick_path = get_program_path("magick")
if magick_path:
    os.environ['IMAGEMAGICK_BINARY'] = magick_path
from shortGPT.config.path_utils import handle_path
import numpy as np
import json
from typing import Any, Dict, List, Union
from moviepy.editor import (AudioFileClip, CompositeVideoClip,CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip, vfx,)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from shortGPT.editing_framework.rendering_logger import MoviepyProgressLogger

def load_schema(json_path):
    return json.loads(open(json_path, 'r', encoding='utf-8').read())

class CoreEditingEngine:

    def generate_image(self, schema:Dict[str, Any],output_file , logger=None):
        assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        clips = []

        for asset_key in assets:
            asset = assets[asset_key]
            asset_type = asset['type']
            if asset_type == 'image':
                try:
                    clip = self.process_image_asset(asset)
                except Exception as e:
                    continue
            elif asset_type == 'text':
                clip = self.process_text_asset(asset)
                clips.append(clip)
            else:
                raise ValueError(f'Invalid asset type: {asset_type}')
            clips.append(clip)

        image = CompositeVideoClip(clips)
        image.save_frame(output_file)
        return output_file

    def generate_video(self, schema:Dict[str, Any], output_file, logger=None) -> None:
        visual_assets = dict(sorted(schema['visual_assets'].items(), key=lambda item: item[1]['z']))
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        
        visual_clips = []
        for asset_key in visual_assets:
            asset = visual_assets[asset_key]
            asset_type = asset['type']
            if asset_type == 'video':
                clip = self.process_video_asset(asset)
            elif asset_type == 'image':
                try:
                    clip = self.process_image_asset(asset)
                except Exception as e:
                    continue
            elif asset_type == 'text':
                clip = self.process_text_asset(asset)
            else:
                raise ValueError(f'Invalid asset type: {asset_type}')

            visual_clips.append(clip)
        
        audio_clips = []

        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            if asset_type == "audio":
                audio_clip = self.process_audio_asset(asset)
            else:
                raise ValueError(f"Invalid asset type: {asset_type}")

            audio_clips.append(audio_clip)
        video = CompositeVideoClip(visual_clips)
        if(audio_clips):
            audio = CompositeAudioClip(audio_clips)
            video.duration = audio.duration
            video.audio = audio
        if logger:
            my_logger = MoviepyProgressLogger(callBackFunction=logger)
            video.write_videofile(output_file, codec='libx264', audio_codec='aac', logger=my_logger)
        else:
            video.write_videofile(output_file, codec='libx264', audio_codec='aac')
        return output_file
    
    def generate_audio(self, schema:Dict[str, Any], output_file, logger=None) -> None:
        audio_assets = dict(sorted(schema['audio_assets'].items(), key=lambda item: item[1]['z']))
        audio_clips = []

        for asset_key in audio_assets:
            asset = audio_assets[asset_key]
            asset_type = asset['type']
            if asset_type == "audio":
                audio_clip = self.process_audio_asset(asset)
            else:
                raise ValueError(f"Invalid asset type: {asset_type}")

            audio_clips.append(audio_clip)
        audio = CompositeAudioClip(audio_clips)
        audio.fps = 44100
        if logger:
            my_logger = MoviepyProgressLogger(callBackFunction=logger)
            audio.write_audiofile(output_file, logger=my_logger)
        else:
            audio.write_audiofile(output_file)
        return output_file
    # Process common actions
    def process_common_actions(self,
                                   clip: Union[VideoFileClip, ImageClip, TextClip, AudioFileClip],
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, AudioFileClip, ImageClip, TextClip]:
        for action in actions:
            if action['type'] == 'set_time_start':
                clip = clip.set_start(action['param'])
                continue
   
            if action['type'] == 'set_time_end':
                clip = clip.set_end(action['param'])
                continue
            
            if action['type'] == 'subclip':
                clip = clip.subclip(**action['param'])
                continue

        return clip

    # Process common visual clip actions
    def process_common_visual_actions(self,
                                   clip: Union[VideoFileClip, ImageClip, TextClip],
                                   actions: List[Dict[str, Any]]) -> Union[VideoFileClip, ImageClip, TextClip]:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
 
            if action['type'] == 'resize':
                clip = clip.resize(**action['param'])
                continue

            if action['type'] == 'crop':
                clip = clip.crop(**action['param'])
                continue

            if action['type'] == 'screen_position':
                clip = clip.set_position(**action['param'])
                continue

            if action['type'] == 'green_screen':
                params = action['param']
                color = params['color'] if  params['color'] else [52, 255, 20]
                thr = params['thr'] if params['thr'] else 100
                s = params['s'] if params['s'] else 5
                clip = clip.fx(vfx.mask_color, color=color,thr=thr, s=s)
                continue

            if action['type'] == 'normalize_image':
                clip = clip.fx(self.__normalize_image)
                continue

            if action['type'] == 'auto_resize_image':
                ar = clip.aspect_ratio
                height = action['param']['maxHeight']
                width = action['param']['maxWidth']
                if ar <1:
                    clip = clip.resize((height*ar, height))
                else:
                    clip = clip.resize((width, width/ar))
                continue

        return clip

    # Process audio actions
    def process_audio_actions(self, clip: AudioFileClip,
                                   actions: List[Dict[str, Any]]) -> AudioFileClip:
        clip = self.process_common_actions(clip, actions)
        for action in actions:
            if action['type'] == 'normalize_music':
                clip = clip.fx(audio_normalize)
                pass
            if action['type'] == 'loop_background_music':
                target_duration = action['param']
                start = clip.duration * 0.15
                clip = clip.subclip(start)
                clip = clip.fx(audio_loop, duration=target_duration)
                pass

            if action['type'] == 'volume_percentage':
                clip = clip.volumex(action['param'])
                pass

        return clip

    # Process individual asset types
    def process_video_asset(self, asset: Dict[str, Any]) -> VideoFileClip:
        params = {
            'filename': handle_path(asset['parameters']['url'])
        }
        if 'audio' in asset['parameters']:
            params['audio'] = asset['parameters']['audio']
        clip = VideoFileClip(**params)
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_image_asset(self, asset: Dict[str, Any]) -> ImageClip:
        clip = ImageClip(asset['parameters']['url'])
        return self.process_common_visual_actions(clip, asset['actions'])

    def process_text_asset(self, asset: Dict[str, Any]) -> TextClip:
        text_clip_params = asset['parameters']
        
        if not (any(key in text_clip_params for key in ['text','fontsize', 'size'])):
            raise Exception('You must include at least a size or a fontsize to determine the size of your text')
        text_clip_params['txt'] = text_clip_params['text']
        clip_info = {k: text_clip_params[k] for k in ('txt', 'fontsize', 'font', 'color', 'stroke_width', 'stroke_color', 'size', 'kerning', 'method', 'align') if k in text_clip_params}
        clip = TextClip(**clip_info)

        return self.process_common_visual_actions(clip, asset['actions'])

    def process_audio_asset(self, asset: Dict[str, Any]) -> AudioFileClip:
        clip = AudioFileClip(asset['parameters']['url'])
        return self.process_audio_actions(clip, asset['actions'])
    
    def __normalize_image(self, clip):
        def f(get_frame, t):
            if f.normalized_frame is not None:
                return f.normalized_frame
            else:
                frame = get_frame(t)
                f.normalized_frame = self.__normalize_frame(frame)
                return f.normalized_frame

        f.normalized_frame = None

        return clip.fl(f)


    def __normalize_frame(self, frame):
        shape = np.shape(frame)
        [dimensions, ] = np.shape(shape)

        if dimensions == 2:
            (height, width) = shape
            normalized_frame = np.zeros((height, width, 3))
            for y in range(height):
                for x in range(width):
                    grey_value = frame[y][x]
                    normalized_frame[y][x] = (grey_value, grey_value, grey_value)
            return normalized_frame
        else:
            return frame
        

