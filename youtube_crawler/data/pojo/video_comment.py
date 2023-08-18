# TODO: implement VideoComment class
class VideoComment:
    """
    VideoInfo is a class that contains information about a video.

    This class is used to store the information of a video.
    VideoInfo is crawled from a video card from a search result page.
    """
    def __init__(self):
        self._video_id: str = None
        self._title: str = None
        self._video_url = None
        self._is_short: bool = None
        self._view_count = None
        self._publish_time = None
        self._channel_name: str = None
        self._channel_url = None
        self._desc_text: str = None

    @property
    def video_id(self):
        return self._video_id

    @property
    def title(self):
        return self._title

    @property
    def video_url(self):
        return self._video_url

    @property
    def is_short(self):
        return self._is_short

    @property
    def view_count(self):
        return self._view_count

    @property
    def publish_time(self):
        return self._publish_time

    @property
    def channel_name(self):
        return self._channel_name

    @property
    def channel_url(self):
        return self._channel_url

    @property
    def desc_text(self):
        return self._desc_text

    def set_video_id(self, video_id: str):
        self._video_id = video_id

    def set_title(self, title: str):
        self._title = title

    def set_video_url(self, video_url: str):
        self._video_url = video_url

    def set_is_short(self, is_short: bool):
        self._is_short = is_short

    def set_view_count(self, view_count: str):
        self._view_count = view_count

    def set_publish_time(self, publish_time: str):
        self._publish_time = publish_time

    def set_channel_name(self, channel_name: str):
        self._channel_name = channel_name

    def set_channel_url(self, channel_url: str):
        self._channel_url = channel_url

    def set_desc_text(self, desc_text: str):
        self._desc_text = desc_text

    def to_dict(self):
        return {
            "video_id": self._video_id,
            "title": self._title,
            "video_url": self._video_url,
            "is_short": self._is_short,
            "view_count": self._view_count,
            "publish_time": self._publish_time,
            "channel_name": self._channel_name,
            "channel_url": self._channel_url,
            "desc_text": self._desc_text
        }

    @classmethod
    def from_dict(cls, data_dict: dict):
        video_info = cls()
        for key, value in data_dict.items():
            if hasattr(video_info, f"set_{key}"):
                getattr(video_info, f"set_{key}")(value)
        if video_info.video_id is None:
            raise ValueError("video_id is None")
        return video_info

    def __str__(self):
        return f"VideoInfo(video_id={self._video_id})"

    def __repr__(self):
        return self.__str__()


__all__ = ['VideoComment']
