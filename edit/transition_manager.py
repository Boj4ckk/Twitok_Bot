from moviepy.editor import VideoFileClip, concatenate_videoclips

class TransitionManager:

    def applyFadeIn(clipList):
        """
        Applies a "fade-in/fade-out" transition between each clip in the list.

        :return: A combined video clip with fade transitions applied between each clip.
        """
        clipsWithFades = []  # List to hold clips with fade transitions
        
        for i in range(len(clipList) - 1):
            # Load the clips using the URL property from each Clip object
            clip = VideoFileClip(clipList[i].url).crossfadeout(2)  # Apply fade-out to the current clip
            nextClip = VideoFileClip(clipList[i + 1].url).crossfadein(2)  # Apply fade-in to the next clip
            
            # Add the current clip with fade-out and the next clip with fade-in
            clipsWithFades.append(clip)
            clipsWithFades.append(nextClip)

        # Concatenate all clips with transitions
        finalVideo = concatenate_videoclips(clipsWithFades, method="compose")
        return finalVideo

    def applyCut(clipList):
        """
        Applies a "cut" transition, which is an abrupt switch between clips without blending or fading.

        :return: A combined video clip with abrupt cuts between each clip.
        """
        # Concatenate all clips without any transition effects
        return concatenate_videoclips([VideoFileClip(clip.url) for clip in clipList], method="compose")

    def applyCrossfade(clipList):
        """
        Applies a "crossfade" transition between each clip, smoothly blending one clip into the next.

        :return: A combined video clip with crossfade transitions between each clip.
        """
        clipsWithCrossfade = []  # List to hold clips with crossfade transitions
        for i in range(len(clipList) - 1):
            # Apply crossfade transitions between clips
            clip = VideoFileClip(clipList[i].url).crossfadeout(2)
            nextClip = VideoFileClip(clipList[i + 1].url).crossfadein(2)
            clipsWithCrossfade.append(clip)
            clipsWithCrossfade.append(nextClip)

        # Concatenate all clips with crossfade transitions
        finalVideo = concatenate_videoclips(clipsWithCrossfade, method="compose")
        return finalVideo