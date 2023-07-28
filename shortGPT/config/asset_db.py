from shortGPT.database.db_document import TinyMongoDocument
from shortGPT.audio.audio_utils import  downloadYoutubeAudio, getAssetDuration
import pandas as pd
import shutil
import os
import re
import time
import base64
from datetime import datetime
audio_extensions = [".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".wma", ".opus"]
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"]
video_extensions = [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".webm", ".m4v"]
TEMPLATE_ASSETS_DB_PATH = '.database/template_asset_db.json'
ASSETS_DB_PATH = '.database/asset_db.json'
class AssetDatabase:
    if not (os.path.exists(ASSETS_DB_PATH)) and os.path.exists(TEMPLATE_ASSETS_DB_PATH):
            shutil.copy(TEMPLATE_ASSETS_DB_PATH, ASSETS_DB_PATH)
    local_assets = TinyMongoDocument("asset_db", "asset_collection", "local_assets", create=True)
    remote_assets = TinyMongoDocument("asset_db", "asset_collection", "remote_assets", create=True)
    
    @classmethod
    def asset_exists(cls, name):
        local_assets = cls.local_assets._get()
        if name in local_assets:
            return True
        remote_assets = cls.remote_assets._get()
        if name in remote_assets:
            return True
        return False
    @classmethod
    def add_local_asset(cls, name, type, path):
        """Add a local asset to the database."""
        cls.local_assets._save({
            name: {
                "type": type,
                "path": path,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    @classmethod
    def add_remote_asset(cls, name, type, url):
        """Add a remote asset to the database."""
        cls.remote_assets._save({
            name: {
                "type": type,
                "url": url,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    @classmethod
    def remove_asset(cls, name):
        """Remove an asset from the database."""
        # Check if the asset exists in local assets
        local_assets = cls.local_assets._get()
        if name in local_assets:
            if (not 'required' in local_assets[name]):
                try:
                    os.remove(local_assets[name]['path'])
                except Exception as e:
                    print(e)
                cls.local_assets._delete(name)

        # Check if the asset exists in remote assets
        remote_assets = cls.remote_assets._get()
        if name in remote_assets:
            cls.remote_assets._delete(name)

        # # If the asset does not exist in the database
        # raise ValueError(f"Asset '{name}' does not exist in the database.")
    @classmethod
    def get_df(cls):
        """Returns a pandas DataFrame with specific asset details."""
        remote_assets = cls.remote_assets._get()

        # Prepare data for DataFrame
        data = []
        remote_items = remote_assets.items()
        for key, asset in remote_items:
            ts = asset['ts'] if 'ts' in asset else None
            data.append({'name': key, 'type': asset['type'], 'link': asset['url'], 'source': 'youtube', 'ts': ts})

        # Create DataFrame
        df = pd.DataFrame(data)

        # Sort DataFrame by ts
        df.sort_values(by='ts', ascending=False, inplace=True)
        df = df.drop(columns='ts')
        return df
    @classmethod
    def sync_local_assets(cls):
        """Loads all local assets from the static-assets folder into the database"""
        local_paths = []
        local_assets = cls.local_assets._get()
        for key in local_assets:
            asset = local_assets[key]
            filePath = asset['path']
            if not os.path.exists(filePath):
                cls.local_assets._delete(key)
            else:
                local_paths.append(filePath)

        folder_path = 'public'
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename).replace("\\", "/")
                if not file_path in local_paths:
                    file_ext = os.path.splitext(file_path)[1]
                    if file_ext in audio_extensions:
                        asset_type = 'audio'
                    elif file_ext in image_extensions:
                        asset_type = 'image'
                    elif file_ext in video_extensions:
                        asset_type = 'video'
                    else:
                        asset_type = 'other'
                    cls.local_assets._save({f'{filename.split(".")[0]}': {"path": file_path, "type": asset_type,
                                                                           "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
    @classmethod
    def getAssetLink(cls, key):
        # If it's a local asset, return the path
        local_assets = cls.local_assets._get()
        if key in local_assets:
            asset = local_assets[key]
            asset['ts'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls.local_assets._save({key: asset})
            return local_assets[key]['path']

        # If it's a remote asset
        remote_assets = cls.remote_assets._get()
        if key in remote_assets:
            asset = remote_assets[key]
            asset['ts'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls.remote_assets._save({key: asset})
            asset_dict = remote_assets[key]
            asset_type = asset_dict['type']
            if 'youtube' in asset_dict['url']:
                if any(type in asset_type for type in ['audio', 'video', 'music']):
                    if any(type in asset_type for type in ['audio', 'music']):
                        local_audio_file, duration = downloadYoutubeAudio(asset_dict['url'], "public/"+key+".wav")
                        cls.local_assets._save({
                            f"{key}" : {
                                'path' : local_audio_file,
                                'duration': duration,
                                'type': 'audio',
                                'ts': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                        })
                        return local_audio_file
                    if 'remote_url' in asset_dict:
                        asset_dict['remote_url'] = base64.b64decode(asset_dict['remote_url']).decode('utf-8')
                        expire_timestamp_match = re.search(r"expire=(\d+)", asset_dict['remote_url'])
                        notExpired = expire_timestamp_match and int(expire_timestamp_match.group(1)) > time.time() + 1800
                        if notExpired and 'duration' in asset_dict:
                            return asset_dict['remote_url']
                    remote_url, duration = cls.updateYoutubeAsset(key)
                    return remote_url
            return asset_dict['url']

        return None
    @classmethod
    def getAssetDuration(cls, key):
        # If it's a local asset, get its duration
        local_assets = cls.local_assets._get()
        if key in local_assets:
            asset = local_assets[key]
            asset['ts'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls.local_assets._save({key: asset})
            asset = local_assets[key]
            if not 'duration' in asset:
                path, duration = cls.updateLocalAsset(key)
                return duration
            return asset['duration']

        # If it's a remote asset
        remote_assets = cls.remote_assets._get()
        if key in remote_assets:
            asset = remote_assets[key]
            asset['ts'] =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cls.remote_assets._save({key: asset})
            if 'duration' in asset:
                return asset['duration']
            # If the duration is not in the asset dictionary, update the asset
            _, duration = cls.updateYoutubeAsset(key)
            return duration

        return None
    @classmethod
    def updateLocalAsset(cls, key: str):
        asset_dict = cls.local_assets._get(key)
        file_path = asset_dict['path']
        # Get duration and file_path
        asset = {
            "path": file_path,
            "type": asset_dict['type']
        }
        if any(type in asset_dict['type'] for type in ['audio', 'video', 'music']):
            _, duration = getAssetDuration(file_path)
            asset['duration'] = duration
        else:
            duration = None
        # Update the asset with file_path and duration
        cls.local_assets._save({key: asset})
        return file_path, duration 
    @classmethod
    def updateYoutubeAsset(cls, key: str):
        asset_dict = cls.remote_assets._get(key)
        youtube_url = asset_dict['url']
        # Get duration and remote_url
        remote_url, duration = getAssetDuration(youtube_url, isVideo= "video" in asset_dict['type'])

        # Update the asset with remote_url and duration
        asset = {
            "url": youtube_url,
            "remote_url": base64.b64encode(remote_url.encode()).decode('utf-8'),
            "duration": duration,
            "type": asset_dict['type']
        }
        cls.remote_assets._save({key: asset})

        return remote_url, duration