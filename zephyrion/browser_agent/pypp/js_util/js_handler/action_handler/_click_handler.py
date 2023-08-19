from zephyrion.browser_agent.pypp.js_util.interface import JsHandler
from zephyrion.browser_agent.pypp.js_util.js_handler.action_handler.common import JsActionHandler
from zephyrion.browser_agent.pypp.page_interactor._decorator import wait_for_selector


class ClickHandler(JsHandler):
    """
    Handler for clicking on elements.
    """
    @wait_for_selector
    async def click(self, selector: str, new_page: bool = False, new_page_wait: float = 1000.):
        """
        Click on an element.

        :param selector: (str) Selector of the element to click
        :param new_page: (bool) Whether to wait for a new page to load, if True, an extra wait time will be added
        :param new_page_wait: (float) Extra wait time in milliseconds for new page to load
        """
        action_handler = JsActionHandler(js_executor=self._js_executor, page=self._page, debug_tool=self.debug_tool)
        self.debug_tool.info(f"Clicking {selector}...")

        await action_handler.click(selector=selector)
        self.debug_tool.info(f'{selector} clicked successfully')
        if new_page:
            self.debug_tool.info(f'waiting for new page to load...')
            await self._page.waitFor(new_page_wait)


__all__ = ['ClickHandler']
