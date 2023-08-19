"""
Common Javascript Handlers for actions on elements. *Common* means that other handlers may build upon these.

Including:

- `JsActionHandler`
"""
from zephyrion.pypp.js_util.interface import JsHandler
from zephyrion.pypp.js_util.decorator import execute_js
from zephyrion.pypp.js_util.js_generator import JsGenerator


class JsActionHandler(JsHandler):
    """
    Javascript Handler for actions on elements.
    """
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


__all__ = ["JsActionHandler"]
