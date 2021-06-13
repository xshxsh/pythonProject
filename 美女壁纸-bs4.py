import requests
from bs4 import BeautifulSoup
import time

# 爬取美女壁纸

url = 'https://pic.netbian.com/4kmeinv/'
resp = requests.get(url)
resp.encoding = 'gbk'
tags = BeautifulSoup(resp.text, 'html.parser')
imgs = tags.find('ul', class_='clearfix').find_all('img')
for img in imgs:
    imgUrl = url[0:-9] + img.get('src')
    # print(imgUrl)
    imgDown = requests.get(imgUrl)
    imgDown.encoding = 'gbk'
    with open('file/' + img.get('alt') + '.jpg', mode='wb') as file:
        file.write(imgDown.content)
    print('下载完成：', img.get('alt'))
    # time.sleep(1)
