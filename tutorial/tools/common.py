# -*- coding: utf-8 -*-
import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

# from selenium import webdriver
# import time
# browser =webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe ")
# browser.get('https://www.douban.com/explore/')
# for i in xrange(5):
#     browser.find_element_by_class_name('a_more').click()
#     time.sleep(4)
# print browser.page_source
# browser.quit()

