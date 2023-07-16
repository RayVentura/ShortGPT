from shortGPT.audio.audio_duration import getAssetDuration
import traceback
from moviepy.editor import TextClip
a = {'asd':43}
try:
    a[4934]
    print(TextClip(txt=2437832))
except Exception as e:
    traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    error_name = type(e).__name__.capitalize()+ " : " +f"{e.args[0]}"
    print(error_name, traceback_str)