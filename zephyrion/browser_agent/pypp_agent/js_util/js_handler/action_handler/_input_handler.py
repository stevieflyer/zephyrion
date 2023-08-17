from zephyrion.browser_agent.pypp_agent.js_util.interface import JsHandler
from zephyrion.browser_agent.pypp_agent.page_interactor.decorator import wait_for_selector
from zephyrion.browser_agent.pypp_agent.js_util.js_handler.data_handler.common import JsAttrHandler


class InputHandler(JsHandler):
    """
    Handler for inputting text in elements.
    """
    @wait_for_selector
    async def type_input(self, selector: str, text: str) -> None:
        """
        Type text in an input element.

        Sometimes the typing can fail, so we retry for 3 times at most.

        :param selector: (str) Selector of the input element
        :param text: (str) Text to type
        :return: (None)
        """
        current_text = ""
        retry_count, max_retry = 0, 3
        attr_handler = JsAttrHandler(js_executor=self._js_executor)
        self._debug_tool.info(f'Typing {text} in {selector}...')

        while retry_count < max_retry:
            await attr_handler.set_attr(selector, 'value', text)
            current_text = await attr_handler.get_attr(selector, 'value')
            if current_text == text:
                break
            retry_count += 1

        if retry_count >= max_retry:
            err_msg = f'Failed to type {text} in {selector} after {max_retry} retries, current text: {current_text}, target text: {text}'
            self._debug_tool.warn(err_msg)
            raise RuntimeError(err_msg)
        else:
            self._debug_tool.info(f'{text} typed successfully in {selector} in {retry_count} times')


__all__ = ['InputHandler']