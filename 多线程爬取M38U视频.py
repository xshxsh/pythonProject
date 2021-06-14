import os
import threading
import requests
import re
from concurrent.futures import ThreadPoolExecutor
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
    reg = re.compile(r'url: \'(?P<m3u8_url>.*?)\',', re.S)
    m3u8_url = reg.search(resp.text).group('m3u8_url')

    # 下载m3u8文件
    m3u8_resp = requests.get(m3u8_url, headers=headers)
    m3u8_resp.encoding = 'utf-8'
    with open('file/孤星第二季01.m3u8', mode='wb') as f:
        f.write(m3u8_resp.content)
    m3u8_resp.close()
    resp.close()

    print('下载m3u8文件完成')


# 解析m3u8文件
def parse_m3u8():
    tasks = []
    with open('file/孤星第二季01.m3u8', mode='r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line.startswith('#'):
                continue
            # 测试，只下载几个
            # if i == 20:
            #     break
            tasks.append((line.split('/')[-1], line))
    # 开启10个线程同时下载
    with ThreadPoolExecutor(10) as t:
        for item in tasks:
            t.submit(download_video, item[0], item[1])


# 下载视频片段
def download_video(name, url):
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    with open(f'file/{name}.ts', mode='wb') as f:
        f.write(resp.content)
        print(f'当前线程：{threading.currentThread().name}，下载完{name}.ts')


# 合并视频
def merge_ts():
    lst = []
    with open('file/孤星第二季01.m3u8', mode='r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line.startswith('#'):
                continue
            lst.append(line.split('/')[-1] + '.ts+')
    s = ''.join(lst).rstrip('+')
    # print(s)
    #  执行合并命令：copy /b 1.ts 2.ts 3.ts a.mp4
    # TODO 命令行长度限制，会报错
    os.system(f'copy /b {s} a.mp4')


if __name__ == '__main__':
    # download_m3u8()
    # t1 = time.time()
    # parse_m3u8()
    # print('耗时', time.time() - t1)
    merge_ts()
    print('over')
