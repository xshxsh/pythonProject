
import re
import requests
import csv

# 爬取豆瓣电影tpo250

url = 'https://movie.douban.com/top250'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}
# 爬取数据
resp = requests.get(url=url, headers=headers)
# print(resp.text)
resp.close()

# 解析数据
obj = re.compile(
    r'<a href="(?P<detail>.*?)">.*?'
    r'<img width=".*?" alt="(?P<name>.*?)" src="(?P<imageUrl>.*?)" class="">.*?'
    r'<p class="">.*?<br>.*?(?P<year>\d+)&nbsp;.*?'
    r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
    r'<span>(?P<number>\d+)人评价</span>.*?'
    , re.S
)
result = obj.finditer(resp.text)
file = open('movie.csv', mode='w',encoding='utf-8')
csvWriter = csv.writer(file)
for it in result:
    print(it.group('name'),
          it.group('year'),
          it.group('score'),
          it.group('number'),
          it.group('detail'))
    dic = it.groupdict()
    csvWriter.writerow(dic.values())
file.close()