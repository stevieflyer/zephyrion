import asynctest
import pyppeteer.page

from test.test_utils.page_utils import prepare_page
from zephyrion.browser_agent.pypp_agent.js_util.handler import JsAttrHandler
from zephyrion.browser_agent.pypp_agent.page_interactor import PageInteractor
from zephyrion.browser_agent.pypp_agent.browser_manager import SinglePageBrowser


class TestJsAttrHandler(asynctest.TestCase):
    async def setUp(self):
        result = await prepare_page()
        self.page: pyppeteer.page.Page = result[0]
        self.browser: SinglePageBrowser = result[1]
        self.page_interactor = PageInteractor(self.page)
        self.test_input_selector = "body > center > form > table > tbody > tr > td:nth-child(2) > div > input"  # 示例选择器
        self.test_click_selector = "body > center > form > table > tbody > tr > td:nth-child(2) > span:nth-child(7) > span > input"  # 示例选择器

    async def tearDown(self):
        await self.browser.close_browser()

    async def test_js_attr_handler_get_attr(self):
        handler = JsAttrHandler(js_executor=self.page_interactor)
        attr = "value"
        value = await handler.get_attr(selector=self.test_click_selector, attr=attr)
        self.assertIn("Google", value)  # 确保值中包含"Google"

    async def test_js_attr_handler_set_attr(self):
        handler = JsAttrHandler(js_executor=self.page_interactor)
        attr = "value"
        new_value = "New Value for Testing"
        await handler.set_attr(selector=self.test_click_selector, attr=attr, value=new_value)
        retrieved_value = await handler.get_attr(selector=self.test_click_selector, attr=attr)
        self.assertEqual(retrieved_value, new_value)
