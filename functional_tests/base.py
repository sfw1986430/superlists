#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from .management.commands.create_session import create_pre_authenticated_session
from django.conf import settings
import time
import functools


MAX_WAIT = 10

# 增加装饰器wait
def wait(fn):
    @functools.wraps(fn)
    def modeified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modeified_fn
    
class FunctionalTest(StaticLiveServerTestCase):
    # setUp 和tearDown 是特殊的方法，分别在各个测试方法之前和之后运行。
    def setUp(self):
        self.browser = webdriver.Chrome('C:\programeRun\chromedriver.exe')
        # self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        # print(staging_server)
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            # print(self.live_server_url)

    def tearDown(self):
        self.browser.quit()



    @wait
    def wait_for(self, fn):
        return fn()
    
    # 测试等待时间
    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # 测试登陆 注销
    @wait
    def wait_to_be_logged_in(self,email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    # 使用django的forms类去编表格
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
    
    def create_pre_authenticated_session(self, email):
        session_key = create_pre_authenticated_session(email)

        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


