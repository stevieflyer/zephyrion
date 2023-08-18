# TODO implement a video comment parser
import pyppeteer.element_handle

from .base_page_parser import BaseParserHandler
from youtube_crawler.data.pojo import VideoComment


class VideoCommentParser(BaseParserHandler):
    """
    Parser Handler for retrieving video comment from video comment element.
    """
    async def parse(self, comment_card: pyppeteer.element_handle.ElementHandle) -> VideoComment:
        raise NotImplementedError


__all__ = ["VideoCommentParser"]
