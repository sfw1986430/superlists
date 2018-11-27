#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
    # 进行简单的前端测试
    def test_layout_and_styling(self):
        # 用户首页测试
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # 测试首页的输入框是否居中
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
