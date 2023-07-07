import ffmpeg
import os
import random
import yt_dlp
def getYoutubeAudio(url):
    ydl_opts = {
    "quiet": True,
    "no_warnings": True,
    "no_color": True,
    "no_call_home": True,
    "no_check_certificate": True,
    "format": "bestaudio/best"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=False)
            return dictMeta['url'], dictMeta['duration']
    except Exception as e:
        print("Failed getting audio link from the following video/url", e.args[0])
    return None

def getYoutubeAudio(url):
    ydl_opts = {
    "quiet": True,
    "no_warnings": True,
    "no_color": True,
    "no_call_home": True,
    "no_check_certificate": True,
    "format": "bestaudio/best"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=False)
            return dictMeta['url'], dictMeta['duration']
    except Exception as e:
        print("Failed getting audio link from the following video/url", e.args[0])
    return None

def getYoutubeVideoLink(url):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "no_color": True,
        "no_call_home": True,
        "no_check_certificate": True,
        "format": "bestvideo[height<=1080]"
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(
                url,
                download=False)
            return dictMeta['url'], dictMeta['duration']
    except Exception as e:
        print("Failed getting video link from the following video/url", e.args[0])
    return None, None

def extract_random_clip_from_video(video_url, video_duration, clip_duration , output_file):
    print(video_url, video_duration, clip_duration , output_file)
    """Extracts a clip from a video using a signed URL.
    Args:
        video_url (str): The signed URL of the video.
        video_url (int): Duration of the video.
        start_time (int): The start time of the clip in seconds.
        clip_duration (int): The duration of the clip in seconds.
        output_file (str): The output file path for the extracted clip.
    """
    if not video_duration:
        raise Exception("Could not get video duration")
    if not video_duration*0.7 > 120:
        raise Exception("Video too short")
    start_time = video_duration*0.15 + random.random()* (0.7*video_duration-clip_duration)
    
    (
        ffmpeg
        .input(video_url, ss=start_time, t=clip_duration)
        .output(output_file, codec="libx264", preset="ultrafast")
        .run()
    )
    if not os.path.exists(output_file):
        raise Exception("Random clip failed to be written")
    return output_file
