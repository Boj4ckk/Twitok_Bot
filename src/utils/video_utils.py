# src/utils/video_utils.py

class VideoUtils:
    """
    Provides utility functions for filtering and processing video metadata.
    """

    @staticmethod
    def filterByViews(videos, minViews=None, maxViews=None):
        """
        Filter videos by view count.

        :param videos: List of video metadata dictionaries.
        :param minViews: Minimum number of views.
        :param maxViews: Maximum number of views.
        :return: Filtered list of videos.
        """
        filteredVideos = []
        for video in videos:
            views = video.get("view_count", 0)
            if (minViews is None or views >= minViews) and (maxViews is None or views <= maxViews):
                filteredVideos.append(video)
        return filteredVideos

    @staticmethod
    def filterByDuration(videos, minDuration=None, maxDuration=None):
        """
        Filter videos by duration.

        :param videos: List of video metadata dictionaries.
        :param minDuration: Minimum duration in seconds.
        :param maxDuration: Maximum duration in seconds.
        :return: Filtered list of videos.
        """
        filteredVideos = []
        for video in videos:
            duration = video.get("duration", 0)
            if (minDuration is None or duration >= minDuration) and (maxDuration is None or duration <= maxDuration):
                filteredVideos.append(video)
        return filteredVideos

    @staticmethod
    def filterByDate(videos, startDate=None, endDate=None):
        """
        Filter videos by published date.

        :param videos: List of video metadata dictionaries.
        :param startDate: Earliest acceptable date (ISO 8601 string).
        :param endDate: Latest acceptable date (ISO 8601 string).
        :return: Filtered list of videos.
        """
        filteredVideos = []
        for video in videos:
            publishedAt = video.get("published_at")
            if (startDate is None or publishedAt >= startDate) and (endDate is None or publishedAt <= endDate):
                filteredVideos.append(video)
        return filteredVideos
