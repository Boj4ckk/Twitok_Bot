# src/api/twitch_api.py

import os
import requests
import subprocess
import logging

class TwitchApi:
    """
    Handles Twitch API interactions for authentication, video fetching, and downloading.
    """

    BASE_URL = "https://api.twitch.tv/helix"

    def __init__(self, clientId, clientSecret):
        """
        Initialize TwitchApi instance and authenticate.

        :param clientId: Twitch application client ID.
        :param clientSecret: Twitch application client secret.
        """
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.accessToken = self.authenticate()

    def authenticate(self):
        """
        Authenticate and get an app access token.

        :return: Access token as a string.
        """
        url = "https://id.twitch.tv/oauth2/token"
        payload = {
            "client_id": self.clientId,
            "client_secret": self.clientSecret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token = response.json()["access_token"]
        logging.info("Successfully authenticated with Twitch API.")
        return token

    def getHeaders(self):
        """
        Generate headers for Twitch API requests.

        :return: Dictionary of headers.
        """
        return {
            "Client-Id": self.clientId,
            "Authorization": f"Bearer {self.accessToken}"
        }

    def getUserId(self, username):
        """
        Fetch the user ID for a given Twitch username.

        :param username: Twitch username.
        :return: User ID as a string, or None if not found.
        """
        url = f"{self.BASE_URL}/users"
        params = {"login": username}
        response = requests.get(url, headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                return data[0]["id"]
        logging.error(f"Failed to fetch user ID for {username}: {response.text}")
        return None

    def getVideos(self, userId, filters=None):
        """
        Fetch videos for a given Twitch user based on filters.

        :param userId: Twitch user ID.
        :param filters: Dictionary of filters (e.g., views, duration).
        :return: List of video metadata dictionaries.
        """
        url = f"{self.BASE_URL}/videos"
        params = {"user_id": userId}
        if filters:
            params.update(filters)
        response = requests.get(url, headers=self.getHeaders(), params=params)
        if response.status_code == 200:
            return response.json().get("data", [])
        logging.error(f"Failed to fetch videos for user {userId}: {response.text}")
        return []

    def downloadClipWithAudio(self, clip, savePath="clips"):
        """
        Download a Twitch clip with audio using Streamlink.

        :param clip: Dictionary containing clip metadata.
        :param savePath: Directory to save the downloaded clip.
        """
        os.makedirs(savePath, exist_ok=True)
        videoUrl = clip["url"]
        fileName = f"{savePath}/{clip['user_name']}_{clip['id']}.mp4"

        # Use streamlink to download the clip with audio
        command = [
            "streamlink",
            videoUrl,
            "worst",
            "-o",
            fileName
        ]

        try:
            subprocess.run(command, check=True)
            logging.info(f"Clip successfully downloaded: {fileName}")
        except subprocess.CalledProcessError as error:
            logging.error(f"Failed to download clip {clip['id']} ({error})")