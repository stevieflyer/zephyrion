from typing import List

import pyppeteer.element_handle

from .filter_enum import FilterSection
from zephyrion.browser_agent.pypp import PyppeteerAgent
from youtube_crawler.page_parser.selectors.common import search_input_sel, clear_input_btn_selector, search_submit_sel
from youtube_crawler.page_parser.selectors.search_result_page import filter_toggle_sel, filter_section_sel, filter_option_sel


class YoutubeBrowserAgent(PyppeteerAgent):
    """
    The browser agent for YouTube.

    `YoutubeBrowserAgent` can monitor all kinds of interactions with Youtube.
    Such as:

    - Search videos and filter the search result.
    - Open a video and scroll down to load all comments.
    """
    home_page = "https://www.youtube.com/"

    async def start(self) -> None:
        """
        Start the browser manager and go to the home page(*youtube.com*).

        :return: (None)
        """
        await super().start()
        await self.browser_manager.go(self.home_page)

    async def stop(self) -> None:
        """
        Stop the browser manager.

        :return: (None)
        """
        await super().stop()

    async def search(self, search_term: str) -> None:
        """
        Search videos by `search_term`.

        @in_page: any Youtube page

        @out_page: search result page

        :param search_term:  (str) The search term.
        :return: (None)
        """
        await self._type_input_search_term(search_term=search_term)
        await self.page_interactor.click(selector=search_submit_sel, new_page=True)

    async def _type_input_search_term(self, search_term: str) -> None:
        """
        Type input the search term.

        :param search_term: (str) The search term.
        :return: (None)
        """
        # 1. clear the input
        await self.page_interactor.click(selector=clear_input_btn_selector)

        # 2. type the input
        await self.page_interactor.type_input(selector=search_input_sel, text=search_term)

        # 3. focus on the input
        await self.page_interactor.click(selector=search_input_sel)

    async def filter_search_result(self, filter_section: FilterSection, filter_option) -> None:
        """
        Filter the search result.

        @in_page: search result page

        @out_page: search result page

        :param filter_section: (int) The filter section.
        :param filter_option:  (int) The index of the filter option.
        :return: (None)
        """
        # 1. 打开 filter modal
        await self.page_interactor.click(selector=filter_toggle_sel)

        # 2. 选择 filter
        filter_group_list = await self.page_interactor.get_elements(filter_section_sel)
        filter_group = filter_group_list[filter_section.value]
        filter_group_name_elem = await filter_group.querySelector("#filter-group-name")
        filter_title = (await self.data_extractor.get_text(filter_group_name_elem)).strip()
        filter_option_elem_list = await filter_group.querySelectorAll(filter_option_sel)
        filter_option_elem = await filter_option_elem_list[filter_option.value].querySelector("a")
        option_text = (await self.data_extractor.get_text(filter_option_elem)).strip()

        # 3. 点击 filter
        self.debug_tool.logger.debug(
            f"Filtering searching result, filter_section_title: {filter_title}, option: {option_text}")
        await filter_option_elem.click()

    async def scroll_load_video_cards(self, n_target: int) -> List[pyppeteer.element_handle.ElementHandle]:
        """
        Scroll down to load more video cards.

        @in_page: search result page

        @out_page: search result page

        :param n_target: (int) The target number of video cards to load.
        :return: (List[ElementHandle]) The list of video card elements.
        """
        video_selector = "ytd-video-renderer"
        await self.page_interactor.scroll_load_selector(selector=video_selector, threshold=n_target)
        return await self.page_interactor.get_elements(selector=video_selector)

    async def scroll_load_comments(self, n_target: int) -> List[pyppeteer.element_handle.ElementHandle]:
        """
        Scroll down to load more comments.

        @in_page: video page

        @out_page: video page

        :param n_target: (int) The target number of comments to load.
        :return: (int) The number of comments loaded.
        """
        return await self.page_interactor.scroll_load_selector(selector="ytd-comment-renderer", threshold=n_target)


__all__ = ["YoutubeBrowserAgent"]
