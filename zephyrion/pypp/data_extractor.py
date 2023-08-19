from typing import List, Any

import pyppeteer.page
from gembox.debug_utils import Debugger
from pyppeteer.element_handle import ElementHandle

from zephyrion.pypp.js_util.js_handler.data_handler.common import JsAttrHandler, JsQueryHandler
from zephyrion.pypp.js_util.interface import JsExecutor


class DataExtractor(JsExecutor):
    """
    Data Extractor for extracting data from elements.
    """
    def __init__(self, page: pyppeteer.page.Page, debug_tool: Debugger = None):
        """
        :param page: (pyppeteer.page.Page) Page to interact with
        :param debug_tool: (Debugger) Debugger to use
        """
        self._page: pyppeteer.page.Page = page
        assert isinstance(self._page, pyppeteer.page.Page)
        self._debug_tool = debug_tool if debug_tool else Debugger()
        self._attr_handler = JsAttrHandler(js_executor=self, page=self._page, debug_tool=self._debug_tool)
        self._query_handler = JsQueryHandler(js_executor=self, page=self._page, debug_tool=self._debug_tool)

    async def get_text(self, element: ElementHandle) -> str:
        """
        Extract text from an element.

        :param element: (ElementHandle) Element to extract text from
        :return: (str) Text extracted from the element
        """
        if not isinstance(element, ElementHandle):
            raise TypeError(f'element should be an instance of ElementHandle, got {type(element)}')
        return await self._page.evaluate('(element) => element.textContent', element)

    async def get_texts(self, selector: str) -> List[str]:
        """
        Extract text from all elements matching the selector.

        :param selector: (str) Selector of the elements to extract text from
        :return: (list) Text extracted from the elements
        """
        elements = await self._page.querySelectorAll(selector)
        return [await self.get_text(element=element) for element in elements]

    async def get_attr(self, element: ElementHandle, attribute: str) -> Any:
        """
        Get attribute of given element

        :param element: (ElementHandle) Element to get attribute from
        :param attribute: (str) Attribute to get
        :return: (Any) Attribute of given element
        """
        return await self._page.evaluate(f'(element) => element.getAttribute("{attribute}")', element)

    async def get_cls_list(self, element: ElementHandle) -> List[Any]:
        """
        Get classList of given element
        :param element: (ElementHandle) Element to get classList from
        :return: (list) List of classList
        """
        cls_dict = await self._page.evaluate('(element) => element.classList', element)
        return list(cls_dict.values())

    async def has_cls(self, element: ElementHandle, cls: str) -> bool:
        """
        Check if given element has given class

        :param element: (ElementHandle) Element to check
        :param cls: (str) Class to check
        :return: (bool) True if element has given class, False otherwise
        """
        cls_list = await self.get_cls_list(element)
        return cls in cls_list

    async def exec_js(self, js: str) -> Any:
        """
        Execute JavaScript code on the page.

        :param js: JavaScript code string to be executed.
        :return: Result of the JavaScript execution.
        """
        return await self._page.evaluate(js)


__all__ = ["DataExtractor"]
