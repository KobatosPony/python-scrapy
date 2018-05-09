# coding:utf-8

from bs4 import BeautifulSoup
from selenium import webdriver
from urllib import request
from urllib.request import *
import time
import ssl
import os

# 定义初始数据
RAW_URL = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&fm=index&pos=history&word='
PIC_LIST = []
SSL = ssl.create_default_context()
HEADER = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
SAVE_PATH = 'save_pic/'
COUNT = 0

# 获取驱动对象
driver = webdriver.PhantomJS()
# driver = webdriver.Chrome()

# 获取用户输入
INPUT_URL = input('input keywords:')

# 获取页面
driver.get(RAW_URL + INPUT_URL)
time.sleep(3)

# 获取所有图片盒子
all_img = driver.find_elements_by_class_name('imgbox')
box_urls = []

# 获取图片盒子链接并处理(放入要获取的数组中)
for src in all_img:
    box_url = src.find_element_by_tag_name('a').get_attribute('href')
    box_urls.append(box_url)

# 获取图片链接
for url in box_urls:
    driver.get(url)
    img_url = driver.find_element_by_id('currentImg').get_attribute('src')
    PIC_LIST.append(img_url)

time.sleep(3)

# 通过urllib进行下载
count = 1
for img_url in PIC_LIST:
    print(img_url)
    req = Request(url=img_url,headers=HEADER)
    img_data = request.urlopen(req,context=SSL).read()
    with open(SAVE_PATH+INPUT_URL+str(count)+'.jpg','wb') as f:
        f.write(img_data)
        print('save suc ...')
    count += 1

driver.quit()