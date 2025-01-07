# src/main.py

import os
import logging
from api.twitch_api import TwitchApi
from api.tiktok_api import TiktokApi
from edit.clip import Clip
from edit.video_processor import VideoProcessor
from utils.video_utils import filterVideos
from utils.metadata_manager import MetadataManager
from config import (
    TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN,
    TIKTOK_DRIVER_PATH, METADATA_FILE,
    DOWNLOAD_FOLDER, PROCESSED_FOLDER,
    TARGET_WIDTH, TARGET_HEIGHT
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

twitchApi = TwitchApi(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
tiktokApi = TiktokApi(TIKTOK_DRIVER_PATH)
clipsMetadata = MetadataManager.loadMetadata(METADATA_FILE)


    # for i, clipData in enumerate(filteredClips):
    #     clip = Clip(
    #         id=clipData["id"],
    #         title=clipData["title"],
    #         duration=clipData["duration"],
    #         category=clipData["game_id"],
    #         streamDate=clipData["created_at"],
    #         url=clipData["url"],
    #         views=clipData["view_count"]
    #     )