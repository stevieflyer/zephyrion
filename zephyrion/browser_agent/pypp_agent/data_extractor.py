import pyppeteer.page

from zephyrion.utils.debug_utils import Debugger
from zephyrion.browser_agent.pypp_agent.js_util.handler import JsAttrHandler
from zephyrion.browser_agent.pypp_agent.js_util.interface import JsExecutor


class DataExtractor(JsExecutor):
    def __init__(self, page: pyppeteer.page.Page, debug_tool: Debugger = None):
        self._page: pyppeteer.page.Page = page
        assert isinstance(self._page, pyppeteer.page.Page)
        self._debug_tool = debug_tool if debug_tool else Debugger()
        self._attr_handler = JsAttrHandler()

    async def extract_text(self, selector):
        # Extract text logic
        pass

    async def extract_texts(self, selector):
        # Extract texts logic
        pass

    async def extract_attribute(self, selector, attribute):
        # Extract attribute logic
        pass

    async def extract_cls_list(self, selector):
        # Extract class list logic
        pass

    async def has_cls(self, selector, cls):
        # Check if element has class logic
        pass

    async def count_elements(self, selector):
        n_elements = await self._attr_handler.co

    async def getScrollTop(self):
        # Get scroll top position logic
        pass

    async def getScrollHeight(self):
        # Get scroll height logic
        pass

    async def nearScrollBottom(self):
        # Check if near scroll bottom logic
        pass



    async def has_after_pseudo_elements(self, selector):
        has_before = await self.exec_js('''(selector) => {
            const element = document.querySelector(selector);
            if (!element) {
                return false;
            }
            const after = window.getComputedStyle(element, '::after');
            return after.content !== 'none';
        }''', selector)

        return has_before

    async def get_attribute(self, selector, attribute):
        # Get attribute logic
        pass

    async def exec_js(self, js: str):
        """
        Execute JavaScript code on the page.

        :param js: JavaScript code string to be executed.
        :return: Result of the JavaScript execution.
        """
        return await self._page.evaluate(js)


__all__ = ["DataExtractor"]
