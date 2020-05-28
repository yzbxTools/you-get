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
from urllib.parse import unquote
from you_get.common import *

class SeleniumTests(unittest.TestCase):
    def test_selenium(self):
        def get_data_imgurl(html):
            soup = BeautifulSoup(html,                      #HTML文档字符串
                             'html.parser',                  #HTML解析器 
                              )
            img_reg='(.*)\.(jpg|bmp|gif|ico|pcx|jpeg|tif|png|raw|tga)'
            links=soup.find_all('img',attrs={'data-imgurl':re.compile(img_reg)})
            #links=soup.find_all('a',class_='down')
            #links=[l for l in links if l.title=='下载原图']
            return links
        
        def get_obj_URL(html):
            links = re.findall('"objURL":"(.*?)",',html,re.S)
            return links
        
        #objurl=http%3A%2F%2Fimg.pconline.com.cn%2Fimages%2Fupload%2Fupc%2Ftx%2Fitbbs%2F1507%2F13%2Fc38%2F9702970_1436774075010.jpg
        def get_objurl(html):
            links=[]
            for ext in ['jpg','bmp','png','jpeg','gif']:
                links+=re.findall('objurl=(http.*?\.%s)&'%ext,html,re.S|re.IGNORECASE)
                links+=re.findall('data-objurl="(http.*?\.%s)"'%ext,html,re.S|re.IGNORECASE)
                
            links=[l for l in links if l.find(' ')==-1]
            return links
        
        def get_links(html):
            return get_objurl(html)
        
        #url="https://pic.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1590513326281_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=%E6%98%9F%E7%A9%BA"
        
        keyword='cat'
        #url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+keyword+'&ct=201326592&v=flip&height=800&width=1280'
        url = 'https://image.baidu.com/search/index?tn=baiduimage&ie=utf-8&word='+keyword+'&ct=201326592&v=flip&height=800&width=1280'
        
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless=True
        
        #This example requires Selenium WebDriver 3.13 or newer
        with webdriver.Firefox(options=fireFoxOptions) as driver:            
            driver.get(url)
            html=driver.page_source
            old_n=len(get_links(html))
            self.assertTrue(old_n>=0)
            for i in range(3):
                webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1)
                html=driver.page_source
                new_n=len(get_links(html))
                self.assertTrue(new_n>=old_n)
                old_n=new_n
                print(new_n,old_n)
            
            links=get_links(html)
            for l in links:
                try:
                    size=url_size(unquote(l))
                except:
                    print('*'*5,l)
                    continue
                else:
                    print(size,l)
                    
            self.assertTrue(len(links)>0)
        
        
if __name__ == '__main__':
    unittest.main()