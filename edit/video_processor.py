from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageFilter
import logging
import numpy as np
import cv2

# Setting up logging for tracking the processing steps
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VideoProcessor:
    
    @staticmethod
    def getWebcamCoordinates(videoPath):
        """
        Detects the coordinates of the first face detected in the video, assuming it's from the webcam feed.

        :param videoPath: The path to the video file where face detection is performed.
        :return: A tuple containing the coordinates (x, y, width, height) of the detected face, or None if no face is found.
        """
        video = cv2.VideoCapture(videoPath)  # Open the video file
        faceCoordinates = None

        # Load Haar Cascade for face detection
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Read video frame by frame
        while True:
            ret, frame = video.read()
            if not ret:
                break  # Break if no frames are left
            
            # Convert to grayscale for face detection
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(grayFrame, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                # Assuming the first detected face is the webcam feed
                x, y, w, h = faces[0]
                faceCoordinates = (x, y, w, h)
                break  # Stop after detecting the first face

        video.release()  # Release the video capture object
        return faceCoordinates

    @staticmethod
    def cropVideoToPortrait(video, targetWidth, targetHeight):
        """
        Crops and resizes the video to match the target portrait dimensions (height and width).

        :param video: The VideoFileClip object to be cropped and resized.
        :param targetWidth: The desired width of the final portrait video.
        :param targetHeight: The desired height of the final portrait video.
        :return: A VideoFileClip object resized and cropped to the target width and height.
        """
        videoWidth, videoHeight = video.size
        videoAspectRatio = videoWidth / videoHeight
        targetAspectRatio = targetWidth / targetHeight

        if videoAspectRatio > targetAspectRatio:
            # Crop the width if the video aspect ratio is wider than the target
            newWidth = int(targetAspectRatio * videoHeight)
            x1 = (videoWidth - newWidth) // 2
            x2 = x1 + newWidth
            video = video.crop(x1=x1, x2=x2)
        elif videoAspectRatio < targetAspectRatio:
            # Crop the height if the video aspect ratio is narrower than the target
            newHeight = int(videoWidth / targetAspectRatio)
            y1 = (videoHeight - newHeight) // 2
            y2 = y1 + newHeight
            video = video.crop(y1=y1, y2=y2)

        video = video.resize((targetWidth, targetHeight))  # Resize to target dimensions
        return video

    @staticmethod
    def blurImage(image, blurRadius):
        """
        Applies a Gaussian blur effect to an image.

        :param image: The image to which the blur effect will be applied, represented as a NumPy array.
        :param blurRadius: The radius of the Gaussian blur to be applied.
        :return: A blurred version of the input image as a NumPy array.
        """
        pilImage = Image.fromarray(image)  # Convert to PIL Image
        blurredImage = pilImage.filter(ImageFilter.GaussianBlur(blurRadius))  # Apply Gaussian Blur
        return np.array(blurredImage)  # Convert back to NumPy array

    def processVideo(clipInstance, outputPath, targetWidth, targetHeight):
        """
        Processes a video to include a blurred background and a superimposed webcam feed at the top. 
        The video is resized to a portrait format.

        :param clipInstance: An object containing the URL to the video that will be processed.
        :param outputPath: The file path where the processed video will be saved.
        :param targetWidth: The target width for the final video.
        :param targetHeight: The target height for the final video.
        :return: None. The processed video is saved to the specified output path.
        """
        try:
            # Load the main video
            logging.info(f"Loading video from: {clipInstance.url}")
            video = VideoFileClip(clipInstance.url)
            logging.info(f"Video size: {video.size}")

            # Get face coordinates
            faceCoordinates = VideoProcessor.getWebcamCoordinates(clipInstance.url)
            if faceCoordinates is None:
                logging.error("No face detected in the video.")
                return

            # Crop the face section in the video
            x, y, w, h = faceCoordinates
            webcamClip = video.crop(x1=x-45, y1=y-(0.25*h), x2=x+(3*w), y2=y+(h*1.25))
            logging.info(f"Face region cropped: x={x}, y={y}, w={w}, h={h}")

            logging.info(f"Webcam Video size: {webcamClip.size}")

            # Crop and resize the video to portrait format
           # croppedVideo = VideoProcessor.cropVideoToPortrait(video, targetWidth, targetHeight)

            # Apply blur effect to the background
            #blurredBackground = croppedVideo.fl_image(lambda image: VideoProcessor.blurImage(image, blurRadius=30))

            # Resize the webcam to occupy 25% of the screen height
            # webcamHeight = int(targetHeight * 0.25)
            overlayedWebcam = webcamClip.resize((480, 270)).set_position(("center", "top"))
            
            logging.info(f"overlayed WEB Video size: {overlayedWebcam.size}")

            overlayedWebcam = VideoProcessor.cropVideoToPortrait(overlayedWebcam, 720, 320)

            logging.info(f"Cropped WEB Video size: {overlayedWebcam.size}")

            # Resize the main video for overlay
            # overlayedVideoHeight = int(croppedVideo.size[1] * 0.75)
            overlayedVideo = video.resize((1440, 810)).set_position("bottom")

            logging.info(f"Resize overlayed Video size: {overlayedVideo.size}")

            overlayedVideo = VideoProcessor.cropVideoToPortrait(overlayedVideo, 720, 960)

            logging.info(f"Crop overlayed Video size: {overlayedVideo.size}")

            # Combine the blurred background, main video, and webcam
            #finalVideo = CompositeVideoClip([blurredBackground, overlayedVideo, overlayedWebcam])

            # Create a background clip
            background_color = (255, 255, 255)  # White background, change as needed
            background = ColorClip(size=(targetWidth, targetHeight), color=background_color, duration=video.duration)

            logging.info(f"BACK Video size: {background.size}")

            finalVideo = CompositeVideoClip([background, overlayedVideo, overlayedWebcam])

            logging.info(f"fINAL Video size: {finalVideo.size}")

            # Export the final result
            logging.info(f"Exporting final video to: {outputPath}")
            finalVideo.write_videofile(outputPath, codec="libx264", fps=24)


            logging.info("Video processing with blur and overlay completed successfully.")

        except Exception as e:
            logging.error(f"An error occurred during video processing: {e}")