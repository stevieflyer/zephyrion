import time

from .base_handler import BaseHandler
from zephyrion.browser_agent.pypp_agent.js_util.handler import JsScrollHandler


class ScrollHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._js_scroll_handler = JsScrollHandler(js_executor=self._js_executor)

    async def count(self, selector: str) -> int:
        """
        Count the number of elements matching the selector.

        :param selector: (str) Selector of the element to count
        :return: (int) Number of elements matching the selector
        """
        elements = await self.query_all(selector)
        return len(elements)

    async def scroll_to_bottom(self):
        """
        Scroll to the bottom of the page.
        """
        await self._js_scroll_handler.scroll_to_bottom()
        self._debug_tool.info('Scrolled to the bottom of the page')

    async def scroll_to_top(self):
        """
        Scroll to the top of the page.
        """
        await self._js_scroll_handler.scroll_to_top()
        self._debug_tool.info('Scrolled to the top of the page')

    async def scroll_to(self, x: int, y: int):
        """
        Scroll to the middle of the page.
        """
        await self._js_scroll_handler.scroll_to(x, y)
        self._debug_tool.info(f'Scrolled to {x} and {y}')

    async def scroll_by(self, x_disp: int, y_disp: int):
        """
        Scroll by x_disp and y_disp.
        """
        await self._js_scroll_handler.scroll_by(x_disp, y_disp)
        self._debug_tool.info(f'Scrolled by {x_disp} and {y_disp}')

    async def get_scroll_height(self):
        """
        Get the scroll height of the page.
        """
        return await self._js_scroll_handler.get_scroll_height()

    async def get_scroll_width(self):
        """
        Get the scroll width of the page.
        """
        return await self._js_scroll_handler.get_scroll_width()

    async def get_scroll_top(self):
        """
        Get the scroll width of the page
        :return:
        """
        return await self._js_scroll_handler.get_scroll_top()

    async def _scroll_step(self, scroll_step: int = None) -> None:
        """
        Scroll by `scroll_step` pixels, if scroll_step is `None`, scroll to bottom.
        """
        if scroll_step is None:
            await self._js_scroll_handler.scroll_to_bottom()
        else:
            await self._js_scroll_handler.scroll_by(0, scroll_step)

    async def scroll_load(self, scroll_step: int = None, load_wait: int = 40, same_th: int = 20):
        """
        Scroll and load all contents, until no new content is loaded.

        :param scroll_step: (int) The number of pixels to scroll each time. If None, scroll to bottom.
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :return:
        """
        return await self._scroll_load_(scroll_step=scroll_step, load_wait=load_wait, same_th=same_th)

    async def scroll_load_selector(self, selector: str, threshold: int = None, scroll_step: int = None,
                                   load_wait: int = 40, same_th: int = 20) -> int:
        """
        Scroll and load all contents, until no new content is loaded or enough specific items are collected.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :return: (int) The number of elements matching the selector
        """
        self._debug_tool.info(f'Scrolling and loading {selector}...')
        await self._scroll_load_(selector=selector, threshold=threshold, scroll_step=scroll_step, load_wait=load_wait, same_th=same_th)
        n_elements = await self.count(selector)
        self._debug_tool.info(f'Loaded {n_elements} elements')
        return n_elements

    async def _scroll_load_(self, selector: str = None, scroll_step: int = None, load_wait: int = 40,
                            same_th: int = 20, threshold: int = None) -> None:
        """
        Scroll and load all contents.

        It's very common to scroll to the bottom and wait for the page to load until no new content is loaded or enough
        specific items are collected.
        Or you just wanna load the whole page.
        This method is to do that.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :return: (None)
        """
        same_count = 0
        last_top = None
        self._debug_tool.info(f'Inner Call Scrolling and loading...(selector={selector}, scroll_step={scroll_step}, load_wait={load_wait}, same_th={same_th}, threshold={threshold})')
        while True:
            if selector is not None:
                count = await self.count(selector)
                if count >= threshold:
                    self._debug_tool.info(f'Loaded {count} elements(exceed threshold {threshold}), stop scrolling')
                    break
            await self._scroll_step(scroll_step)
            time.sleep(load_wait)
            top = await self.get_scroll_top()
            self._debug_tool.debug(f'Scroll top: {top}, last top: {last_top}')
            if top == last_top:
                same_count += 1
                self._debug_tool.info(f'Top unchanged, Scroll top: {top}, last top: {last_top}, same count: {same_count}, same_th: {same_th}')
                if same_count >= same_th:
                    break
            else:
                same_count = 0
            last_top = top


__all__ = ['ScrollHandler']
