import aiofiles
import requests
import re
import asyncio
import aiohttp
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


# 下载m3u8文件
def download_m3u8():
    # 获取m3u8链接
    url = 'https://www.91kanju.com/vod-play/59608-1-1.html'
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    # print(resp.text)
    reg = re.compile(r'url: \'(?P<m3u8_url>.*?)\',', re.S)
    m3u8_url = reg.search(resp.text).group('m3u8_url')
    # print(m3u8_url)

    # 下载m3u8文件
    m3u8_resp = requests.get(m3u8_url, headers=headers)
    m3u8_resp.encoding = 'utf-8'
    with open('file/孤星第二季01.m3u8', mode='wb') as f:
        f.write(m3u8_resp.content)
    m3u8_resp.close()
    resp.close()

    print('下载m3u8文件完成')


# 解析m3u8文件
async def parse_m3u8():
    tasks = []
    with open('file/孤星第二季01.m3u8', mode='r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line.startswith('#'):
                continue
            # 测试，只下载几个
            # if i == 20:
            #     break
            tasks.append(asyncio.create_task(download_video(line.split('/')[-1], line)))
    await asyncio.wait(tasks)


# 下载视频片段
async def download_video(name, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            async with aiofiles.open(f'file/{name}.ts', mode='wb') as f:
                await f.write(await resp.content.read())
                print(f'下载完{name}.ts')


if __name__ == '__main__':
    download_m3u8()

    t1 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parse_m3u8())

    print('耗时', time.time() - t1)

    print('over')
