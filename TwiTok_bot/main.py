# Import necessary classes and libraries
from tiktok_api import TikTokAPI  # TikTok API class for automation
from edit.clip import Clip  # Import the Clip class to create video clip instances
from edit.transition_manager import TransitionManager  # Import the TransitionManager class for handling transitions between clips
from edit.video_processor import VideoProcessor  # Import the VideoProcessor class for processing video clips
import logging  # Import logging to capture processing information

# Configure logging to capture the processing information
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instructions:
# ===========================
# Download 1-2 video clips (in .mp4 format) and place them in the "clip_twitch" folder.

# Path to your web driver (ChromeDriver or GeckoDriver)
driver_path = r"C:\\Users\\user\\chromedriver-win64\\chromedriver.exe"

# Create the TikTokAPI instance
tiktok_api = TikTokAPI(driver_path)

# Target dimensions for portrait format (9:16) - these are typical dimensions for mobile viewing
targetHeight = 1280  # Height of the video in pixels
targetWidth = 720  # Width of the video in pixels

# Process video before uploading
# ---------------------------------------------------------
# Create Clip instance for processing a single clip with effects
clipInstance = Clip(
    id=3,  # Unique identifier for the clip
    title="Best Twitch Moments with Blur",  # Title of the clip
    duration=120,  # Duration of the clip in seconds
    category="gaming",  # Category of the clip
    streamDate="2024-10-01",  # Date of the stream
    url=r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_twitch\\clip (1).mp4",  # Path to the video file
    views=1  # Number of views (initially set to 1)
)

# Output path for the processed clip with blur effect
outputPath = r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_processed\\clip p1.mp4"  # Path where the processed clip will be saved

# Process the video with blur effect using the VideoProcessor class
VideoProcessor.processVideo(clipInstance, outputPath, targetWidth, targetHeight)

# Log the success message after exporting the processed clip
logging.info(f"File has been exported to: {outputPath}")

# Now upload the processed video to TikTok
# ------------------------------------------
# Start the driver and go to the TikTok upload page
tiktok_api.startDriver()

# Login with your TikTok credentials (username, password)
tiktok_api.login("username", "password", 'Username')

# Upload the processed video from local path
tiktok_api.uploadVideo(outputPath, "This is an example description for my TikTok video!")

# Close the browser
tiktok_api.closeDriver()