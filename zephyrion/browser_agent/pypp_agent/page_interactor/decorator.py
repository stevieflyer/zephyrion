from functools import wraps


def wait_for_selector(func):
    @wraps(func)
    async def decorator(self: 'PageInteractor', selector: str, *args, **kwargs):
        await self._page.waitForSelector(selector, timeout=self._config.selector_wait_time_out)
        return await func(self, selector, *args, **kwargs)
    return decorator
