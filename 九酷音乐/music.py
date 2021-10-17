import requests, re, os
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

# 根据歌名在www.9ku.com下载音乐

allMusic = []
allMusicGroup = []


def main():
    # name = input('请输入你要下载的歌曲名称：')
    with open('musicName.txt', encoding='utf-8') as file:
        allMusic = file.read().splitlines()

    # 每100首歌拆分为一个数组
    allMusicGroup = list_split(allMusic, 100)

    # 开启10个线程同时下载
    with ThreadPoolExecutor(10) as t:
        for num in range(len(allMusicGroup)):
            t.submit(download, allMusicGroup[num])


def download(musicList):
    for music in musicList:
        name = urllib.parse.quote(music)
        url = f"https://baidu.9ku.com/song/?key={name}"
        headers = {
            'Referer': 'https://www.9ku.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }
        rep1 = requests.get(url=url, headers=headers).text

        try:
            dowm_url = 'https:' + re.search(r'<a target="_blank" href="(?P<d_url>.*?)" class="down">下载</a>',
                                            rep1).group('d_url')
            rep2 = requests.get(url=dowm_url, headers=headers).text
            tag_music = re.search(r'<a href="(?P<d2_url>.*?)" style="display:none">(?P<mus_name>.*?)Mp3下载</a>', rep2)
            music_url = tag_music.group('d2_url')
            music_name = tag_music.group('mus_name')
            # print(music_url, music_name)
            if not os.path.exists('music'):
                os.mkdir('music')
            path = 'music/' + music_name + ".mp3"
            resp = requests.get(url=music_url, headers=headers).content
            with open(path, "wb") as f:
                f.write(resp)
                print(music_name, "下载完成")
        except Exception:
            print('发生异常')
            pass
        continue

    print('全部下载完成！')


# 把列表拆分为n个元素的多个列表
def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


if __name__ == '__main__':
    main()
