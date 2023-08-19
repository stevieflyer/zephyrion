from functools import wraps

timeout = 5000  # 5 seconds


def wait_for_selector(func):
    @wraps(func)
    async def decorator(self: 'PageInteractor', selector: str, *args, **kwargs):
        await self._page.waitForSelector(selector, timeout=timeout)
        return await func(self, selector, *args, **kwargs)

    return decorator
