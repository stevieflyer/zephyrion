import pyppeteer.page
from zephyrion.browser_agent.pypp.browser_manager import SinglePageBrowser


async def prepare_page(headless=False) -> (pyppeteer.page.Page, SinglePageBrowser):
    """
    Prepare a `pyppeteer.page.Page` object and a `SinglePageBrowser` for testing.

    :return: (page: `pyppeteer.page.Page`, browser: `SinglePageBrowser`)
    """
    test_url = "https://www.google.com/"
    browser = SinglePageBrowser(headless=headless)
    await browser.start_browser()
    await browser.go(test_url)
    page = await browser.get_page()
    return page, browser
