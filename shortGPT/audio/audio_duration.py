import yt_dlp
import subprocess
import json
from shortGPT.editing_utils.handle_videos import getYoutubeVideoLink

def get_duration_yt_dlp(url):
    ydl_opts = {
    "quiet": True,
    "no_warnings": True,
    "no_color": True,
    "no_call_home": True,
    "no_check_certificate": True
}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(url, download=False, )
            return dictMeta['duration'], ""
    except Exception as e:
        return None, f"Failed getting duration from the following video/audio url/path using yt_dlp. {e.args[0]}"

def get_duration_ffprobe(signed_url):
    try:
        cmd = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-i",
            signed_url
        ]
        output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if output.returncode != 0:
            return None, f"Error executing command using ffprobe. {output.stderr.strip()}"

        metadata = json.loads(output.stdout)
        duration = float(metadata["format"]["duration"])
        return duration, ""
    except Exception as e:
        print("Failed getting the duration of the asked ressource", e.args[0])
    return None, ""

def getAssetDuration(url, isVideo=True):
    if("youtube.com" in url):
        if not isVideo:
            url, _ = getYoutubeAudioLink(url)
        else:
            url, _ = getYoutubeVideoLink(url)
    #Trying two different method to get the duration of the video / audio
    duration, err_ffprobe = get_duration_ffprobe(url)
    if duration is not None:
        return url, duration

    duration, err_yt_dlp = get_duration_yt_dlp(url)
    if duration is not None:
        return url, duration
    print(err_yt_dlp)
    print(err_ffprobe)
    print(f"The url/path {url} does not point to a video/ audio. Impossible to extract its duration")
    return url, None


def getYoutubeAudioLink(url):
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
