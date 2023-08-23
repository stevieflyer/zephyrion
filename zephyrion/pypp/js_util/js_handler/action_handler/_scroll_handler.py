import time
import asyncio
from typing import List, Callable

import pyppeteer.page
import pyppeteer.element_handle

from zephyrion.pypp.js_util.decorator import execute_js
from zephyrion.pypp.js_util.interface import JsHandler, JsExecutor
from zephyrion.pypp.js_util.js_generator import JsGenerator
from zephyrion.pypp.js_util.js_handler.data_handler.common import JsQueryHandler


class ScrollHandler(JsHandler):
    def __init__(self, page: pyppeteer.page.Page, js_executor: JsExecutor, debug_tool=None):
        super().__init__(page=page, js_executor=js_executor, debug_tool=debug_tool)
        self._js_query_handler = JsQueryHandler(page=page, js_executor=js_executor, debug_tool=debug_tool)

    async def scroll_to(self, x: int, y: int):
        return await self._scroll_to(x=x, y=y)

    @execute_js
    async def _scroll_to(self, x: int, y: int):
        return JsGenerator.scroll_to(x=x, y=y)

    async def scroll_by(self, x_disp: int, y_disp: int):
        return await self._scroll_by(x_disp=x_disp, y_disp=y_disp)

    @execute_js
    async def _scroll_by(self, x_disp: int, y_disp: int):
        return JsGenerator.scroll_by(x_disp=x_disp, y_disp=y_disp)

    async def scroll_to_bottom(self):
        return await self._scroll_to_bottom()

    @execute_js
    async def _scroll_to_bottom(self):
        return JsGenerator.scroll_to_bottom()

    async def scroll_to_top(self):
        return await self._scroll_to_top()

    @execute_js
    async def _scroll_to_top(self):
        return JsGenerator.scroll_to_top()

    async def get_scroll_height(self):
        return await self._get_scroll_height()

    @execute_js
    async def _get_scroll_height(self):
        return JsGenerator.get_scroll_height()

    async def get_scroll_width(self):
        return await self._get_scroll_width()

    @execute_js
    async def _get_scroll_width(self):
        return JsGenerator.get_scroll_width()

    async def get_scroll_top(self):
        return await self._get_scroll_top()

    @execute_js
    async def _get_scroll_top(self):
        return JsGenerator.get_scroll_top()

    async def get_scroll_left(self):
        return await self._get_scroll_left()

    @execute_js
    async def _get_scroll_left(self):
        return JsGenerator.get_scroll_left()

    async def _scroll_step(self, scroll_step: int = None) -> None:
        """
        Scroll by `scroll_step` pixels, if scroll_step is `None`, scroll to bottom.
        """
        if scroll_step is None:
            await self.scroll_to_bottom()
        else:
            await self.scroll_by(0, scroll_step)

    async def scroll_load(self, scroll_step: int = 400, load_wait: int = 40, same_th: int = 20, scroll_step_callbacks: List[Callable] = None):
        """
        Scroll and load all contents, until no new content is loaded.

        :param scroll_step: (int) The number of pixels to scroll each time. If None, scroll to bottom.
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param scroll_step_callbacks: (List[Callable]) A callback function to be called after each scroll.
        :return:
        """
        return await self._scroll_load_(scroll_step=scroll_step, load_wait=load_wait, same_th=same_th, scroll_step_callbacks=scroll_step_callbacks)

    async def scroll_load_selector(self, selector: str, threshold: int = None, scroll_step: int = 400,
                                   load_wait: int = 40, same_th: int = 20, scroll_step_callbacks: List[Callable] = None,
                                   log_interval: int = 100) \
            -> List[pyppeteer.element_handle.ElementHandle]:
        """
        Scroll and load all contents, until no new content is loaded or enough specific items are collected.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :param scroll_step_callbacks: (Callable) A callback function to be called after each scroll.
        :param log_interval: (int) The interval of logging the number of loaded elements.
        :return: (int) The number of elements matching the selector
        """
        self.debug_tool.info(f'Scrolling and loading {selector}...')
        await self._scroll_load_(selector=selector, threshold=threshold, scroll_step=scroll_step, load_wait=load_wait,
                                 same_th=same_th, scroll_step_callbacks=scroll_step_callbacks, log_interval=log_interval)
        n_elements = await self._js_query_handler.count(selector=selector)
        self.debug_tool.info(f'Loaded {n_elements} elements')
        return await self._js_query_handler.query_all(selector=selector)

    async def _scroll_load_(self, selector: str = None, scroll_step: int = None, load_wait: int = 40,
                            same_th: int = 20, threshold: int = None, scroll_step_callbacks: List[Callable] = None,
                            log_interval: int = 100) -> None:
        """
        Scroll and load all contents.

        It's very common to scroll to the bottom and wait for the page to load until no new content is loaded or enough
        specific items are collected.
        Or you just want to load the whole page.
        This method is to do that.

        :param selector: (str) The selector of the element to scroll. If None, the method will just scroll to the bottom
        :param scroll_step: (int) The scroll step in pixels. If none, each scroll will be `scroll_to_bottom`
        :param load_wait: (int) The time to wait after each scroll, in milliseconds. If none, the method will wait for 100 ms
        :param same_th: (int) The threshold of the number of same scroll top to stop scrolling.
        :param threshold: (int) only valid when `selector` is not `None`, after loading `threshold` number of elements, the method will stop scrolling
        :param scroll_step_callbacks: (List[Callable]) A callback function to be called after each scroll.
        :log_interval: (int) The interval of logging the number of loaded elements.
        :return: (None)
        """
        same_count = 0
        last_top = None
        self.debug_tool.info(f'Inner Call Scrolling and loading...(selector={selector}, scroll_step={scroll_step}, load_wait={load_wait}, same_th={same_th}, threshold={threshold})')
        count, prev_count = 0, 0

        while True:
            if selector is not None:
                count = await self._js_query_handler.count(selector=selector)
                if threshold is not None or selector is not None:
                    if count >= threshold:
                        self.debug_tool.info(f'Loaded {count} elements(exceed threshold {threshold}), stop scrolling')
                        break
                    else:
                        if count - prev_count >= log_interval:
                            self.debug_tool.info(f'Loaded {count} elements(sel: {selector}), threshold: {threshold}.')
                            prev_count = count
            await self._scroll_step(scroll_step)
            if scroll_step_callbacks is not None and len(scroll_step_callbacks) > 0:
                for scroll_step_cb in scroll_step_callbacks:
                    if asyncio.iscoroutinefunction(scroll_step_cb):
                        await scroll_step_cb()
                    else:
                        scroll_step_cb()
            time.sleep(load_wait / 1000.)
            top = await self.get_scroll_top()
            self.debug_tool.debug(f'Scroll top: {top}, last top: {last_top}')
            if top == last_top:
                same_count += 1
                self.debug_tool.info(f'Top unchanged, Scroll top: {top}, last top: {last_top}, same count: {same_count}, same_th: {same_th}')
                if same_count >= same_th:
                    break
            else:
                same_count = 0
            last_top = top


__all__ = ['ScrollHandler']
