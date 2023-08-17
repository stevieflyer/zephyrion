from .base_handler import BaseHandler
from ..decorator import wait_for_selector
from zephyrion.browser_agent.pypp_agent.js_util.handler import JsActionHandler


class ClickHandler(BaseHandler):
    @wait_for_selector
    async def click(self, selector: str, new_page: bool = False):
        """
        Click on an element.

        :param selector: (str) Selector of the element to click
        :param new_page: (bool) Whether to wait for a new page to load, if True, an extra wait time will be added
        """
        action_handler = JsActionHandler(js_executor=self._js_executor)
        self._debug_tool.info(f"Clicking {selector}...")
        await action_handler.click(selector=selector)
        self._debug_tool.info(f'{selector} clicked successfully')
        if new_page:
            self._debug_tool.info(f'waiting for new page to load...')
            await self._page.waitFor(self._config.new_page_wait)


__all__ = ['ClickHandler']
