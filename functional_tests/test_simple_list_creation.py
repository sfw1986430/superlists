#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_for_one_uesr(self):
        # 用户听说有一个很酷的在线待办事项应用
        # 她在浏览器输入网址
        self.browser.get(self.live_server_url)

        # 网页的标题和头部都包含“To-Do”这个词
        # unittest 提供了很多这种用于编写测试断言的辅助函数，如assertEqual、assertTrue 和assertFalse 等。更多断言辅助函数参见unittest 的文档
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        # 应用邀请她输入一个待办事项
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 她在一个文本框中输入了“Buy peacock feathers”（购买孔雀羽毛）
        inputbox.send_keys('Buy peacock feathers')
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        # 她按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
        # 伊迪丝做事很有条理
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这两个待办事项
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 伊迪丝想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能
        # 她访问那个URL，发现她的待办事项列表还在
        # 她很满意，去睡觉了

    # 进行多用户测试
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 伊迪丝开始新添加List
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 测试是否为用户分配独立的URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 新用户francis访问网站，页面中无法看到伊迪丝的清单
        self.browser.quit()
        self.browser = webdriver.Chrome('C:\programeRun\chromedriver.exe')
        # self.browser = webdriver.Firefox()
        # francis访问主页，无伊迪丝之前保存的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # francis新建一个list，添加相关清单
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # 测试francis是否保存自己的URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 再次检测页面内容
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

