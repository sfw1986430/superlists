#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.is-invalid')

    def test_cannot_add_empty_list_items(self):
        # 伊迪丝访问首页，不小心提交了一个空待办事项
        # 输入框中没输入内容，她就按下了回车键
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 首页刷新了，显示一个错误消息
        # 提示待办事项不能为空
        self.wait_for(lambda :self.browser.find_element_by_css_selector('#id_text:invalid'))

        # 她输入一些文字，然后再次提交，这次没问题了
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda :self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        # 她有点儿调皮，又提交了一个空待办事项
        self.get_item_input_box().send_keys(Keys.ENTER)
        # 在清单页面她看到了一个类似的错误消息
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))
        # 输入文字之后就没问题了
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy beef')

        # 重复输入相同项
        self.get_item_input_box().send_keys('Buy beef')
        self.get_item_input_box().send_keys(Keys.ENTER)

        #得到错误信息
        self.wait_for(lambda :self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))