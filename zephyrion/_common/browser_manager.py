import abc
from functools import wraps

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


class SinglePageBrowserBase(abc.ABC):
    """
    Browser manager class for managing browser instances.

    To avoid troubles, **only one browser instance** is allowed to run at a time,
    and **only one page** is allowed to be used.
    """

    def __init__(self, headless=True, debug_tool: Debugger = None):
        self._is_running: bool = False
        """whether browser is running"""
        self._browser = None
        """Singleton browser instance"""
        self._headless: bool = headless
        """whether browser is headless"""
        self._debug_tool = debug_tool if debug_tool is not None else Debugger()
        """Debugger instance"""

    @property
    def is_running(self) -> bool:
        """whether browser is running"""
        return self._is_running

    @property
    def headless(self) -> bool:
        """whether browser is headless"""
        return self._headless

    @property
    def debug_tool(self):
        return self._debug_tool

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """Return the current url of the page."""
        raise NotImplementedError

    @abc.abstractmethod
    async def start_browser(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def close_browser(self) -> None:
        raise NotImplementedError

    async def restart_browser(self) -> None:
        await self.close_browser()
        await self.start_browser()

    async def go_back(self) -> None:
        self.debug_tool.info(f"Browser: Go back")
        await self._go_back()
        self.debug_tool.info(f"Browser: Go back successfully")

    @abc.abstractmethod
    async def _go_back(self):
        raise NotImplementedError

    async def go(self, url: str) -> None:
        self.debug_tool.info(f"Browser: Go to {url}")
        await self._go(url)
        self.debug_tool.info(f"Browser: Go to {url} successfully")

    @abc.abstractmethod
    async def _go(self, url: str):
        raise NotImplementedError
