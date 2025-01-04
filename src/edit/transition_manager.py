# src/edit/transition_manager.py

from moviepy.editor import VideoFileClip, concatenate_videoclips

class TransitionManager:
    """
    Handles transitions between video clips.
    """

    @staticmethod
    def applyFadeIn(clipList):
        """
        Applies a "fade-in/fade-out" transition between each clip in the list.

        :param clipList: List of Clip objects with a 'url' property pointing to the video file.
        :return: A combined video clip with fade transitions applied between each clip.
        """
        clipsWithFades = []  # List to hold clips with fade transitions
        
        for i in range(len(clipList) - 1):
            # Load the current and next clips using their URLs
            currentClip = VideoFileClip(clipList[i].url).crossfadeout(2)
            nextClip = VideoFileClip(clipList[i + 1].url).crossfadein(2)
            
            # Add the processed clips to the list
            clipsWithFades.append(currentClip)
            clipsWithFades.append(nextClip)

        # Concatenate all clips with fade transitions
        finalVideo = concatenate_videoclips(clipsWithFades, method="compose")
        return finalVideo

    @staticmethod
    def applyCut(clipList):
        """
        Applies a "cut" transition, which is an abrupt switch between clips without blending or fading.

        :param clipList: List of Clip objects with a 'url' property pointing to the video file.
        :return: A combined video clip with abrupt cuts between each clip.
        """
        # Concatenate all clips without applying any transition effects
        videoClips = [VideoFileClip(clip.url) for clip in clipList]
        return concatenate_videoclips(videoClips, method="compose")

    @staticmethod
    def applyCrossfade(clipList):
        """
        Applies a "crossfade" transition between each clip, smoothly blending one clip into the next.

        :param clipList: List of Clip objects with a 'url' property pointing to the video file.
        :return: A combined video clip with crossfade transitions between each clip.
        """
        clipsWithCrossfade = []  # List to hold clips with crossfade transitions

        for i in range(len(clipList) - 1):
            # Load the current and next clips with crossfade effects
            currentClip = VideoFileClip(clipList[i].url).crossfadeout(2)
            nextClip = VideoFileClip(clipList[i + 1].url).crossfadein(2)

            # Add the processed clips to the list
            clipsWithCrossfade.append(currentClip)
            clipsWithCrossfade.append(nextClip)

        # Concatenate all clips with crossfade transitions
        finalVideo = concatenate_videoclips(clipsWithCrossfade, method="compose")
        return finalVideo
