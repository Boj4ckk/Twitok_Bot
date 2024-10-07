from edit.Clip import Clip  # Ensure this is correct
from moviepy.editor import VideoFileClip, CompositeVideoClip
from PIL import Image, ImageFilter
import logging
import numpy as np
from edit.VideoProcessor import VideoProcessor


# Clip information
clipInstance = Clip(
    id=1,
    title="Best Twitch Moments",
    duration=120,  # 120 seconds
    category="gaming",
    streamDate="2024-10-01",
    url=r"C:\\Users\\yazki\\OneDrive\\Bureau\\conception logiciel\\edit\\clip_twitch\\clip1.mp4",
    views=1
)

# Target dimensions for portrait (9:16 aspect ratio)
target_height = 1920
target_width = 1080


# Process the video
output_path = "C:\\Users\\yazki\\OneDrive\\Bureau\\conception logiciel\\edit\\clip_processed\\clip1.mp4"
VideoProcessor.process_video_with_blur(clipInstance, output_path, target_width, target_height)


