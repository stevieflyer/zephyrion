from functools import wraps


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
            self._debug_tool.debug(f"executed js code: {js_code}, result: {result}")
            return result
    return decorator


__all__ = ["execute_js"]
