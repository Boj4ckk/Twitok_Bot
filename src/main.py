# src/main.py

import os
import logging
from api.twitch_api import TwitchApi
from api.tiktok_api import TiktokApi
from utils.metadata_manager import MetadataManager
from config import (
    TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN,
    TIKTOK_DRIVER_PATH, METADATA_FILE
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

twitchApi = TwitchApi(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
tiktokApi = TiktokApi(TIKTOK_DRIVER_PATH)
clipsMetadata = MetadataManager.loadMetadata(METADATA_FILE)