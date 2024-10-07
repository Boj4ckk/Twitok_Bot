from moviepy.editor import VideoFileClip, CompositeVideoClip
from PIL import Image, ImageFilter
import logging
import numpy as np
import os 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VideoProcessor:
    def __init__(self, clip):
        """
        Initialise un objet VideoProcessor pour traiter un clip vidéo.

        :param clip: Le clip vidéo à traiter.
        """
        self.clip = clip  # Le clip vidéo qui sera traité

    def process_video(self):
        """
        Traite le clip vidéo en le transformant en format 9:16 (vertical).
        Redimensionne la vidéo en 1080x1920 tout en conservant le ratio.
        """
        target_height = 1920
        target_width = 1080

        # Redimensionner la vidéo pour s'ajuster en hauteur à 1920 pixels tout en conservant son ratio
        resized_clip = self.clip.resize(height=target_height)

        # Si la vidéo est plus large que 1080 pixels, on la recadre au centre
        if resized_clip.w > target_width:
            resized_clip = resized_clip.crop(x_center=resized_clip.w / 2, width=target_width)

        # Exporter la vidéo redimensionnée
        resized_clip.write_videofile("clip_processed/clip_processed_1.mp4", fps=24)

        return resized_clip

    @staticmethod
    def crop_video_to_portrait(video, target_width, target_height):
        video_width, video_height = video.size
        video_aspect_ratio = video_width / video_height
        target_aspect_ratio = target_width / target_height

        if video_aspect_ratio > target_aspect_ratio:
            new_width = int(target_aspect_ratio * video_height)
            x1 = (video_width - new_width) // 2
            x2 = x1 + new_width
            video = video.crop(x1=x1, x2=x2)
        elif video_aspect_ratio < target_aspect_ratio:
            new_height = int(video_width / target_aspect_ratio)
            y1 = (video_height - new_height) // 2
            y2 = y1 + new_height
            video = video.crop(y1=y1, y2=y2)

        video = video.resize((target_width, target_height))
        return video

    @staticmethod
    def blur_image(image, blur_radius):
        pil_image = Image.fromarray(image)  # Convert to PIL Image
        blurred_image = pil_image.filter(ImageFilter.GaussianBlur(blur_radius))  # Apply Gaussian Blur
        return np.array(blurred_image)  # Convert back to NumPy array


    def process_video_with_blur(clip_instance, output_path, target_width, target_height):
        try:
            # Charger la vidéo
            logging.info(f"Loading video from: {clip_instance.url}")
            video = VideoFileClip(clip_instance.url)

            # Recadrer et redimensionner la vidéo pour le format portrait
            cropped_video = VideoProcessor.crop_video_to_portrait(video, target_width, target_height)

            # Appliquer l'effet de flou sur l'arrière-plan
            blurred_background = cropped_video.fl_image(lambda image: VideoProcessor.blur_image(image, blur_radius=30))

            # Redimensionner la vidéo pour superposition (90% de la largeur originale)
            overlayed_video_width = int(cropped_video.size[0] * 0.9)
            overlayed_video = cropped_video.resize((overlayed_video_width, target_height))

            # Positionner la vidéo superposée au centre
            overlayed_video = overlayed_video.set_position("center")

            # Combiner le fond flou et la vidéo superposée
            final_video = CompositeVideoClip([blurred_background, overlayed_video])

            # Exporter le résultat final
            logging.info(f"Exporting final video to: {output_path}")
            final_video.write_videofile(output_path, codec="libx264", fps=24)

            logging.info("Video processing with blur and overlay completed successfully.")

        except Exception as e:
            logging.error(f"An error occurred during video processing: {e}")




















    
    '''
    def addTransition(self, video):
        """
        Applique les transitions au clip vidéo en fonction des objets `TransitionManager`.

        :param video: La vidéo à laquelle les transitions seront appliquées.
        :return: Retourne la vidéo avec les transitions appliquées.
        """
        for transitionManager in self.transitionsList:
            if transitionManager.transitionType == 'fade':
                video = transitionManager.applyFadeIn(transitionManager.transitionDuration)(video)
            elif transitionManager.transitionType == 'cut':
                video = transitionManager.applyCut()(video)
            elif transitionManager.transitionType == 'crossfade':
                video = transitionManager.applyCrossfade(transitionManager.transitionDuration)(video)
        return video
    '''

    '''
    
    def addTextEffect(self, video, text):
        """
        Ajoute un effet de texte à la vidéo.

        :param video: Le clip vidéo auquel le texte sera ajouté.
        :param text: Le texte à ajouter sur la vidéo.
        :return: Retourne la vidéo avec l'effet de texte appliqué.
        """
        textClip = TextClip(text, fontsize=50, color='white')
        textClip = textClip.set_pos('center').set_duration(5)
        videoWithText = CompositeVideoClip([video, textClip])
        return videoWithText
    '''

    '''
    def exportToTikTokFormat(self, video):
        """
        Exporte la vidéo dans un format compatible avec TikTok (par exemple, résolution verticale).

        :param video: Le clip vidéo à formater pour TikTok.
        :return: Retourne la vidéo formatée pour TikTok.
        """
        # Redimensionner la vidéo en format vertical (9:16 pour TikTok)
        tiktokVideo = video.fx(vfx.resize, height=1920).crop(x_center=video.w / 2, width=1080)
        return tiktokVideo
    '''

    def exportVideo(self, video, outputPath):
        """
        Exporte le clip vidéo dans le format spécifié à l'emplacement donné.

        :param video: La vidéo à exporter.
        :param outputPath: Chemin où le fichier vidéo sera exporté.
        """
        video.write_videofile(outputPath, codec=self.videoFormat)  # Exportation du clip avec le format spécifié
