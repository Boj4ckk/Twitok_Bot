# src/tests/test_twitch_api.py

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / 'src'))

from api.twitch_api import TwitchApi
from utils.metadata_manager import MetadataManager
from config import (
    TWITCH_CLIENT_ID,
    TWITCH_CLIENT_SECRET,
    DOWNLOAD_FOLDER,
    DEFAULT_FILTERS,
    METADATA_FILE
)

# Initialize the Twitch API
twitchApi = TwitchApi(clientId=TWITCH_CLIENT_ID, clientSecret=TWITCH_CLIENT_SECRET)

def testGetUserId(username):
    """
    Test fetching the user ID of a Twitch username.

    :param username: Twitch username to test.
    """
    print("Testing getUserId...")
    userId = twitchApi.getUserId(username)
    if userId:
        print(f"User ID for {username}: {userId}")
    else:
        print(f"Failed to fetch User ID for {username}")
    return userId

def testGetVideos(userId):
    """
    Test fetching videos for a user ID with default filters.

    :param userId: Twitch user ID to fetch videos for.
    """
    print("\nTesting getVideos...")
    if not userId:
        print("Cannot fetch videos without a valid user ID.")
        return []

    videos = twitchApi.getVideos(userId=userId, filters=DEFAULT_FILTERS)
    if videos:
        print(f"Fetched {len(videos)} videos:")
        for video in videos[:3]:  # Print details of the first 3 videos
            print(f"- ID: {video['id']}, Title: {video['title']}, Views: {video['view_count']}")
        # Save metadata to clips_metadata.json
        MetadataManager.saveMetadata(videos, METADATA_FILE)
    else:
        print("No videos found.")
    return videos

def testDownloadVideo(video):
    """
    Test downloading a video using the provided `downloadClipWithAudio` method.

    :param video: Dictionary containing video metadata.
    """
    print("\nTesting downloadVideo...")
    if not video:
        print("No valid video metadata provided.")
        return False

    # Download the first video using the existing function in TwitchApi
    twitchApi.downloadClipWithAudio(clip=video, savePath=DOWNLOAD_FOLDER)
    return True

if __name__ == "__main__":
    # Replace with a Twitch username for testing
    TEST_USERNAME = "Ponce"  # Replace with a real Twitch username

    # Step 1: Test getUserId
    userId = testGetUserId(TEST_USERNAME)

    # Step 2: Test getVideos
    videos = testGetVideos(userId)

    # Step 3: Download the first video (if videos are available)
    if videos:
        print(f"\nAttempting to download the first video: ID {videos[0]['id']}")
        testDownloadVideo(videos[0])
