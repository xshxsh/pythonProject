import requests, re, os
import urllib.parse


def main():
    name = input('请输入你要下载的歌曲名称：')
    name1 = urllib.parse.quote(name)
    url = f"https://baidu.9ku.com/song/?key={name1}"
    headers = {
        'Referer': 'https://www.9ku.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    rep1 = requests.get(url=url, headers=headers).text
    dowm_url = 'https:' + re.search(r'<a target="_blank" href="(?P<d_url>.*?)" class="down">下载</a>', rep1).group(
        'd_url')
    rep2 = requests.get(url=dowm_url, headers=headers).text
    tag_music = re.search(r'<a href="(?P<d2_url>.*?)" style="display:none">(?P<mus_name>.*?)Mp3下载</a>', rep2)
    music_url = tag_music.group('d2_url')
    music_name = tag_music.group('mus_name')
    print(music_url, music_name)
    if not os.path.exists('music'):
        os.mkdir('music')
    path = 'music/' + music_name + ".mp3"
    resp = requests.get(url=music_url, headers=headers).content
    with open(path, "wb") as f:
        f.write(resp)
        print(music_name, "下载完成")


if __name__ == '__main__':
    main()