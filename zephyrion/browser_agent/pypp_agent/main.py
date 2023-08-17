from .debugger import Debugger
from .data_extractor import DataExtractor
from .browser_manager import SinglePageBrowser
from .page_interactor import PageInteractor


class PyppeteerAgent:
    def __init__(self, headless=True):
        self.debug_tool = Debugger()
        self.browser_manager = SinglePageBrowser(self.debug_tool, headless=headless)
        self.page_interactor = PageInteractor(self.browser_manager.get_page, self.debug_tool)
        self.data_extractor = DataExtractor(self.browser_manager.get_page, self.debug_tool)

    async def screenshot(self, path):
        # Screenshot logic
        pass

    async def get_cookies(self):
        # Get cookies logic
        pass

    async def refresh_cookies(self):
        # Refresh cookies logic
        pass


__all__ = ["PyppeteerAgent"]
