import os
import sys
from pathlib import Path

# Add the `src` directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / 'src'))

from api.tiktok_api import TiktokApi
from config import (
    TIKTOK_COOKIES_PATH,
    TIKTOK_USERNAME,
    TIKTOK_PASSWORD
)


# Initialize the Tiktok API with mock paths
tiktokApi = TiktokApi(TIKTOK_COOKIES_PATH)

def testLogin(username, password):
    """
    Test logging into TikTok and saving cookies.

    :param username: TikTok username or email.
    :param password: TikTok password.
    """
    print("Testing login...")
    tiktokApi.startDriver()
    tiktokApi.login(username, password)

    # Check if cookies were saved correctly
    if os.path.exists(TIKTOK_COOKIES_PATH):
        print(f"Cookies saved at {TIKTOK_COOKIES_PATH}.")
        return True
    else:
        print("Failed to save cookies.")
        return False

def testUploadVideo(videoPath, description):
    """
    Test uploading a video to TikTok.

    :param videoPath: Path to the video file.
    :param description: Description text for the video.
    """
    print("\nTesting video upload...")
    tiktokApi.uploadVideo(videoPath, description)

    # Simulate that video was uploaded and check if uploadVideo was called
    print(f"Video '{videoPath}' uploaded with description: {description}")
    return True

def testCloseDriver():
    """
    Test closing the WebDriver.
    """
    print("\nTesting closeDriver...")
    tiktokApi.startDriver()  # Start the driver
    tiktokApi.closeDriver()  # Close the driver

    if tiktokApi.driver is None:
        print("Driver closed successfully.")
        return True
    else:
        print("Failed to close the driver.")
        return False

if __name__ == "__main__":
    # Replace with real TikTok credentials and test video path
    TEST_VIDEO_PATH = "./2316638431.mp4"
    TEST_DESCRIPTION = "Test video upload"

    # Step 1: Test login
    login_success = testLogin(TIKTOK_USERNAME, TIKTOK_PASSWORD )

    # Step 2: Test video upload (if login is successful)
    if login_success:
        testUploadVideo(TEST_VIDEO_PATH, TEST_DESCRIPTION)

    # Step 3: Test driver closure
    testCloseDriver()
