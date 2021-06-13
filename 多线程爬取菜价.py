from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
import csv

# def fun(name):
#     for i in range(100):
#         print(name, i)
#
#
# if '__main__' == __name__:
#     # 创建线程池
#     with ThreadPoolExecutor(10) as t:
#         # 启动50个任务
#         for i in range(50):
#             t.submit(fun, name=f'{i}')
#     print('over')

# 多线程爬取北京新发地市场菜价，保存到CSV文件
f = open('file/vegetable_prices.scv', mode='w', newline='', encoding='utf-8')
csvWriter = csv.writer(f)


# 下载单个页面的菜价
def downLoad_one_page(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    # print(resp.text)
    html = etree.HTML(resp.text)
    # 获取表格内容，去掉表头
    table = html.xpath('/html/body/div[2]/div[4]/div[1]/table/tr')[1:]
    # print(len(table))
    for tr in table:
        txt = tr.xpath('./td/text()')
        # 去掉掉菜价的\\ /
        content = (item.replace('\\', '').replace('/', '') for item in txt)
        # print(list(content))
        csvWriter.writerow(content)
    print('保存菜价完毕')


if '__main__' == __name__:
    # 开启50个线程同时下载
    with ThreadPoolExecutor(50) as t:
        # 下载100页的数据
        for i in range(1, 100):
            t.submit(downLoad_one_page, f'http://xinfadi.com.cn/marketanalysis/0/list/{i}.shtml')
    f.close()