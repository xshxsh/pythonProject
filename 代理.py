import requests

'''
如果频繁访问某个网站，会被网站封IP，可以通过替换不同的IP进行代理访问
先去找到一个可以免费获取代理IP的网址，比如:https://www.zdaye.com/FreeIPList.html
可以爬取里面可以用的代理IP用作转发
'''

# 代理地址
proxies = {
    'http': 'https://119.3.235.101:3128',
    'http': 'https:113.100.209.113:3128'
}

resp = requests.get('https://www.baidu.com/', proxies=proxies)
resp.encoding = 'utf-8'
print(resp.text)
