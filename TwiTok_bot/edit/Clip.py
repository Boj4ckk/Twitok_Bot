class Clip:
    def __init__(self, id, title, duration, category, streamDate, url, views=0):
        """
        Initializes a video clip with details such as ID, title, duration, and more.

        :param id: The unique identifier for the clip.
        :param title: The title of the clip.
        :param duration: The duration of the clip in seconds.
        :param category: The category of the clip (e.g., gaming, just chatting).
        :param streamDate: The date the clip was streamed on Twitch.
        :param url: The URL of the clip.
        :param views: The number of views the clip has (default is 0).
        """
        self.id = id  # Unique identifier for the clip
        self.title = title  # Title of the clip
        self.duration = duration  # Duration of the clip in seconds
        self.views = views  # Number of views the clip has
        self.category = category  # Category of the clip (e.g., gaming, just chatting)
        self.streamDate = streamDate  # Date the clip was streamed on Twitch
        self.url = url  # URL of the clip

    def getClipInfo(self):
        """
        Returns a summary of the clip's information.

        :return: A dictionary containing the clip's ID, title, duration, views, category, stream date, and URL.
        """
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "views": self.views,
            "category": self.category,
            "streamDate": self.streamDate,
            "url": self.url,
        }