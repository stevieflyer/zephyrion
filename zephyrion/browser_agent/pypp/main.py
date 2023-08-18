import pathlib
from typing import Union

from .data_extractor import DataExtractor
from .page_interactor import PageInteractor
from .browser_manager import SinglePageBrowser
from utils.debug_utils import Debugger


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

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


__all__ = ["PyppeteerAgent"]
