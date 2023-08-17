"""
Common Javascript Handlers for actions on elements. *Common* means that other handlers may build upon these.

include:
- `JsQueryHandler`
- `JsAttrHandler`
- `JsClassHandler`
"""
import json

from typing import List
import pyppeteer.element_handle

from zephyrion.browser_agent.pypp_agent.js_util.decorator import execute_js
from zephyrion.browser_agent.pypp_agent.js_util.interface import JsHandler
from zephyrion.browser_agent.pypp_agent.js_util.js_generator import JsGenerator


class JsQueryHandler(JsHandler):
    """
    Javascript Handler for querying elements and pseudo elements.
    """
    async def query_one(self, selector: str) -> pyppeteer.element_handle.ElementHandle:
        """
        Get the first element matching the selector.

        :param selector: (str) Selector of the element to get
        :return: (pyppeteer.element_handle.ElementHandle) Element matching the selector
        """
        return await self._page.querySelector(selector)

    async def query_all(self, selector: str) -> List[pyppeteer.element_handle.ElementHandle]:
        """
        Get all elements matching the selector.

        :param selector: (str) Selector of the element to get
        :return: (list) List of elements matching the selector
        """
        return await self._page.querySelectorAll(selector)

    async def count(self, selector: str) -> int:
        """
        Count the number of elements matching the selector.

        :param selector: (str) Selector of the element to count
        :return: (int) Number of elements matching the selector
        """
        elements = await self.query_all(selector)
        n_elements = 0 if elements is None else len(elements)
        return n_elements

    @execute_js
    async def extract_text(self, selector: str) -> str:
        """
        Get the text content of the first element matching the selector.

        :param selector: (str) Selector of the element to get
        :return: (str) Text content of the first element matching the selector
        """
        return JsGenerator.get_text_content(selector)

    async def extract_texts(self, selector: str) -> List[str]:
        """
        Get the text content of all elements matching the selector.

        :param selector: (str) Selector of the element to get
        :return:
        """

    @execute_js
    async def has_before_pseudo_elements(self, selector: str) -> str:
        js_code_to_exec = f'''
            (function(selector) {{
                const element = document.querySelector(selector);
                if (!element) {{
                    return false;
                }}
                const before = window.getComputedStyle(element, '::before');
                return {{ hasBefore: before.content !== 'none' }};
            }})({json.dumps(selector)})
        '''
        return js_code_to_exec

    @execute_js
    async def has_after_pseudo_elements(self, selector: str) -> str:
        js_code_to_exec = f'''
            (function(selector) {{
                const element = document.querySelector(selector);
                if (!element) {{
                    return false;
                }}
                const after = window.getComputedStyle(element, '::after');
                return {{ hasAfter: after.content !== 'none' }};
            }})({json.dumps(selector)})
        '''
        return js_code_to_exec


class JsAttrHandler(JsHandler):
    """
    Javascript Handler for attribute manipulation.
    """
    async def get_attr(self, selector: str, attr: str):
        """
        Get the value of an attribute of an element.

        :param selector: (str) Selector of the element to get
        :param attr: (str) Attribute to get, e.g. 'href'
        :return: (Any) Value of the attribute
        """
        raw_result = await self._get_attr(selector=selector, attr=attr)
        return raw_result

    @execute_js
    async def _get_attr(self, selector: str, attr: str):
        return JsGenerator.get_attr(selector=selector, attr=attr)

    async def set_attr(self, selector, attr, value) -> None:
        """
        Set the value of an attribute of an element.

        :param selector: (str) Selector of the element to set
        :param attr: (str) Attribute to set, e.g. 'href'
        :param value: (Any) Value to set
        :return: None
        """
        return await self._set_attr(selector=selector, attr=attr, value=value)

    @execute_js
    async def _set_attr(self, selector: str, attr: str, value: str):
        return JsGenerator.set_attr(selector=selector, attr=attr, value=value)


class JsClassHandler(JsHandler):
    """
    Javascript Handler for class list manipulation.
    """
    async def get_class_list(self, selector) -> List[str]:
        """
        Get the class list of an element.

        :param selector: (str) Selector of the element to get
        :return: (list) List of classes
        """
        cls_dict: dict = await self._get_class_list(selector=selector)
        return list(cls_dict.values())

    @execute_js
    async def _get_class_list(self, selector: str):
        return JsGenerator.get_class_list(selector=selector)

    async def add_class(self, selector, class_name) -> None:
        """
        Add a class to an element's classList.

        :param selector: (str) Selector of the element to add
        :param class_name: (str) Class to add
        :return: (None)
        """
        return await self._add_class(selector=selector, class_name=class_name)

    @execute_js
    async def _add_class(self, selector: str, class_name: str):
        return JsGenerator.add_class(selector=selector, class_name=class_name)

    async def remove_class(self, selector, class_name) -> None:
        """
        Remove a class from an element's classList.

        :param selector: (str) Selector of the element to remove
        :param class_name: (str) Class to remove
        :return: (None)
        """
        return await self._remove_class(selector=selector, class_name=class_name)

    @execute_js
    async def _remove_class(self, selector: str, class_name: str):
        return JsGenerator.remove_class(selector=selector, class_name=class_name)

    async def toggle_class(self, selector, class_name) -> None:
        """
        Toggle a class on an element's classList.

        :param selector: (str) Selector of the element to toggle
        :param class_name: (str) Class to toggle
        :return: (None)
        """
        return await self._toggle_class(selector=selector, class_name=class_name)

    @execute_js
    async def _toggle_class(self, selector: str, class_name: str):
        return JsGenerator.toggle_class(selector=selector, class_name=class_name)


__all__ = ["JsClassHandler", "JsAttrHandler", "JsQueryHandler"]
