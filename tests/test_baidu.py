import unittest
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

class BaiduTests(unittest.TestCase):
    def test_baidu(self):
        def get_original_image(html):
            soup = BeautifulSoup(html,                      #HTML文档字符串
                                 'html.parser',                  #HTML解析器 
                                  )
            img_reg='(.*)\.(jpg|bmp|gif|ico|pcx|jpeg|tif|png|raw|tga)'
            links=soup.find_all('a',class_='down')
            return links
    
        keyword='cat'
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+keyword+'&ct=201326592&v=flip&height=800&width=1280'
        result = requests.get(url)
        html = result.text
        print(html)
        #links=get_original_image(html)
        #pic_url=['https://image.baidu.com/'+l.href for l in links]
        pic_url = re.findall('"objURL":"(.*?)",',html,re.S)
        i = 0
        
        self.assertTrue(len(pic_url)>5)
        for each in pic_url:
            print(pic_url)
        
            try:
                pic= requests.get(each, timeout=10)
            except requests.exceptions.ConnectionError:
                print ('exception')
                continue
    
            string = 'pictures'+keyword+'_'+str(i) + '.jpg'
            fp = open(string,'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
            
        self.assertTrue(i>0)
        
if __name__ == '__main__':
    unittest.main()