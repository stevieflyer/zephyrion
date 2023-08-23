import pathlib
from typing import Union, List, Any

import pyppeteer.element_handle
from gembox.debug_utils import Debugger

from .data_extractor import DataExtractor
from .page_interactor import PageInteractor
from .browser_manager import SinglePageBrowser


class PyppeteerAgent:
    """
    Agent class for managing browser instances and page interactions.
    """
    def __init__(self, headless=False, debug_tool: Debugger = None, interactor_config_path: Union[str, pathlib.Path] = None):
        """
        :param headless: (bool) Whether to run the browser in headless mode
        :param debug_tool: (Debugger) Debugger instance for debugging
        :param interactor_config_path: (str, pathlib.Path) Path to the page interaction config file
        """
        self.debug_tool = debug_tool if debug_tool is not None else Debugger()
        self._interactor_config_path = interactor_config_path
        self.browser_manager = SinglePageBrowser(headless=headless, debug_tool=self.debug_tool)
        self.page_interactor: Union[PageInteractor, None] = None
        self.data_extractor: Union[DataExtractor, None] = None

    @property
    def interactor_config_path(self) -> Union[str, pathlib.Path]:
        """Path to the page interaction config file"""
        return self._interactor_config_path

    @property
    def is_running(self) -> bool:
        """Check if the browser is running"""
        return self.browser_manager.is_running

    @property
    def url(self) -> str:
        """Return the current url of the page."""
        return self.page_interactor.url

    # Context management
    async def start(self) -> None:
        """
        Start the browser and initialize the page interactor and data extractor.

        :return: (None)
        """
        self.debug_tool.debug(f"Starting PyppeteerAgent...")
        await self.browser_manager.start_browser()
        page = await self.browser_manager.get_page()
        self.page_interactor = PageInteractor(page=page, debug_tool=self.debug_tool, config_path=self.interactor_config_path)
        self.data_extractor = DataExtractor(page=page, debug_tool=self.debug_tool)
        assert self.is_running is True, "Browser is not running successfully"
        self.debug_tool.debug(f"Starting PyppeteerAgent Successfully")

    async def stop(self) -> None:
        """
        Close the browser and release the page interactor and data extractor.

        :return: (None)
        """
        await self.browser_manager.close_browser()
        self.page_interactor = None
        self.data_extractor = None
        assert self.is_running is False, "Browser is not closed successfully"

    # Page interactions
    async def click(self, selector: str, new_page: bool = False):
        """
        Click on the element specified by the selector.

        :param selector: (str) Selector for the element to click
        :param new_page: (bool) Whether to open a new page after clicking
        :return: (None)
        """
        return await self.page_interactor.click(selector=selector, new_page=new_page)

    async def type_input(self, selector: str, text: str):
        """
        Type text into an input element.

        :param selector: (str) Selector of the element to type into
        :param text: (str) Text to type
        :return:
        """
        return await self.page_interactor.type_input(selector=selector, text=text)

    async def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page.
        """
        return await self.page_interactor.scroll_to_bottom()

    async def scroll_to_top(self):
        """
        Scroll to the top of the page.
        """
        return await self.page_interactor.scroll_to_top()

    async def scroll_to(self, x: int, y: int):
        """
        Scroll to a specific position of the page.

        :param x: (int) x coordinate
        :param y: (int) y coordinate
        """
        return await self.page_interactor.scroll_to(x=x, y=y)

    async def scroll_by(self, x_disp: int, y_disp: int):
        """
        Scroll by a specific displacement.

        :param x_disp: (int) x displacement
        :param y_disp:  (int) y displacement
        :return:
        """
        return await self.page_interactor.scroll_by(x_disp=x_disp, y_disp=y_disp)

    async def scroll_load(self, scroll_step: int = 400, load_wait: int = 40, same_th: int = 20, scroll_step_callbacks: List[callable] = None):
        """
        Scroll and load all contents, until no new content is loaded.

        :param scroll_step: (int) The number of pixels to scroll each time. If None, scroll to bottom.
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param scroll_step_callbacks: (List[Callable]) A callback function that will be called after each scroll.
        :return:
        """
        return await self.page_interactor.scroll_load(scroll_step=scroll_step, load_wait=load_wait, same_th=same_th,
                                                      scroll_step_callbacks=scroll_step_callbacks)

    async def scroll_load_selector(self, selector: str, threshold: int = None, scroll_step: int = 400, load_wait: int = 40,
                                   same_th: int = 20, scroll_step_callbacks: List[callable] = None) -> List[pyppeteer.element_handle.ElementHandle]:
        """
        Scroll and load all contents, until no new content is loaded or enough specific items are collected.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :param scroll_step_callbacks: (List[Callable]) A callback function that will be called after each scroll.
        :return: (int) The number of elements matching the selector
        """
        return await self.page_interactor.scroll_load_selector(selector=selector, threshold=threshold, scroll_step=scroll_step,
                                                               load_wait=load_wait, same_th=same_th, scroll_step_callbacks=scroll_step_callbacks)

    # Browser interactions
    async def go_back(self):
        return await self.browser_manager.go_back()

    async def go(self, url: str):
        return await self.browser_manager.go(url=url)

    # data extraction
    async def get_text(self, element: pyppeteer.element_handle.ElementHandle) -> str:
        """
        Extract text from an element.

        :param element: (ElementHandle) Element to extract text from
        :return: (str) Text extracted from the element
        """
        return await self.data_extractor.get_text(element=element)

    async def get_texts(self, selector: str) -> List[str]:
        """
        Extract text from all elements matching the selector.

        :param selector: (str) Selector of the elements to extract text from
        :return: (list) Text extracted from the elements
        """
        return await self.data_extractor.get_texts(selector=selector)

    async def get_attr(self, element: pyppeteer.element_handle.ElementHandle, attribute: str) -> Any:
        """
        Get attribute of given element

        :param element: (ElementHandle) Element to get attribute from
        :param attribute: (str) Attribute to get
        :return: (Any) Attribute of given element
        """
        return await self.data_extractor.get_attr(element=element, attribute=attribute)

    async def get_cls_list(self, element: pyppeteer.element_handle.ElementHandle) -> List[Any]:
        """
        Get classList of given element
        :param element: (ElementHandle) Element to get classList from
        :return: (list) List of classList
        """
        return await self.data_extractor.get_cls_list(element=element)

    async def has_cls(self, element: pyppeteer.element_handle.ElementHandle, cls: str) -> bool:
        """
        Check if given element has given class

        :param element: (ElementHandle) Element to check
        :param cls: (str) Class to check
        :return: (bool) True if element has given class, False otherwise
        """
        return await self.data_extractor.has_cls(element=element, cls=cls)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


__all__ = ["PyppeteerAgent"]
