from time import sleep
from time import sleep
from yt_dlp import YoutubeDL


def search_videos_YouTube(query_string): # or query?
    ydl_opts = {
        'default_search': 'ytsearch',
        'format': 'bestvideo[height=1920][height=1080]+bestaudio/best', # Optional: Specify desired video format
        'max_downloads': 1, 
        'no_playlist' : True,
        'ignoreerrors': True,
        #'width': 1920,
        #'height': 1080,
        #'start_time': 10,
        #'duration': 100,
        'min_views': 2000
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            search_results = ydl.extract_info(query_string, download=False)
            video_url = search_results['entries'][0]['webpage_url']
            print(video_url, ", we can proceed")
            return video_url
        except:
            return None
