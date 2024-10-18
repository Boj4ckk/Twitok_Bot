# Import necessary classes and libraries
from tiktok_api import TikTokAPI
from edit.clip import Clip  # Import the Clip class to create video clip instances
from edit.transition_manager import TransitionManager  # Import the TransitionManager class for handling transitions between clips
from edit.video_processor import VideoProcessor  # Import the VideoProcessor class for processing video clips
import logging  # Import logging to capture processing information
import webbrowser

# Configure logging to capture the processing information
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Instructions:
# ===========================
# 1. Download 1-2 video clips (in .mp4 format) and place them in the "clip_twitch" folder.
# 2. Update the 'url' attributes of the Clip instances below to match your local file paths.
# 3. Define the output path for the final processed videos, where the resulting video will be saved.
# 4. After running the script, the processed videos will be saved in the "clip_processed" folder (or any folder you specify).

# # Path to your web driver (ChromeDriver or GeckoDriver)
# driver_path = r"C:\\Users\\user\\chromedriver-win64\\chromedriver.exe"

# # Create the TikTokAPI instance
# Initialize the TikTokAPI instance
tiktok_api = TikTokAPI()

# Start the WebDriver
tiktok_api.start_driver()

# Attempt to login using saved cookies or prompt for credentials if it's the first time
tiktok_api.login()

# Check if login was successful by navigating to a known authenticated page
if "tiktok.com/upload" in tiktok_api.driver.current_url:
    logging.info("Successfully logged into TikTok and navigated to the upload page.")
else:
    logging.error("Login failed. Could not navigate to the upload page.")

# Close the browser
tiktok_api.close_driver()

# Upload video from local path
#tiktok_api.upload_video(r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_processed\\clip p(1).mp4", "This is an example description for my TikTok video!", "Tout le monde")

# Close the browser
#tiktok_api.close_driver()

print("Choose Feature:")
print("\t1. Edit video")
print("\t2. Add transition")

choice = int(input("\nChoice: "))

if choice == 1:
    
    # Processing a Single Clip with VideoProcessor
    # ---------------------------------------------------------
    # This test case demonstrates how to create one instance of the Clip class
    # and use the VideoProcessor to apply effects to it.
    # The video will be processed with a blur effect and saved to the specified output path.

    # Target dimensions for portrait format (9:16) - these are typical dimensions for mobile viewing
    targetHeight = 1280  # Height of the video in pixels
    targetWidth = 720  # Width of the video in pixels

    # Create Clip instance for processing a single clip with effects
    clipInstance = Clip(
        id=3,  # Unique identifier for the clip
        title="Best Twitch Moments with Blur",  # Title of the clip
        duration=120,  # Duration of the clip in seconds
        category="gaming",  # Category of the clip
        streamDate="2024-10-01",  # Date of the stream
        url=r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_twitch\\clip (1).mp4",  # Path to the video file (to be updated)
        views=1  # Number of views (initially set to 1)
    )

    # Output path for the processed clip with blur effect
    outputPath = r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_processed\\clip p1.mp4"  # Path where the processed clip will be saved (to be updated)

    # Process the video with blur effect using the VideoProcessor class
    VideoProcessor.processVideo(clipInstance, outputPath, targetWidth, targetHeight)  # Method to process the video (to be verified)

    # Log the success message after exporting the processed clip
    logging.info(f"File has been exported to: {outputPath}")  # Log statement for successful export

elif choice == 2:

    # Test Case 1: Creating and Processing Clips with Transitions
    # -----------------------------------------------------------
    # This test case demonstrates how to create two instances of the Clip class.
    # It then initializes a TransitionManager to apply transitions between these clips.
    # The processed final video will be exported to a specified output path.

    # Create Clip instance 1 with detailed information
    clipInstance1 = Clip(
        id=1,  # Unique identifier for the clip
        title="Best Twitch Moments",  # Title of the clip
        duration=120,  # Duration of the clip in seconds
        category="gaming",  # Category of the clip (e.g., gaming)
        streamDate="2024-10-01",  # Date the stream occurred
        url=r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_twitch\\clip (1).mp4",  # Path to the video file (to be updated)
        views=1  # Number of views (initially set to 1)
    )

    # Create Clip instance 2 with similar details
    clipInstance2 = Clip(
        id=2,  # Unique identifier for the second clip
        title="Best Twitch Moments",  # Title of the clip
        duration=120,  # Duration of the clip in seconds
        category="gaming",  # Category of the clip
        streamDate="2024-10-01",  # Date of the stream
        url=r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_twitch\\clip (2).mp4",  # Path to the second video file (to be updated)
        views=1  # Number of views (initially set to 1)
    )

    # List of clips to be processed
    clipList = [clipInstance1, clipInstance2]  # A list containing both Clip instances

    print("Choose Transition:")
    print("\t1. Crossfade")
    print("\t2. Cut")
    print("\t3. Fadein")

    transition = int(input("\nChoice: "))

    # Apply the transitions between the clips using the TransitionManager
    # finalClip will hold the resulting video after applying transitions

    finalClip = clipInstance1.url

    if transition == 1:
       
        finalClip = TransitionManager.applyCrossfade(clipList)  # Applies crossfade between the clips (method name to be verified)

    elif transition == 2:

        finalClip = TransitionManager.applyCut(clipList)  # Applies cuts between the clips (method name to be verified)

    elif transition == 3:
         
        finalClip = TransitionManager.applyFadeIn(clipList)  # Applies cuts between the clips (method name to be verified)

    else:
        print("Wrong input")
   
    # Define the output path for the processed video
    outputPath = r"C:\\Users\\user\\Desktop\\Twitok_Bot\\TwiTok_bot\\edit\\clip_processed\\clip pt.mp4"  # Path where the processed video will be saved (to be updated)

    # Export the final video with the applied transitions
    # The processed video will be written to the specified output path
    finalClip.write_videofile(outputPath, codec="libx264", fps=24)  # Method to save the video (to be verified)

    # Log the success message after exporting
    logging.info(f"Final file has been exported to: {outputPath}")  # Log statement for successful export

else:
    print("Wrong input")

# Final Notes:
# ==========================
# After running both test cases:
# 1. Ensure the input clips exist in the "clip_twitch" folder.
# 2. Verify the processed video(s) in the "clip_processed" folder with transitions and effects applied.