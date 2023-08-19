import logging

import asynctest

from test.test_utils.page_utils import prepare_page
from zephyrion.pypp import Debugger
from zephyrion.pypp import PageInteractor


class TestPageInteractor(asynctest.TestCase):
    async def setUp(self):
        page, browser = await prepare_page(headless=False)  # 打开 google.com
        self.browser = browser
        self.page_interactor = PageInteractor(page, debug_tool=Debugger(level=logging.DEBUG))
        self.input_selector = "body > center > form > table > tbody > tr > td:nth-child(2) > div > input"
        self.search_click_selector = "body > center > form > table > tbody > tr > td:nth-child(2) > span:nth-child(7) > span > input"
        self.lucky_click_selector = "#tsuid_1"  # <input class="lsb" id="tsuid_1" value="&nbsp;手气不错&nbsp;" name="btnI" type="submit">
        self.close_pop_up_selector = "#yDmH0d > c-wiz > div > div > c-wiz > div > div > div > div.DRc6kd.bdn4dc > div.QlyBfb > button"
        try:
            iframe_handle = await page.querySelector('iframe[name="callout"]')
            iframe = await iframe_handle.contentFrame()

            # 在iframe中查找和交互元素
            close_button = await iframe.querySelector(
                '#yDmH0d > c-wiz > div > div > c-wiz > div > div > div > div.DRc6kd.bdn4dc > div.QlyBfb > button')
            await close_button.click()
        except:
            print("No pop-up, everything is fine!")
            pass

    async def tearDown(self) -> None:
        await self.browser.close_browser()

    async def test_exec_js(self):
        result = await self.page_interactor.exec_js("5 + 5")
        self.assertEqual(result, 10)

    async def test_click(self):
        await self.page_interactor.click(self.lucky_click_selector, new_page=True)
        current_url = self.page_interactor.url
        self.assertNotEqual(current_url, "https://www.google.com/")  # 一旦点击搜索按钮，URL应该发生变化

    async def test_type_input(self):
        test_text = "OpenAI"
        await self.page_interactor.type_input(self.input_selector, test_text)
        value = await self.page_interactor._page.Jeval(self.input_selector, "input => input.value")
        self.assertEqual(value, test_text)
