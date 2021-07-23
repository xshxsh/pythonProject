import requests
from lxml import etree

# 使用xpath爬取猪八戒网的信息
url = 'https://guangzhou.zbj.com/wzkf/f.html?fr=zbj.sy.zyyw_2nd.lv2'
resp = requests.get(url)
resp.encoding = 'utf-8'
print(resp.text)

html = etree.HTML(resp.text)
print(html.xpath('//*[@id="utopia_widget_68"]/a[1]/div[2]/div[2]/p/text()'))