import datetime
import os
import re
import shutil
import subprocess
import json

from shortGPT.audio import audio_utils
from shortGPT.audio.audio_duration import get_asset_duration
from shortGPT.config.asset_db import AssetDatabase
from shortGPT.config.languages import Language
from shortGPT.editing_framework.editing_engine import EditingEngine, EditingStep
from shortGPT.editing_utils import captions
from shortGPT.editing_utils.handle_videos import getYoutubeVideoLink, get_aspect_ratio
from shortGPT.engine.abstract_content_engine import AbstractContentEngine
from shortGPT.gpt import gpt_movie_clipper


class MovieClipperEngine(AbstractContentEngine):
    
    def __init__(
        self,
        video_path: str,
        num_clips: int = 3,
        min_clip_duration: int = 15,
        max_clip_duration: int = 45,
        background_music_name: str = "",
        watermark: str = None,
        language: Language = Language.ENGLISH,
        short_id: str = ""
    ):
        super().__init__(short_id, "movie_clipper", language, voiceModule=None)
        
        if not short_id:
            self._db_source_video_path = video_path
            self._db_num_clips = num_clips
            self._db_min_clip_duration = min_clip_duration
            self._db_max_clip_duration = max_clip_duration
            if background_music_name:
                self._db_background_music_name = background_music_name
            if watermark:
                self._db_watermark = watermark
        
        self.stepDict = {
            1: self._prepareSourceVideo,
            2: self._extractAudio,
            3: self._transcribeAudio,
            4: self._detectInterestingMoments,
            5: self._extractClips,
            6: self._generateCaptions,
            7: self._chooseBackgroundMusic,
            8: self._renderClips,
            9: self._finalizeOutput
        }
    
    def _prepareSourceVideo(self):
        if self._db_prepared_video_path:
            return
        
        source = self._db_source_video_path
        
        if source.startswith('http'):
            if 'youtube.com' in source or 'youtu.be' in source:
                self.logger("Fetching YouTube video...")
                video_url, duration = getYoutubeVideoLink(source)
                self._db_video_url = video_url
                self._db_video_duration = duration
                self._db_prepared_video_path = video_url
            else:
                self._db_prepared_video_path = source
                self._db_video_url = source
        else:
            if not os.path.exists(source):
                raise Exception(f"Video file not found: {source}")
            self._db_prepared_video_path = source
            self._db_video_url = source
        
        self.logger(f"Source video prepared: {self._db_prepared_video_path}")
    
    def _extractAudio(self):
        if self._db_extracted_audio_path:
            return
        
        self.logger("Extracting audio from video...")
        audio_output = self.dynamicAssetDir + "extracted_audio.wav"
        
        command = [
            'ffmpeg', '-y',
            '-loglevel', 'error',
            '-i', self._db_prepared_video_path,
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            audio_output
        ]
        
        subprocess.run(command, check=True)
        
        if not os.path.exists(audio_output):
            raise Exception("Failed to extract audio from video")
        
        self._db_extracted_audio_path = audio_output
        self.logger("Audio extraction complete")
    
    def _transcribeAudio(self):
        if self._db_whisper_analysis:
            return
        
        self.logger("Transcribing audio with Whisper...")
        self._db_whisper_analysis = audio_utils.audioToText(self._db_extracted_audio_path)
        self.logger("Transcription complete")
    
    def _detectInterestingMoments(self):
        if self._db_detected_moments:
            return
        
        self.logger("Using LLM to detect interesting moments...")
        
        moments = gpt_movie_clipper.detect_interesting_moments(
            self._db_whisper_analysis,
            min_duration=self._db_min_clip_duration,
            max_duration=self._db_max_clip_duration,
            num_clips=self._db_num_clips
        )
        
        if not moments:
            raise Exception("No interesting moments detected in the video")
        
        self._db_detected_moments = moments
        
        summary = gpt_movie_clipper.get_clip_suggestions_summary(moments)
        self.logger(f"Detected {len(moments)} interesting moments:\n{summary}")
    
    def _extractClips(self):
        if self._db_extracted_clips:
            return
        
        self.logger("Extracting video clips...")
        extracted_clips = []
        
        for i, moment in enumerate(self._db_detected_moments):
            clip_output = self.dynamicAssetDir + f"clip_{i}.mp4"
            
            start_time = moment['start_time']
            duration = moment['end_time'] - moment['start_time']
            
            command = [
                'ffmpeg', '-y',
                '-loglevel', 'error',
                '-ss', str(start_time),
                '-i', self._db_prepared_video_path,
                '-t', str(duration),
                '-map', '0:v:0',
                '-map', '0:a:0?',
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-preset', 'fast',
                clip_output
            ]
            
            subprocess.run(command, check=True)
            
            if os.path.exists(clip_output):
                extracted_clips.append({
                    'path': clip_output,
                    'title': moment['clip_title'],
                    'start_time': start_time,
                    'end_time': moment['end_time'],
                    'duration': duration
                })
                self.logger(f"Extracted clip {i + 1}: {moment['clip_title']}")
        
        self._db_extracted_clips = extracted_clips
    
    def _generateCaptions(self):
        if self._db_clips_captions:
            return
        
        self.logger("Generating captions for clips...")
        clips_captions = []
        
        for i, clip in enumerate(self._db_extracted_clips):
            clip_audio = self.dynamicAssetDir + f"clip_{i}_audio.wav"
            
            command = [
                'ffmpeg', '-y',
                '-loglevel', 'error',
                '-i', clip['path'],
                '-vn',
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                clip_audio
            ]
            subprocess.run(command, check=True)
            
            whisper_result = audio_utils.audioToText(clip_audio)
            timed_captions = captions.getCaptionsWithTime(whisper_result, maxCaptionSize=15)
            
            clips_captions.append(timed_captions)
            self.logger(f"Generated captions for clip {i + 1}")
        
        self._db_clips_captions = clips_captions
    
    def _chooseBackgroundMusic(self):
        if self._db_background_music_name:
            self._db_background_music_url = AssetDatabase.get_asset_link(self._db_background_music_name)
    
    def _renderClips(self):
        if self._db_rendered_clips:
            return
        
        total_clips = len(self._db_extracted_clips)
        print(f"[RenderClips] Starting to render {total_clips} clips...")
        rendered_clips = []
        
        for i, clip in enumerate(self._db_extracted_clips):
            print(f"[RenderClips] Processing clip {i + 1}/{total_clips}: {clip['title']}")
            output_path = self.dynamicAssetDir + f"rendered_clip_{i}.mp4"
            
            if os.path.exists(output_path):
                print(f"[RenderClips] Clip {i + 1} already exists, skipping...")
                rendered_clips.append({
                    'path': output_path,
                    'title': clip['title']
                })
                continue
            
            resized_clip = self.dynamicAssetDir + f"resized_clip_{i}.mp4"
            print(f"[RenderClips] Resizing clip {i + 1} to 1080x1920...")
            self._resize_to_short(clip['path'], resized_clip)
            print(f"[RenderClips] Resize complete for clip {i + 1}")
            
            print(f"[RenderClips] Setting up editing steps for clip {i + 1}...")
            videoEditor = EditingEngine()
            
            videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_VIDEO, {
                'url': resized_clip,
                'set_time_start': 0,
                'set_time_end': clip['duration']
            })
            
            clip_audio = self.dynamicAssetDir + f"clip_{i}_audio.wav"
            if os.path.exists(clip_audio):
                videoEditor.addEditingStep(EditingStep.ADD_VOICEOVER_AUDIO, {
                    'url': clip_audio
                })
            
            if self._db_background_music_url:
                videoEditor.addEditingStep(EditingStep.ADD_BACKGROUND_MUSIC, {
                    'url': self._db_background_music_url,
                    'loop_background_music': clip['duration'],
                    'volume_percentage': 0.05
                })
            
            caption_type = EditingStep.ADD_CAPTION_SHORT_ARABIC if self._db_language == Language.ARABIC.value else EditingStep.ADD_CAPTION_SHORT
            
            clip_captions = self._db_clips_captions[i]
            print(f"[RenderClips] Adding {len(clip_captions)} captions to clip {i + 1}...")
            for (t1, t2), text in clip_captions:
                videoEditor.addEditingStep(caption_type, {
                    'text': text.upper(),
                    'set_time_start': t1,
                    'set_time_end': t2
                })
            
            if self._db_watermark:
                videoEditor.addEditingStep(EditingStep.ADD_WATERMARK, {
                    'text': self._db_watermark
                })
            
            print(f"[RenderClips] Rendering clip {i + 1} with EditingEngine...")
            videoEditor.renderVideo(output_path, logger=self.logger if self.logger is not self.default_logger else None)
            print(f"[RenderClips] Finished rendering clip {i + 1}")
            
            rendered_clips.append({
                'path': output_path,
                'title': clip['title']
            })
            self.logger(f"Rendered clip {i + 1}: {clip['title']}")
        
        print(f"[RenderClips] All {total_clips} clips rendered successfully")
        self._db_rendered_clips = rendered_clips
    
    def _resize_to_short(self, input_path, output_path):
        command = [
            'ffmpeg', '-y',
            '-loglevel', 'error',
            '-i', input_path,
            '-map', '0:v:0',
            '-map', '0:a:0?',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-preset', 'fast',
            output_path
        ]
        subprocess.run(command, check=True)
    
    def _finalizeOutput(self):
        if not os.path.exists('videos/'):
            os.makedirs('videos')
        
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        final_paths = []
        for i, clip in enumerate(self._db_rendered_clips):
            safe_title = re.sub(r"[^a-zA-Z0-9 '\n\.]", '', clip['title'])[:50]
            new_filename = f"videos/{date_str}_clip{i + 1}_{safe_title}.mp4"
            
            shutil.copy(clip['path'], new_filename)
            final_paths.append(new_filename)
            
            with open(new_filename.replace('.mp4', '.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Title: {clip['title']}\n")
        
        self._db_video_path = final_paths[0] if final_paths else None
        self._db_all_video_paths = final_paths
        self._db_ready_to_upload = True
        
        self.logger(f"Finalized {len(final_paths)} clips")
    
    def get_all_video_paths(self):
        return self._db_all_video_paths or []
