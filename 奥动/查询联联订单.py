from time import sleep

import requests

# 打开文件并逐行读取内容，存储到列表中
lines = []
with open('order.txt', 'r', encoding='utf-8') as file:
    for line in file:
        lines.append(line.strip())

# 登录archery页面查询后按F12查看修改SQL和token
url = "https://archery.aulton.com/query/"

# 修改SQL，注意最后在&limit_num=1000前加上 +limit+{}%2C1000
payload = "instance_name=abs_order_slave(%E8%AE%A2%E5%8D%95%E4%BB%8E%E5%BA%931)&db_name=abs_order&schema_name=&tb_name=&sql_content=SELECT+*+from+order_swap_details+where+partner_swap_no+%3D+'{}'&limit_num=100"
headers = {
    # 修改X-CSRFToken,Cookie值
    'X-CSRFToken': 'kKlQMnmLqVQsJyDfsqViXJ5JNC20wk7T',
    'Cookie': '_ga=GA1.2.143828957.1732874159; _gid=GA1.2.1530247464.1734315234; csrftoken=kKlQMnmLqVQsJyDfsqViXJ5JNC20wk7T; sessionid=lwtoax2sl1xm9k4htok6tveusro1o9e7',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://archery.aulton.com',
    'Pragma': 'no-cache',
    'Referer': 'https://archery.aulton.com/sqlquery/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

no_order = []
# 打印列表中的每一行
for line in lines:
    data = payload.format(str(line.strip()))
    response = requests.request("POST", url, headers=headers, data=data).json()
    res = response['data']['rows']
    if not res:
        print("列表为空:" + line)
        no_order.append(line.strip())
    # 休眠秒数，根据SQL执行快慢修改参数
    sleep(1)
print(no_order)
