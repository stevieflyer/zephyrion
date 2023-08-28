from typing import Union

import playwright
from playwright.async_api import async_playwright
from gembox.debug_utils import Debugger

from .._common.browser_manager import NoActivePageError


class SingleBrowserManager:
    def __init__(self,
                 wright: playwright.async_api.Playwright,
                 headless=True,
                 debug_tool: Debugger = None) -> None:
        """
        Initialize the SingleBrowserManager.

        **Note: You should create a instance by calling `SingleBrowserManager.create()` instead of `SingleBrowserManager()`**
        """
        self._wright = wright
        self._headless: bool = headless
        self._debug_tool = debug_tool if debug_tool is not None else Debugger()
        self._is_running: bool = False
        self._browser: [playwright.async_api.Browser, None] = None
        self._context: [playwright.async_api.BrowserContext, None] = None
        self._page: [playwright.async_api.Page, None] = None

    @property
    def headless(self) -> bool:
        """whether browser is headless"""
        return self._headless

    @property
    def debug_tool(self):
        """the debugger"""
        return self._debug_tool

    @property
    def wright(self) -> playwright.async_api.Playwright:
        """the playwright instance"""
        return self._wright

    @property
    def is_running(self) -> bool:
        """whether the browser is running"""
        return self._is_running

    @property
    def browser(self) -> Union[playwright.async_api.Browser, None]:
        """the context manager"""
        return self._browser

    @property
    def context(self) -> Union[playwright.async_api.BrowserContext, None]:
        return self._context

    @property
    def page(self) -> Union[playwright.async_api.Page, None]:
        """the page"""
        return self._page

    @classmethod
    async def create(cls, headless=True, debug_tool: Debugger = None):
        wright = await (async_playwright().start())
        instance = cls(wright=wright, headless=headless, debug_tool=debug_tool)
        return instance

    async def start(self, **kwargs):
        self.debug_tool.info(f"[Browser Manager]: Starting browser...")
        if self.is_running is True:
            self.debug_tool.warn(f"[Browser Manager]: Browser is already running, no need to start_browser.")
            return
        self._browser = await self.wright.chromium.launch(headless=self.headless, **kwargs)
        self._context = await self._browser.new_context(viewport={'width': 1920, 'height': 1080})
        self._page = await self._context.new_page()
        self._is_running = True
        self.debug_tool.info(f"[Browser Manager]: Browser started successfully.")

    async def close(self):
        self.debug_tool.info(f"[Browser Manager]: Closing browser...")
        if self.is_running is False:
            self.debug_tool.warn(f"Browser is not running, no need to close_browser.")
            return
        await self.browser.close()
        self._browser = None
        self._context = None
        self._page = None
        self._is_running = False
        self.debug_tool.info(f"[Browser Manager]: Browser closed successfully.")

    async def restart(self):
        await self.close()
        await self.start()

    async def go(self, url: str, **kwargs):
        if self.page is None:
            raise NoActivePageError
        await self.page.goto(url=url, **kwargs)

    async def go_back(self, **kwargs):
        if self.page is None:
            raise NoActivePageError
        await self.page.go_back(**kwargs)

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
