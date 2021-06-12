import requests

# 爬取视频，解决防盗链问题
"""
某些视频网站，为了防盗链，会把视频地址中的某部分换成固定的字符串
只要替换回来，就能正常访问
"""

# 网站地址
url = 'https://www.pearvideo.com/video_1732044'
contId = url.split('_')[1]
# 视频地址
videoUrl = f'https://www.pearvideo.com/videoStatus.jsp?contId={contId}&mrd=0.2776271598332598'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    # 防盗链
    'Referer': url
}
resp = requests.get(videoUrl, headers=headers)
# print(resp.text)
dic = resp.json()
systemTime = dic['systemTime']
# 替换视频下载地址
video = dic['videoInfo']['videos']['srcUrl'].replace(systemTime, f'cont-{contId}')
# print(vedio)
# 下载视频
with open('file/a.mp4', mode='wb') as f:
    f.write(requests.get(video).content)
