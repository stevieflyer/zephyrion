from typing import Union, List

import playwright.async_api
from gembox.debug_utils import Debugger


class PageInteractor:
    def __init__(self, page, debug_tool: Debugger = None):
        self._page: playwright.async_api.Page = page
        self._debug_tool = Debugger() if debug_tool is None else debug_tool

    @property
    def page(self) -> Union[None, playwright.async_api.Page]:
        return self._page

    @property
    def debug_tool(self) -> Debugger:
        return self._debug_tool

    async def get_element(self, selector: str, strict: bool = False) -> playwright.async_api.ElementHandle:
        """
        Get the element according to the selector.

        If `strict` is True, then when resolving multiple elements, the function will raise Error
        """
        return await self.page.query_selector(selector=selector, strict = strict)

    async def get_elements(self, selector: str) -> List[playwright.async_api.ElementHandle]:
        return await self.page.query_selector_all(selector=selector)

    async def click(self, selector: str):
        return await self.page.click(selector=selector)

    async def type_input(self, selector: str, text: str):
        return await self.page.type(selector=selector, text=text)
