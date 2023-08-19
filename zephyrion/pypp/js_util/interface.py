import abc
import pyppeteer.page

from gembox.debug_utils import Debugger


class JsExecutor(abc.ABC):
    """
    Javascript executor interface.

    Every `JsExecutor` can execute any javascript code.
    """
    @abc.abstractmethod
    async def exec_js(self, js: str):
        """
        Execute javascript code.

        This interface does not define the return value specifications.

        :param js: (str) Javascript code to execute
        :return:
        """
        raise NotImplementedError()


class JsHandler:
    """
    Javascript code handler.

    This class is used to execute javascript code in specific usage case.
    """
    def __init__(self, page: pyppeteer.page.Page, js_executor: JsExecutor, debug_tool=None):
        """
        :param page: (pyppeteer.page.Page) Page to interact with
        :param js_executor: (JsExecutor) Javascript executor to use
        :param debug_tool: (Debugger) Debugger to use
        """
        self._page = page
        self._js_executor = js_executor
        """general javascript code handler"""
        if not isinstance(self._js_executor, JsExecutor):
            raise TypeError(f'js_executor should be an instance of JsExecutor, got {type(js_executor)}')
        self.debug_tool = debug_tool if debug_tool else Debugger()

    @property
    def js_executor(self):
        """
        Javascript executor used by this handler.
        """
        return self._js_executor


__all__ = ['JsExecutor', 'JsHandler']
