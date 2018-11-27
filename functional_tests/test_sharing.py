#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListPage

def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class SharingTest(FunctionalTest):
    def test_can_share_a_list_with_another_user(self):
        # 伊迪丝是已登录用户
        self.create_pre_authenticated_session('edith@example.com')
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # 她的朋友Oniciferous也在使用这个清单网站
        oni_browser = webdriver.Chrome('C:\programeRun\chromedriver.exe')
        self.browser.get(self.live_server_url)
        self.addCleanup(lambda :quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oniciferous@example.com')

        # 伊迪丝访问首页，新建一个清单
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )
        # 她分享自己的清单之后，页面更新了
        # 提示已经分享给Oniciferous
        list_page.share_list_with('oniciferous@example.com')
        # 现在Oniciferous在他的浏览器中访问清单页面
        self.browser = oni_browser
        MyListPage(self).go_to_my_lists_page()
        # 他看到了伊迪丝分享的清单
        self.browser.find_element_by_link_text('Get help').click()

        # 在清单页面，Oniciferous看到这个清单属于伊迪丝
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'edith@example.com'
        ))
        # 他在这个清单中添加一个待办事项
        list_page.add_list_item('Hi 伊迪丝!')
        # 伊迪丝刷新页面后，看到Oniciferous添加的内容
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)


        
        
        
        
        
        
        
        

