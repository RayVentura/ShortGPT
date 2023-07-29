import base64
import re
import shutil
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from shortGPT.audio.audio_utils import downloadYoutubeAudio, get_asset_duration
from shortGPT.database.db_document import TinyMongoDocument

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".wma", ".opus"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv", ".webm", ".m4v"}
TEMPLATE_ASSETS_DB_PATH = '.database/template_asset_db.json'
ASSETS_DB_PATH = '.database/asset_db.json'


class AssetDatabase:
    """
    Class for managing assets, both local and remote.
    The class provides methods to add, remove, get and sync assets.
    It uses a MongoDB-like database to store information about the assets.
    """

    if not Path(ASSETS_DB_PATH).exists() and Path(TEMPLATE_ASSETS_DB_PATH).exists():
        shutil.copy(TEMPLATE_ASSETS_DB_PATH, ASSETS_DB_PATH)

    local_assets = TinyMongoDocument("asset_db", "asset_collection", "local_assets", create=True)
    remote_assets = TinyMongoDocument("asset_db", "asset_collection", "remote_assets", create=True)

    @classmethod
    def _update_timestamp_and_get(cls, asset_type, key):
        asset = asset_type._get(key)
        asset['ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        asset_type._save({key: asset})
        return asset

    @classmethod
    def asset_exists(cls, name: str) -> bool:
        return name in cls.local_assets._get() or name in cls.remote_assets._get()

    @classmethod
    def add_local_asset(cls, name: str, asset_type: str, path: str):
        cls.local_assets._save({
            name: {
                "type": asset_type,
                "path": path,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    @classmethod
    def add_remote_asset(cls, name: str, asset_type: str, url: str):
        cls.remote_assets._save({
            name: {
                "type": asset_type,
                "url": url,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    @classmethod
    def remove_asset(cls, name: str):
        if name in cls.local_assets._get():
            cls._remove_local_asset(name)
        elif name in cls.remote_assets._get():
            cls.remote_assets._delete(name)
        else:
            raise ValueError(f"Asset '{name}' does not exist in the database.")

    @classmethod
    def get_df(cls, source=None) -> pd.DataFrame:
        data = []
        if source is None or source == 'local':
            for key, asset in cls.local_assets._get().items():
                data.append({'name': key,
                             'type': asset['type'],
                             'link': asset['path'],
                             'source': 'local',
                             'ts': asset.get('ts')
                             })
        if source is None or source == 'youtube':
            for key, asset in cls.remote_assets._get().items():
                data.append({'name': key,
                            'type': asset['type'],
                             'link': asset['url'],
                             'source': 'youtube',
                             'ts': asset.get('ts')
                             })

        df = pd.DataFrame(data)
        df.sort_values(by='ts', ascending=False, inplace=True)
        return df.drop(columns='ts')

    @classmethod
    def sync_local_assets(cls):
        """
        Loads all local assets from the static-assets folder into the database.
        """
        local_assets = cls.local_assets._get()
        local_paths = {asset['path'] for asset in local_assets.values()}

        for path in Path('public').rglob('*'):
            if path.is_file() and str(path) not in local_paths:
                cls._add_local_asset_from_path(path)

    @classmethod
    def get_asset_link(cls, key: str) -> str:
        """
        Get the link to an asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Link to the asset.
        """
        if key in cls.local_assets._get():
            return cls._update_local_asset_timestamp_and_get_link(key)
        elif key in cls.remote_assets._get():
            return cls._get_remote_asset_link(key)
        else:
            raise ValueError(f"Asset '{key}' does not exist in the database.")

    @classmethod
    def get_asset_duration(cls, key: str) -> str:
        """
        Get the duration of an asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Duration of the asset.
        """
        if key in cls.local_assets._get():
            return cls._get_local_asset_duration(key)
        elif key in cls.remote_assets._get():
            return cls._get_remote_asset_duration(key)
        else:
            raise ValueError(f"Asset '{key}' does not exist in the database.")

    @classmethod
    def _remove_local_asset(cls, name: str):
        """
        Remove a local asset from the database.

        Args:
            name (str): Name of the asset.
        """
        asset = cls.local_assets._get(name)
        if 'required' not in asset:
            try:
                Path(asset['path']).unlink()
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            cls.local_assets._delete(name)

    @classmethod
    def _add_local_asset_from_path(cls, path: Path):
        """
        Add a local asset to the database from a file path.

        Args:
            path (Path): Path to the asset.
        """
        file_ext = path.suffix
        if file_ext in AUDIO_EXTENSIONS:
            asset_type = 'audio'
        elif file_ext in IMAGE_EXTENSIONS:
            asset_type = 'image'
        elif file_ext in VIDEO_EXTENSIONS:
            asset_type = 'video'
        else:
            asset_type = 'other'
        cls.local_assets._save({
            path.stem: {
                "path": str(path),
                "type": asset_type,
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        })

    @classmethod
    def _update_local_asset_timestamp_and_get_link(cls, key: str) -> str:
        """
        Update the timestamp of a local asset and get its link.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Link to the asset.
        """
        asset = cls.local_assets._get(key)
        asset['ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cls.local_assets._save({key: asset})
        return asset['path']

    @classmethod
    def _get_remote_asset_link(cls, key: str) -> str:
        """
        Get the link to a remote asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Link to the asset.
        """
        asset = cls.remote_assets._get(key)
        asset['ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cls.remote_assets._save({key: asset})
        if 'youtube' in asset['url']:
            return cls._get_youtube_asset_link(key, asset)
        return asset['url']

    @classmethod
    def _get_local_asset_duration(cls, key: str) -> str:
        """
        Get the duration of a local asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Duration of the asset.
        """
        asset = cls.local_assets._get(key)
        asset['ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cls.local_assets._save({key: asset})
        if 'duration' not in asset:
            _, duration = cls._update_local_asset_duration(key)
            return duration
        return asset['duration']

    @classmethod
    def _get_remote_asset_duration(cls, key: str) -> str:
        """
        Get the duration of a remote asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Duration of the asset.
        """
        asset = cls.remote_assets._get(key)
        asset['ts'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cls.remote_assets._save({key: asset})
        if 'duration' in asset:
            return asset['duration']
        _, duration = cls._update_youtube_asset_duration(key)
        return duration

    @classmethod
    def _update_local_asset_duration(cls, key: str) -> str:
        """
        Update the duration of a local asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Duration of the asset.
        """
        asset = cls.local_assets._get(key)
        path = Path(asset['path'])
        if any(t in asset['type'] for t in ['audio', 'video', 'music']):
            _, duration = get_asset_duration(str(path))
            asset['duration'] = duration
        else:
            duration = None
        cls.local_assets._save({key: asset})
        return str(path), duration

    @classmethod
    def _update_youtube_asset_duration(cls, key: str) -> str:
        """
        Update the duration of a Youtube asset.

        Args:
            key (str): Name of the asset.

        Returns:
            str: Duration of the asset.
        """
        asset = cls.remote_assets._get(key)
        youtube_url = asset['url']
        remote_url, duration = get_asset_duration(youtube_url, isVideo="video" in asset['type'])
        asset.update({
            "remote_url": base64.b64encode(remote_url.encode()).decode('utf-8'),
            "duration": duration,
        })
        cls.remote_assets._save({key: asset})
        return remote_url, duration

    @classmethod
    def _get_youtube_asset_link(cls, key: str, asset: dict) -> str:
        """
        Get the link to a Youtube asset.

        Args:
            key (str): Name of the asset.
            asset (dict): Asset data.

        Returns:
            str: Link to the asset.
        """
        if any(t in asset['type'] for t in ['audio', 'music']):
            local_audio_file, duration = downloadYoutubeAudio(asset['url'], f"public/{key}.wav")
            cls.local_assets._save({
                key: {
                    'path': local_audio_file,
                    'duration': duration,
                    'type': 'audio',
                    'ts': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            })
            return local_audio_file
        if 'remote_url' in asset:
            asset['remote_url'] = base64.b64decode(asset['remote_url']).decode('utf-8')
            expire_timestamp_match = re.search(r"expire=(\d+)", asset['remote_url'])
            not_expired = expire_timestamp_match and int(expire_timestamp_match.group(1)) > time.time() + 1800
            if not_expired and 'duration' in asset:
                return asset['remote_url']
        remote_url, _ = cls._update_youtube_asset_duration(key)
        return remote_url
