import ffmpeg
import os
import random
import yt_dlp
import subprocess
import json


def getYoutubeVideoLink(url):
    if "shorts" in url:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "no_color": True,
            "no_call_home": True,
            "no_check_certificate": True,
            "format": "bestvideo[height<=1920]",
        }
    else:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "no_color": True,
            "no_call_home": True,
            "no_check_certificate": True,
            "format": "bestvideo[height<=1080]",
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            dictMeta = ydl.extract_info(url, download=False)
            return dictMeta["url"], dictMeta["duration"]
    except Exception as e:
        print("Failed getting video link from the following video/url", e.args[0])
    return None, None


def loop_video_until_target_length(
    video_url, output_file, target_length, video_duration
):
    """Loops the video by concatenating it with itself until it reaches the target length."""
    intermediate_file = "intermediate.mp4"
    n_loops_required = int(target_length / video_duration) + 1

    # Create a list with the video URL repeated as many times as needed
    inputs = [video_url] * n_loops_required

    # Concatenate videos
    (
        ffmpeg.concat(*[ffmpeg.input(i) for i in inputs])
        .output(
            intermediate_file,
            codec="libx264",
            preset="ultrafast",
        )
        .run(overwrite_output=True)
    )

    # Truncate the concatenated video to the desired length
    (
        ffmpeg.input(intermediate_file, t=target_length)
        .output(output_file, codec="libx264", preset="ultrafast")
        .run()
    )

    # Cleanup the intermediate file
    os.remove(intermediate_file)


def extract_random_clip_from_video(
    video_url, video_duration, clip_duration, output_file
):
    while not video_duration * 0.7 > 120:
        print(
            f"Video too short ({video_duration * 0.7} seconds). Doubling its length..."
        )
        loop_video_until_target_length(
            video_url, output_file, video_duration * 2, video_duration
        )
        video_url = output_file  # Update video URL to point to the looped file
        video_duration *= 2  # Update video duration

    start_time = video_duration * 0.15 + random.random() * (
        0.7 * video_duration - clip_duration
    )

    # Create new output file with new name
    output_file = output_file.replace(".mp4", "_final.mp4")

    (
        ffmpeg.input(video_url, ss=start_time, t=clip_duration)
        .output(output_file, codec="libx264", preset="ultrafast")
        .run()
    )
    if not os.path.exists(output_file):
        raise Exception("Random clip failed to be written")
    return output_file


def get_aspect_ratio(video_file):
    cmd = (
        'ffprobe -i "{}" -v quiet -print_format json -show_format -show_streams'.format(
            video_file
        )
    )
    #     jsonstr = subprocess.getoutput(cmd)
    jsonstr = subprocess.check_output(cmd, shell=True, encoding="utf-8")
    r = json.loads(jsonstr)
    # look for "codec_type": "video". take the 1st one if there are mulitple
    video_stream_info = [x for x in r["streams"] if x["codec_type"] == "video"][0]
    if (
        "display_aspect_ratio" in video_stream_info
        and video_stream_info["display_aspect_ratio"] != "0:1"
    ):
        a, b = video_stream_info["display_aspect_ratio"].split(":")
        dar = int(a) / int(b)
    else:
        # some video do not have the info of 'display_aspect_ratio'
        w, h = video_stream_info["width"], video_stream_info["height"]
        dar = int(w) / int(h)
        ## not sure if we should use this
        # cw,ch = video_stream_info['coded_width'], video_stream_info['coded_height']
        # sar = int(cw)/int(ch)
    if (
        "sample_aspect_ratio" in video_stream_info
        and video_stream_info["sample_aspect_ratio"] != "0:1"
    ):
        # some video do not have the info of 'sample_aspect_ratio'
        a, b = video_stream_info["sample_aspect_ratio"].split(":")
        sar = int(a) / int(b)
    else:
        sar = dar
    par = dar / sar
    return dar
