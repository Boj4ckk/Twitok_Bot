# src/edit/video_processor.py

from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageFilter
import logging
import numpy as np
import cv2

# Setting up logging for tracking the processing steps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VideoProcessor:
    """
    Handles video processing tasks such as face detection, cropping, resizing, and applying effects.
    """

    @staticmethod
    def getWebcamCoordinates(videoPath):
        """
        Detects the coordinates of the first face in a video, assuming it's from the webcam feed.

        :param videoPath: Path to the video file.
        :return: Tuple (x, y, width, height) of the detected face, or None if no face is found.
        """
        video = cv2.VideoCapture(videoPath)  # Open the video file
        faceCoordinates = None

        # Load Haar Cascade for face detection
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Read video frame by frame
        while True:
            ret, frame = video.read()
            if not ret:
                break  # No frames left
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for detection
            faces = faceCascade.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                # Take the first detected face
                faceCoordinates = faces[0]
                break

        video.release()  # Release resources
        return faceCoordinates

    @staticmethod
    def cropVideoToPortrait(video, targetWidth, targetHeight):
        """
        Crops and resizes a video to match portrait dimensions (9:16).

        :param video: The VideoFileClip object to be cropped and resized.
        :param targetWidth: The desired width of the final video.
        :param targetHeight: The desired height of the final video.
        :return: A VideoFileClip object resized and cropped to the target dimensions.
        """
        videoWidth, videoHeight = video.size
        videoAspectRatio = videoWidth / videoHeight
        targetAspectRatio = targetWidth / targetHeight

        if videoAspectRatio > targetAspectRatio:
            # Crop width
            newWidth = int(targetAspectRatio * videoHeight)
            x1 = (videoWidth - newWidth) // 2
            video = video.crop(x1=x1, x2=x1 + newWidth)
        elif videoAspectRatio < targetAspectRatio:
            # Crop height
            newHeight = int(videoWidth / targetAspectRatio)
            y1 = (videoHeight - newHeight) // 2
            video = video.crop(y1=y1, y2=y1 + newHeight)

        return video.resize((targetWidth, targetHeight))

    @staticmethod
    def blurImage(image, blurRadius):
        """
        Applies a Gaussian blur to an image.

        :param image: NumPy array representing the image.
        :param blurRadius: Radius of the blur.
        :return: Blurred image as a NumPy array.
        """
        pilImage = Image.fromarray(image)
        blurredImage = pilImage.filter(ImageFilter.GaussianBlur(blurRadius))
        return np.array(blurredImage)

    @staticmethod
    def processVideo(url, outputPath, targetWidth, targetHeight):
        """
        Processes a video: overlays webcam feed, adds a blurred background, and formats for TikTok.

        :param clipInstance: Clip object containing metadata (e.g., URL, dimensions).
        :param outputPath: Path to save the processed video.
        :param targetWidth: Target width for TikTok's vertical format.
        :param targetHeight: Target height for TikTok's vertical format.
        """
        try:
            # Load video
            logging.info(f"Loading video from: {url}")
            video = VideoFileClip(url)

            # Detect face coordinates
            faceCoords = VideoProcessor.getWebcamCoordinates(url)
            if not faceCoords:
                logging.warning("No face detected. Proceeding without webcam overlay.")
                faceClip = None
            else:
                x, y, w, h = faceCoords
                faceClip = video.crop(x1=x, y1=y, x2=x + w, y2=y + h).resize((targetWidth // 3, targetHeight // 3))
                faceClip = faceClip.set_position(("center", "top"))

            # Apply blur effect to background
            #blurredBackground = video.fl_image(lambda img: VideoProcessor.blurImage(img, 30))
            #blurredBackground = blurredBackground.resize((targetWidth, targetHeight))

            # Combine clips
            clips = []
            if faceClip:
                clips.append(faceClip)

            finalVideo = CompositeVideoClip(clips)

            # Save the video
            logging.info(f"Saving processed video to: {outputPath}")
            finalVideo.write_videofile(outputPath, codec="libx264", fps=24)
            logging.info("Video processing completed successfully.")

        except Exception as e:
            logging.error(f"An error occurred during video processing: {e}")
