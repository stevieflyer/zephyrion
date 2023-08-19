from typing import Union
from functools import wraps

import pyppeteer.page
import pyppeteer.browser
from pyppeteer import launch
from gembox.debug_utils import Debugger


class BrowserNotRunningError(Exception):
    def __init__(self, message=f"Browser is not running"):
        super().__init__(message)


class NoActivePageError(Exception):
    def __init__(self, message=f"No active page found"):
        super().__init__(message)


class NonSingletonError(Exception):
    def __init__(self, message=f"Only one browser instance and one page is allowed"):
        super().__init__(message)


def ensure_browser_is_running(func):
    @wraps(func)
    async def wrapper(browser_mgr, *args, **kwargs):
        if browser_mgr.is_running is False:
            raise BrowserNotRunningError()
        return await func(browser_mgr, *args, **kwargs)

    return wrapper


def ensure_the_page(func):
    @wraps(func)
    async def wrapper(browser_mgr: "SinglePageBrowser", *args, **kwargs):
        the_page = kwargs.pop("page", None)
        # if no `active_page` is provided, get it from `browser_mgr`
        if the_page is None:
            the_page = await browser_mgr.get_page()
        # if active_page is still null, raise error
        if the_page is None:
            raise NoActivePageError()
        return await func(browser_mgr, *args, page=the_page, **kwargs)

    return wrapper


class SinglePageBrowser:
    """
    Browser manager class for managing browser instances.

    To avoid troubles, **only one browser instance** is allowed to run at a time,
    and **only one page** is allowed to be used.
    """

    def __init__(self, browser_options=None, headless=True, debug_tool=None):
        self._is_running: bool = False
        """whether browser is running"""
        self._browser: Union[pyppeteer.browser.Browser, None] = None
        """Singleton browser instance"""
        self._headless: bool = headless
        """whether browser is headless"""
        self._browser_options: dict = browser_options if browser_options is not None else {}
        self._debug_tool = debug_tool if debug_tool is not None else Debugger()

    @property
    def is_running(self) -> bool:
        """whether browser is running"""
        return self._is_running

    @property
    def headless(self) -> bool:
        """whether browser is headless"""
        return self._headless

    async def get_page(self) -> Union[pyppeteer.page.Page, None]:
        """get the active only page, if more than one pages are found, raise error"""
        if not self.is_running:
            return None
        pages = await self._browser.pages()
        if len(pages) == 0:
            return None
        if len(pages) == 1:
            return pages[0]
        raise NonSingletonError(f"Only one page is allowed to be used, but {len(pages)} pages are found")

    async def start_browser(self) -> None:
        page = await self.get_page()
        if page is not None and self._is_running:
            self._debug_tool.warn(f"Browser: Already running.")
        else:
            self._browser = await launch(headless=self._headless, **self._browser_options)
            self._is_running = True

    async def close_browser(self) -> None:
        if not self._is_running or not self._browser:
            self._debug_tool.warn(f"Browser: Not running, no need to close.")
        else:
            await self._browser.close()
            self._browser = None
            self._is_running = False

    async def restart_browser(self) -> None:
        await self.close_browser()
        await self.start_browser()

    @ensure_the_page
    async def get_url(self, page: pyppeteer.page.Page) -> str:
        return page.url

    @ensure_the_page
    async def get_cookies(self, page: pyppeteer.page.Page) -> list[dict[str, Union[str, int, bool]]]:
        return await page.cookies()

    @ensure_the_page
    async def refresh_cookies(self, page: pyppeteer.page.Page):
        """
        Refresh the current page and get the cookies

        :return: (str) cookies
        """
        await page.reload()
        return await self.get_cookies(page=page)

    @ensure_the_page
    async def go_back(self, page: pyppeteer.page.Page) -> None:
        self._debug_tool.info(f"Browser: Go back")
        await page.goBack()

    @ensure_the_page
    async def go(self, url, page: pyppeteer.page.Page) -> None:
        self._debug_tool.info(f"Browser: Go to {url}")
        await page.goto(url)


__all__ = ["SinglePageBrowser"]
