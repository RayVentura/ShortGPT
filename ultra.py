from shortGPT.config.api_db import ApiKeyManager, ApiProvider
from shortGPT.config.asset_db import AssetDatabase, AssetType
from shortGPT.engine.reddit_short_engine import RedditShortEngine
from shortGPT.audio.eleven_voice_module import ElevenLabsVoiceModule
from shortGPT.config.languages import Language
from shortGPT.audio.edge_voice_module import EdgeTTSVoiceModule, EDGE_TTS_VOICENAME_MAPPING
from shortGPT.api_utils.youtube_api import search_videos_YouTube
import random

# Set API Keys
ApiKeyManager.set_api_key(ApiProvider.OPENAI, "")
ApiKeyManager.set_api_key(ApiProvider.ELEVEN_LABS, "")
ApiKeyManager.set_api_key(ApiProvider.PEXELS, "")

random_pairs = {
  "abba": ["https://www.youtube.com/watch?v=yJcCoZ34S5k", "https://www.youtube.com/watch?v=SQIawwMwVLs"],
  "onerepublic": ["https://www.youtube.com/watch?v=nZEQ4a1ZT8I", "https://www.youtube.com/watch?v=SQIawwMwVLs"],
  "afterdark": ["https://www.youtube.com/watch?v=As3LGNTlPQ0", new_video_url], # <---- variable use
  "materialgirl": ["https://www.youtube.com/watch?v=ng81ukSvV6s", "https://www.youtube.com/watch?v=_zvqSgPw_2M"]
}


random_keys = list(random_pairs.keys())
random.shuffle(random_keys)

random_pair = random.choice(random_keys)
pair_urls = random_pairs[random_pair]

try: 
  new_video_url = search_videos_YouTube("Palmer Luckey Sucks")
except:
  new_video_url = "https://www.youtube.com/watch?v=nZEQ4a1ZT8I"

video_url = pair_urls[1]
music_url = pair_urls[0]

music_title = random_pair + "_music"
video_title = random_pair + "_video"

AssetDatabase.add_remote_asset(music_title, AssetType.BACKGROUND_MUSIC, music_url)
AssetDatabase.add_remote_asset(video_title, AssetType.BACKGROUND_VIDEO, video_url)


USE_ELEVEN_LABS = True
# Configure the ElevenLabs Voice Module
if USE_ELEVEN_LABS:
    eleven_labs_key = ApiKeyManager.get_api_key(ApiProvider.ELEVEN_LABS)
    voice_module = ElevenLabsVoiceModule(api_key = eleven_labs_key, voiceName="Bella") #gigi aggressive
else:
    ## You can also use the EdgeTTS for Free voice synthesis
    voice_name = EDGE_TTS_VOICENAME_MAPPING[Language.ENGLISH]['female']
    voice_module = EdgeTTSVoiceModule(voice_name)

# Configure Content Engine
content_engine = RedditShortEngine(voiceModule=voice_module,
    background_video_name=video_title, # <--- use the same name you saved in  the AssetDatabase
    background_music_name=music_title, # <--- use the same name you saved in  the AssetDatabase
    num_images=4, # If you don't want images in your video, put 0 or None
    language=Language.ENGLISH)

# Generate Content
for step_num, step_logs in content_engine.makeContent():
    print(f" {step_logs}")

# Get Video Output Path
print(content_engine.get_video_output_path())
