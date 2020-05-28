# -*- coding: utf-8 -*-

import unittest
from bs4 import BeautifulSoup
from urllib import parse,request
import re
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

class SeleniumTests(unittest.TestCase):
    def test_selenium(self):
        def get_links(html):
            soup = BeautifulSoup(html,                      #HTML文档字符串
                             'html.parser',                  #HTML解析器 
                              )
            img_reg='(.*)\.(jpg|bmp|gif|ico|pcx|jpeg|tif|png|raw|tga)'
            links=soup.find_all('img',attrs={'data-imgurl':re.compile(img_reg)})
            #links=soup.find_all('a',class_='down')
            #links=[l for l in links if l.title=='下载原图']
            return links
        
        def get_obj_links(html):
            links = re.findall('"objURL":"(.*?)",',html,re.S)
            return links
        
        url="https://pic.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1590513326281_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E6%98%9F%E7%A9%BA"
        
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless=True
        
        #This example requires Selenium WebDriver 3.13 or newer
        with webdriver.Firefox(options=fireFoxOptions) as driver:
            #driver.get("https://pic.baidu.com")
            #obj=driver.find_element(By.CSS_SELECTOR, "#kw")
            #obj.send_keys("露珠" + Keys.RETURN)
            
            driver.get(url)
            html=driver.page_source
            old_n=len(get_links(html))
            self.assertTrue(old_n>=0)
            for i in range(5):
                webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)
                html=driver.page_source
                new_n=len(get_links(html))
                self.assertTrue(new_n>=old_n)
                old_n=new_n
                print(new_n,old_n)
            
            print(html)
        # start web browser
        browser=webdriver.Firefox(options=fireFoxOptions)
        
        # get source code
        
        browser.get(url)
        html = browser.page_source
        self.assertTrue(html.find('data-imgurl')>=0)
        
        # close web browser
        browser.close()
        links=get_links(html)
        print(len(links))
        self.assertTrue(len(links)>0)
        
        
if __name__ == '__main__':
    unittest.main()