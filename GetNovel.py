import requests
from bs4 import BeautifulSoup
import re


# 确定待抓取的url
url = 'https://www.biqiuge.com/book/4772/'

# 网页请求
response = requests.get(url)
response.encoding = response.apparent_encoding


# 解析 用select没有下标 用find all有下标
soup = BeautifulSoup(response.text, 'lxml')
title = soup.find('h2').get_text()
acontent = soup.select('.listmain')[0]
chapter_info_list = acontent.find_all("a")

# 新建文件

fb = open('G:\Workspace\VSCode\Python\scarynovel\%s.txt' % title, 'w', encoding='utf-8')

# 循环每章节去下载
for chapter_info in enumerate(chapter_info_list):
    if chapter_info[0] > 5:
        chapter_url = chapter_info[1].get("href")
        chapter_title = chapter_info[1].get_text()
        chapter_url = "https://www.biqiuge.com%s" % chapter_url
        print(chapter_url, chapter_title)
        # 下载章节的内容
        chapter_reponse = requests.get(chapter_url)
        chapter_reponse.encoding = response.apparent_encoding
        soup_content = BeautifulSoup(chapter_reponse.text, 'lxml')
        chapter_content = soup_content.find('div', id = 'content').get_text()
        # 按照指定格式替换章节内容，运用正则表达式  先找到匹配所有空格的地方 替换  导入文本 strip 剥夺文本格式
        # re.sub 将字符串3所有pat1匹配项用repl2代替 \d是匹配数字字符[0-9]，+匹配一个或多个
        # 放在一起是匹配一个或多个数字字符，比如：’1‘、’34‘、’9999‘
        chapter_content = re.sub('\s+', '\r\n\t', chapter_content).strip('\r\n')
        print(chapter_content)
        fb.write(chapter_title)
        fb.write('\n')
        fb.write(chapter_content)
        fb.write('\n')


