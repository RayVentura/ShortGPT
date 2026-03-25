"""
Upload-Post API integration for cross-posting videos to TikTok and Instagram.

Docs: https://docs.upload-post.com
"""
import os
import requests


class UploadPostAPI:
    """
    Client for Upload-Post API - Cross-post videos to TikTok, Instagram, and more.
    """

    API_BASE = "https://api.upload-post.com"

    def __init__(self, api_key: str, username: str):
        """
        Initialize Upload-Post API client.

        Args:
            api_key (str): Upload-Post API key
            username (str): Upload-Post username/profile
        """
        self.api_key = api_key
        self.username = username

    def upload_video(
        self,
        video_path: str,
        title: str,
        platforms: list = None,
        privacy_level: str = "PUBLIC_TO_EVERYONE"
    ) -> dict:
        """
        Upload a video to TikTok and/or Instagram.

        Args:
            video_path (str): Path to the video file
            title (str): Video title/caption (max 2200 chars for Instagram)
            platforms (list): List of platforms ["tiktok", "instagram"]
            privacy_level (str): Privacy level for the video

        Returns:
            dict: API response with request_id and status
        """
        if platforms is None:
            platforms = ["tiktok", "instagram"]

        if not os.path.exists(video_path):
            return {"success": False, "error": f"Video file not found: {video_path}"}

        try:
            with open(video_path, 'rb') as video_file:
                files = {'video': video_file}
                
                data = {
                    'user': self.username,
                    'title': title[:2200],
                    'privacy_level': privacy_level
                }
                
                # Add each platform
                for i, platform in enumerate(platforms):
                    data[f'platform[{i}]'] = platform

                headers = {
                    'Authorization': f'Apikey {self.api_key}'
                }

                response = requests.post(
                    f"{self.API_BASE}/api/upload_video",
                    headers=headers,
                    data=data,
                    files=files,
                    timeout=300
                )
                
                response.raise_for_status()
                return response.json()

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def upload_photos(
        self,
        photo_paths: list,
        title: str,
        platforms: list = None,
        privacy_level: str = "PUBLIC_TO_EVERYONE"
    ) -> dict:
        """
        Upload photos as a carousel/slideshow to TikTok and/or Instagram.

        Args:
            photo_paths (list): List of paths to photo files
            title (str): Caption for the post
            platforms (list): List of platforms ["tiktok", "instagram"]
            privacy_level (str): Privacy level

        Returns:
            dict: API response with request_id and status
        """
        if platforms is None:
            platforms = ["tiktok", "instagram"]

        files = []
        try:
            for path in photo_paths:
                if os.path.exists(path):
                    files.append(('photos[]', open(path, 'rb')))

            if not files:
                return {"success": False, "error": "No valid photo files found"}

            data = {
                'user': self.username,
                'title': title[:2200],
                'privacy_level': privacy_level,
                'auto_add_music': 'true'
            }
            
            for i, platform in enumerate(platforms):
                data[f'platform[{i}]'] = platform

            headers = {
                'Authorization': f'Apikey {self.api_key}'
            }

            response = requests.post(
                f"{self.API_BASE}/api/upload_photos",
                headers=headers,
                data=data,
                files=files,
                timeout=300
            )
            
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
        finally:
            # Close all file handles
            for _, f in files:
                f.close()

    def check_status(self, request_id: str) -> dict:
        """
        Check the status of an upload request.

        Args:
            request_id (str): The request ID from upload

        Returns:
            dict: Status information
        """
        try:
            headers = {
                'Authorization': f'Apikey {self.api_key}'
            }

            response = requests.get(
                f"{self.API_BASE}/api/status/{request_id}",
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}
