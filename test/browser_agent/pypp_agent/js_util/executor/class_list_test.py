import asynctest
import pyppeteer.page

from test.test_utils.page_utils import prepare_page
from zephyrion.browser_agent.pypp.js_util.handler import JsClassListHandler
from zephyrion.browser_agent.pypp.page_interactor import PageInteractor
from zephyrion.browser_agent.pypp.browser_manager import SinglePageBrowser


class TestJsClassListHandler(asynctest.TestCase):
    async def setUp(self):
        result = await prepare_page()
        self.page: pyppeteer.page.Page = result[0]
        self.browser: SinglePageBrowser = result[1]
        self.page_interactor = PageInteractor(self.page)
        self.test_selector = "body > center > form > table > tbody > tr > td:nth-child(2) > div > input"  # 示例选择器

    async def tearDown(self):
        await self.browser.close_browser()

    async def test_js_class_list_handler_get_class_list(self):
        handler = JsClassListHandler(js_executor=self.page_interactor)
        class_list = await handler.get_class_list(selector=self.test_selector)
        self.assertIsInstance(class_list, list)  # 确保返回结果是一个列表

    async def test_js_class_list_handler_add_class(self):
        handler = JsClassListHandler(js_executor=self.page_interactor)
        test_class = "testClass"
        await handler.add_class(selector=self.test_selector, class_name=test_class)
        class_list = await handler.get_class_list(selector=self.test_selector)
        self.assertIn(test_class, class_list)  # 确保新添加的类存在于列表中

    async def test_js_class_list_handler_remove_class(self):
        handler = JsClassListHandler(js_executor=self.page_interactor)
        test_class = "testClassToRemove"
        await handler.add_class(selector=self.test_selector, class_name=test_class)  # 先添加一个类
        await handler.remove_class(selector=self.test_selector, class_name=test_class)  # 然后移除它
        class_list = await handler.get_class_list(selector=self.test_selector)
        self.assertNotIn(test_class, class_list)  # 确保已移除的类不在列表中

    async def test_js_class_list_handler_toggle_class(self):
        handler = JsClassListHandler(js_executor=self.page_interactor)
        test_class = "testClassToToggle"
        await handler.toggle_class(selector=self.test_selector, class_name=test_class)  # 添加类
        class_list = await handler.get_class_list(selector=self.test_selector)
        self.assertIn(test_class, class_list)  # 确保类已添加

        await handler.toggle_class(selector=self.test_selector, class_name=test_class)  # 再次切换，即移除类
        class_list = await handler.get_class_list(selector=self.test_selector)
        self.assertNotIn(test_class, class_list)  # 确保类已移除
