from moviepy.editor import VideoFileClip, concatenate_videoclips

class TransitionManager:
    def __init__(self, clipList, transitionType, transitionDuration):
        """
        Initializes a transition manager for a video, which applies transitions between clips.

        :param clipList: A list of Clip objects (containing URLs) to apply transitions to.
        :param transitionType: The type of transition to apply (e.g., fade, cut, crossfade).
        :param transitionDuration: The duration of the transition in seconds.
        """
        self.transitionType = transitionType  # Type of transition (e.g., fade, cut, crossfade)
        self.transitionDuration = transitionDuration  # Duration of the transition in seconds
        self.clipList = clipList  # List of clip objects to process

    def applyFadeIn(self):
        """
        Applies a "fade-in/fade-out" transition between each clip in the list.

        :return: A combined video clip with fade transitions applied between each clip.
        """
        clipsWithFades = []  # List to hold clips with fade transitions
        
        for i in range(len(self.clipList) - 1):
            # Load the clips using the URL property from each Clip object
            clip = VideoFileClip(self.clipList[i].url).crossfadeout(self.transitionDuration)  # Apply fade-out to the current clip
            nextClip = VideoFileClip(self.clipList[i + 1].url).crossfadein(self.transitionDuration)  # Apply fade-in to the next clip
            
            # Add the current clip with fade-out and the next clip with fade-in
            clipsWithFades.append(clip)
            clipsWithFades.append(nextClip)

        # Concatenate all clips with transitions
        finalVideo = concatenate_videoclips(clipsWithFades, method="compose")
        return finalVideo

    def applyCut(self):
        """
        Applies a "cut" transition, which is an abrupt switch between clips without blending or fading.

        :return: A combined video clip with abrupt cuts between each clip.
        """
        # Concatenate all clips without any transition effects
        return concatenate_videoclips([VideoFileClip(clip.url) for clip in self.clipList], method="compose")

    def applyCrossfade(self):
        """
        Applies a "crossfade" transition between each clip, smoothly blending one clip into the next.

        :return: A combined video clip with crossfade transitions between each clip.
        """
        clipsWithCrossfade = []  # List to hold clips with crossfade transitions
        for i in range(len(self.clipList) - 1):
            # Apply crossfade transitions between clips
            clip = VideoFileClip(self.clipList[i].url).crossfadeout(self.transitionDuration)
            nextClip = VideoFileClip(self.clipList[i + 1].url).crossfadein(self.transitionDuration)
            clipsWithCrossfade.append(clip)
            clipsWithCrossfade.append(nextClip)

        # Concatenate all clips with crossfade transitions
        finalVideo = concatenate_videoclips(clipsWithCrossfade, method="compose")
        return finalVideo