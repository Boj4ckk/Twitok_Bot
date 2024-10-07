from moviepy.editor import *


class TransitionManager:
    def __init__(self, transitionType, transitionDuration):
        """
        Initialise un gestionnaire de transitions pour une vidéo.

        :param transitionType: Le type de transition (ex: fade, cut, crossfade).
        :param transitionDuration: La durée de la transition en secondes.
        """
        self.transitionType = transitionType  # Type de transition (fade, cut, etc.)
        self.transitionDuration = transitionDuration  # Durée de la transition en secondes

    def applyFadeIn(self, duration):
        """
        Applique une transition de type "fade-in" à la vidéo.

        :param duration: Durée de la transition en secondes.
        :return: La vidéo avec la transition "fade-in" appliquée.
        """
        return lambda video: video.fadein(duration)

    def applyCut(self):
        """
        Applique une transition de type "cut" (coupure brutale) à la vidéo.
        
        :return: La vidéo après application de la transition "cut".
        """
        # Implémentation pour un "cut" peut varier selon le besoin
        return lambda video: video  # Un simple retour sans effet pour une coupure brutale

    def applyCrossfade(self, duration):
        """
        Applique une transition de type "crossfade" à la vidéo.

        :param duration: Durée de la transition en secondes.
        :return: La vidéo avec la transition "crossfade" appliquée.
        """
        return lambda video: video.crossfadein(duration)
