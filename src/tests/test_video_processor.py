# src/tests/test_video_processor.py

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / 'src'))

from edit.video_processor import VideoProcessor

from config import (
    PROCESSED_FOLDER,
    TARGET_HEIGHT,
    TARGET_WIDTH,
    TEST_CLIP
)

# Main test
def videoProcessingPipeline():
    """
    Tests the entire pipeline: face detection, cropping, blurring, and combining clips.
    """
    # Process video
    try:
        print("Starting video processing pipeline...")
        VideoProcessor.processVideo(TEST_CLIP, PROCESSED_FOLDER, TARGET_WIDTH, TARGET_HEIGHT)
        assert os.path.exists(PROCESSED_FOLDER), "Processed video not saved successfully."
        print(f"Video processing pipeline completed. Processed video saved at {PROCESSED_FOLDER}")

    except Exception as exception:
        print(f"Error during processing: {exception}")
        raise

# Run the test
if __name__ == "__main__":
    videoProcessingPipeline()
