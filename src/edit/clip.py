# src/edit/clip.py

class Clip:
    """
    Represents a Twitch clip with relevant metadata for processing.
    """

    def __init__(self, id, title, duration, category, streamDate, url, views=0):
        """
        Initialize a Clip instance with metadata.

        :param id: Unique identifier for the clip.
        :param title: Title of the clip.
        :param duration: Duration of the clip in seconds.
        :param category: Category of the clip (e.g., game, chatting).
        :param streamDate: Date when the clip was streamed on Twitch.
        :param url: URL of the clip for downloading or reference.
        :param views: Number of views the clip has (default is 0).
        """
        self.id = id  # Unique identifier for the clip
        self.title = title  # Title of the clip
        self.duration = duration  # Duration of the clip in seconds
        self.views = views  # Number of views
        self.category = category  # Category or game ID
        self.streamDate = streamDate  # Date the clip was streamed
        self.url = url  # URL of the clip

    def getClipInfo(self):
        """
        Retrieve a summary of the clip's metadata.

        :return: A dictionary containing the clip's metadata.
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

    def __str__(self):
        """
        String representation of the clip for debugging or display.

        :return: A formatted string with clip details.
        """
        return (f"Clip(ID: {self.id}, Title: {self.title}, Duration: {self.duration}s, "
                f"Views: {self.views}, Category: {self.category}, Stream Date: {self.streamDate}, "
                f"URL: {self.url})")
