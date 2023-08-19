from zephyrion.browser_agent.pypp.js_util.interface import JsHandler
from zephyrion.browser_agent.pypp.page_interactor._decorator import wait_for_selector
from zephyrion.browser_agent.pypp.js_util.js_handler.data_handler.common import JsAttrHandler


class InputHandler(JsHandler):
    """
    Handler for inputting text in elements.
    """
    @wait_for_selector
    async def type_input(self, selector: str, text: str) -> None:
        """
        Type text in an input element.

        :param selector: (str) Selector of the input element
        :param text: (str) Text to type
        :return: (None)
        """
        self.debug_tool.info(f'Typing {text} in {selector}...')
        await self._page.type(selector=selector, text=text)
        self.debug_tool.info(f'{text} typed successfully in {selector}')


__all__ = ['InputHandler']
