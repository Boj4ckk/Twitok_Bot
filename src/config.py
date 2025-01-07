# src/config.py

# Twitch API credentials
TWITCH_CLIENT_ID = "zae28miqv3hp5q2556epbqak7gzdxt"  # Replace with your Twitch API Client ID
TWITCH_CLIENT_SECRET = "5ysav0r608lcmti1fggc4la5ui7ghq"
TWITCH_ACCESS_TOKEN = ""  # Replace with a valid OAuth token

# TikTok automation setup
TIKTOK_DRIVER_PATH = "./drivers/chromedriver"  # Path to ChromeDriver for Selenium
TIKTOK_COOKIES_PATH = "./src/tiktok_cookies.pkl"  # Path to saved TikTok cookies
TIKTOK_USERNAME = "twitok_bot"
TIKTOK_PASSWORD = "utT5K5~gDi$29rK"

# File paths for clip management
METADATA_FILE = "./src/metadata/clips_metadata.json"  # File to store Twitch video metadata
USERS_FILE = "./src/metadata/user.json"
DOWNLOAD_FOLDER = "./src/edit/twitch_clip/"  # Folder to store raw Twitch clips
PROCESSED_FOLDER = "./src/edit/tiktok_clip/"  # Folder to store processed TikTok-ready clips
TEST_CLIP = "./src/edit/twitch_clip/Ponce_2318057455.mp4"

# Video processing settings
TARGET_WIDTH = 720  # TikTok video width (9:16 aspect ratio)
TARGET_HEIGHT = 1280  # TikTok video height (9:16 aspect ratio)
CLIP_DURATION_LIMIT = 60  # Maximum duration of a processed clip (in seconds)

# Default filters for fetching Twitch clips
DEFAULT_FILTERS = {
    "views": ">100",  # Minimum views threshold
    "duration": "<600",  # Maximum clip duration in seconds
}

# Logging settings
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Flask server settings
FLASK_HOST = "127.0.0.1"  # Localhost IP
FLASK_PORT = 5000  # Port for the Flask server
REDIRECT_URI = "http://localhost:5000/callback"

# Additional settings
ENABLE_DEBUG_MODE = True  # Enable Flask debug mode
