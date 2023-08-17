from youtube_crawler.filter_enum import FilterSection
from zephyrion.browser_agent.pypp import PyppeteerAgent
from youtube_crawler.selectors.common import search_input_sel, search_submit_sel
from youtube_crawler.selectors.search_result_page import filter_toggle_sel, filter_section_sel, filter_option_sel


class YoutubeAgent(PyppeteerAgent):
    home_page = "https://www.youtube.com/"

    async def start(self) -> None:
        await super().start()
        await self.browser_manager.go(self.home_page)

    async def search(self, search_term: str):
        await self.page_interactor.type_input(selector=search_input_sel, text=search_term)
        await self.page_interactor.click(selector=search_submit_sel, new_page=True)

    async def filter_search_result(self, filter_section: FilterSection, filter_option) -> None:
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
        self._debug_tool.logger.debug(
            f"Filtering searching result, filter_section_title: {filter_title}, option: {option_text}")
        await filter_option_elem.click()
