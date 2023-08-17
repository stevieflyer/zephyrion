from functools import wraps

from .interface import JsHandler
from .generator import JsGenerator


def execute_js(f):
    """
    Decorator for executing javascript code.

    Return RAW javascript result. Usually a `dict` or `str`.
    """
    @wraps(f)
    async def decorator(self, *args, **kwargs):
        js_code = await f(self, *args, **kwargs)
        if js_code:
            result = await self._js_executor.exec_js(js_code)
            return result
    return decorator


class JsClassListHandler(JsHandler):
    async def get_class_list(self, selector):
        raw_result: dict = await self._get_class_list(selector=selector)
        return list(raw_result.values())

    @execute_js
    async def _get_class_list(self, selector: str):
        return JsGenerator.get_class_list(selector=selector)

    async def add_class(self, selector, class_name):
        return await self._add_class(selector=selector, class_name=class_name)

    @execute_js
    async def _add_class(self, selector: str, class_name: str):
        return JsGenerator.add_class(selector=selector, class_name=class_name)

    async def remove_class(self, selector, class_name):
        return await self._remove_class(selector=selector, class_name=class_name)

    @execute_js
    async def _remove_class(self, selector: str, class_name: str):
        return JsGenerator.remove_class(selector=selector, class_name=class_name)

    async def toggle_class(self, selector, class_name):
        return await self._toggle_class(selector=selector, class_name=class_name)

    @execute_js
    async def _toggle_class(self, selector: str, class_name: str):
        return JsGenerator.toggle_class(selector=selector, class_name=class_name)


class JsAttrHandler(JsHandler):
    async def get_attr(self, selector, attr):
        raw_result = await self._get_attr(selector=selector, attr=attr)
        return raw_result

    @execute_js
    async def _get_attr(self, selector: str, attr: str):
        return JsGenerator.get_attr(selector=selector, attr=attr)

    async def set_attr(self, selector, attr, value):
        return await self._set_attr(selector=selector, attr=attr, value=value)

    @execute_js
    async def _set_attr(self, selector: str, attr: str, value: str):
        return JsGenerator.set_attr(selector=selector, attr=attr, value=value)


class JsActionHandler(JsHandler):
    async def click(self, selector):
        return await self._click(selector)

    @execute_js
    async def _click(self, selector: str):
        return JsGenerator.click(selector=selector)

    async def submit(self, selector):
        return await self._submit(selector)

    @execute_js
    async def _submit(self, selector: str):
        return JsGenerator.submit(selector=selector)

    async def focus(self, selector):
        return await self._focus(selector)

    @execute_js
    async def _focus(self, selector: str):
        return JsGenerator.focus(selector=selector)

    async def blur(self, selector):
        return await self._blur(selector)

    @execute_js
    async def _blur(self, selector: str):
        return JsGenerator.blur(selector=selector)

    async def select(self, selector):
        return await self._select(selector)

    @execute_js
    async def _select(self, selector: str):
        return JsGenerator.select(selector=selector)


class JsScrollHandler(JsHandler):
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


__all__ = [
    "JsAttrHandler",
    "JsActionHandler",
    "JsClassListHandler",
    "JsScrollHandler",
]
