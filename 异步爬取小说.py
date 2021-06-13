import asyncio
import aiohttp
import aiofiles
import requests
from lxml import etree
from bs4 import BeautifulSoup

domain = 'https://www.xyyuedu.com'


# 获取小说目录
async def get_catalogue():
    resp = requests.get(f'{domain}/gdmz/sidamingzhu/xyji/')
    resp.encoding = 'gbk'
    # print(resp.text)
    # 获取目录连接
    tags = BeautifulSoup(resp.text, 'html.parser')
    hrefs = tags.find('ul', class_='zhangjie2').find_all('a')
    # print(hrefs)
    tasks = []
    for i, item in enumerate(hrefs):
        # 下载10章
        if i == 10:
            break
        title = item.get('title')
        url = domain + item.get('href')
        # print(url)
        tasks.append(asyncio.create_task(get_content(title, url)))
    await asyncio.wait(tasks)


# 异步下载小说
async def get_content(title, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            # print(await resp.text(encoding='gbk'))
            content = etree.HTML(await resp.text(encoding='gbk')).xpath('//div[@id="onearcxsbd"]/text()')
            # print(content)
            async with aiofiles.open(f'file/{title}.txt', mode='a', encoding='utf-8') as f:
                # async with aiofiles.open(f'file/西游记.txt', mode='w', encoding='utf-8') as f:
                # 把list转string后写入文件
                await f.write(''.join(content))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_catalogue())
    # asyncio.run(get_catalogue())
    print('over')
