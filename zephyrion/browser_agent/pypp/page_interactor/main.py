from typing import List

import pyppeteer.page
import pyppeteer.element_handle

from .config import PageInteractionConfig
from ..js_util.interface import JsExecutor
from zephyrion.utils.debug_utils import Debugger
from ..js_util.js_handler.action_handler import ClickHandler, InputHandler, ScrollHandler


class PageInteractor(JsExecutor):
    """
    Pyppeteer-based Page Interactor.

    This class is a facade class that provides a high-level interface for interacting with a page.
    """

    def __init__(self, page: pyppeteer.page.Page, config_path: str = None, debug_tool: 'Debugger' = None):
        """
        Initialize the PageInteractor.

        :param page: Pyppeteer page object.
        :param config_path: Path to the interaction configuration. Defaults to None.
        :param debug_tool: Debugging tool. Defaults to Debugger instance.
        """
        # initialize self
        self._page: pyppeteer.page.Page = page
        assert isinstance(self._page, pyppeteer.page.Page)
        self._config_path = config_path
        self._debug_tool = debug_tool if debug_tool else Debugger()
        self._config: PageInteractionConfig = PageInteractionConfig()
        if self._config_path:
            self._config.parse_config(self._config_path)
        # initialize handlers
        self.click_handler = ClickHandler(page=self._page, js_executor=self, debug_tool=self._debug_tool)
        self.input_handler = InputHandler(page=self._page, js_executor=self, debug_tool=self._debug_tool)
        self.scroll_handler = ScrollHandler(page=self._page, js_executor=self, debug_tool=self._debug_tool)

    async def get_element(self, selector: str) -> pyppeteer.element_handle.ElementHandle:
        return await self._page.querySelector(selector=selector)

    async def get_elements(self, selector: str) -> List[pyppeteer.element_handle.ElementHandle]:
        return await self._page.querySelectorAll(selector=selector)

    # click related
    async def click(self, selector: str, new_page: bool = False):
        """
        Click on an element.

        :param selector: (str) Selector of the element to click
        :param new_page: (bool) Whether to wait for a new page to load, if True, an extra wait time will be added
        :return:
        """
        return await self.click_handler.click(selector=selector, new_page=new_page, new_page_wait=self._config.new_page_wait)

    # type related
    async def type_input(self, selector: str, text: str):
        """
        Type text into an input element.

        :param selector: (str) Selector of the element to type into
        :param text: (str) Text to type
        :return:
        """

        return await self.input_handler.type_input(selector=selector, text=text)

    # scroll related
    async def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page.
        """
        return await self.scroll_handler.scroll_to_bottom()

    async def scroll_to_top(self):
        """
        Scroll to the top of the page.
        """
        return await self.scroll_handler.scroll_to_top()

    async def scroll_to(self, x: int, y: int):
        """
        Scroll to a specific position of the page.

        :param x: (int) x coordinate
        :param y: (int) y coordinate
        """
        return await self.scroll_handler.scroll_to(x=x, y=y)

    async def scroll_by(self, x_disp: int, y_disp: int):
        """
        Scroll by a specific displacement.

        :param x_disp: (int) x displacement
        :param y_disp:  (int) y displacement
        :return:
        """
        return await self.scroll_handler.scroll_by(x_disp=x_disp, y_disp=y_disp)

    async def scroll_load(self, scroll_step: int = 400, load_wait: int = 40, same_th: int = 20):
        """
        Scroll and load all contents, until no new content is loaded.

        :param scroll_step: (int) The number of pixels to scroll each time. If None, scroll to bottom.
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :return:
        """
        return await self.scroll_handler.scroll_load(scroll_step=scroll_step, load_wait=load_wait, same_th=same_th)

    async def scroll_load_selector(self, selector: str, threshold: int = None, scroll_step: int = 400,
                                   load_wait: int = 40, same_th: int = 20) -> int:
        """
        Scroll and load all contents, until no new content is loaded or enough specific items are collected.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :return: (int) The number of elements matching the selector
        """
        return await self.scroll_handler.scroll_load_selector(selector=selector, threshold=threshold,
                                                              scroll_step=scroll_step, load_wait=load_wait,
                                                              same_th=same_th)

    @property
    def url(self) -> str:
        """Return the current url of the page."""
        return self._page.url

    @property
    def config_path(self) -> str:
        """Return the path to the config file."""
        return self._config_path

    @property
    def config(self) -> PageInteractionConfig:
        """Return the config object."""
        return self._config

    async def exec_js(self, js: str):
        """Execute JavaScript code on the page.

        :param js: JavaScript code string to be executed.
        :return: Result of the JavaScript execution.
        """
        return await self._page.evaluate(js)

    def __str__(self):
        return f"PageInteractor(url={self.url})"

    def __repr__(self):
        return self.__str__()


__all__ = ["PageInteractor"]
