
import requests
import re

# 获取电影天堂2021必看精品的电影下载链接
domain = 'https://www.dytt8.net/index.htm'
resp = requests.get(domain)  # 如果遇到https拦截，可以加verify=False去掉安全验证
resp.encoding = 'gb2312'
# print(resp.text)
obj = re.compile(r'.*?最新电影下载</a>]<a href=\'(?P<link>.*?)\'>(?P<name>.*?)</a><br/>.*?', re.S)
result = obj.finditer(resp.text)
childHrefList = []
for it in result:
    # print(it.group('link'), it.group('name'))
    # 提取子页面链接
    childHref = domain[0:-10] + it.group('link')
    childHrefList.append(childHref)

# 提取子页面内容
reg = re.compile(r'<title>(?P<tittle>.*?)</title>'
                 r'.*?<a target="_blank" href="(?P<downUrl>.*?)"><strong>.*?', re.S)
for href in childHrefList:
    content = requests.get(href)
    content.encoding = 'gb2312'
    urlList = reg.finditer(content.text)
    for url in urlList:
        print(url.group('tittle'), url.group('downUrl'))

