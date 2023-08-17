import pyppeteer.page
import pyppeteer.element_handle

from zephyrion.browser_agent.pypp_agent.debugger import Debugger
from zephyrion.browser_agent.pypp_agent.js_util.interface import JsExecutor
from zephyrion.browser_agent.pypp_agent.page_interactor.config import PageInteractionConfig


class BaseHandler:
    def __init__(self, page: pyppeteer.page.Page, js_executor: JsExecutor, debug_tool=None, config=None):
        self._page = page
        self._js_executor = js_executor
        """general javascript code handler"""
        if not isinstance(self._js_executor, JsExecutor):
            raise TypeError(f'js_executor should be an instance of JsExecutor, got {type(js_executor)}')
        self._debug_tool = debug_tool if debug_tool else Debugger()
        self._config = config if config else PageInteractionConfig()

    async def query_one(self, selector: str) -> pyppeteer.element_handle.ElementHandle:
        """
        Get the first element matching the selector.

        :param selector: (str) Selector of the element to get
        :return: (pyppeteer.element_handle.ElementHandle) Element matching the selector
        """
        return await self._page.querySelector(selector)

    async def query_all(self, selector: str) -> list:
        """
        Get all elements matching the selector.

        :param selector: (str) Selector of the element to get
        :return: (list) List of elements matching the selector
        """
        return await self._page.querySelectorAll(selector)

    async def count(self, selector: str) -> int:
        """
        Count the number of elements matching the selector.

        :param selector: (str) Selector of the element to count
        :return: (int) Number of elements matching the selector
        """
        elements = await self.query_all(selector)
        return len(elements)


__all__ = ['BaseHandler']
