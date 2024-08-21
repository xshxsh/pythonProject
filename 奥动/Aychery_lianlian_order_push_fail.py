from time import sleep

import requests
import openpyxl

url = "https://archery.aulton.com/query/"

# 修改SQL
payload = "instance_name=abs_message&db_name=abs_message&schema_name=&tb_name=lianlian_order_push_fail&sql_content=select+*+from+lianlian_order_push_fail+where+create_time+%3E'2024-06-01'+and+create_time+%3C'2024-06-16'+and+message%3D'ChargingCompartmentID%E4%B8%8D%E5%85%81%E8%AE%B8%E4%B8%BA%E7%A9%BA'+limit+page%2C1000&limit_num=1000"

headers = {
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
    'sec-ch-ua-platform': '"macOS"',
    # 修改这2个
    'X-CSRFToken': '0iIOl0sb1UFqde23VkrOEuPL9pzAgCGS',
    'Cookie': '_ga=GA1.2.2134789236.1724124534; _gid=GA1.2.743330497.1724124534; csrftoken=0iIOl0sb1UFqde23VkrOEuPL9pzAgCGS; sessionid=uo1axxolqjeq7lmtabvi8yyhzwibvdva; sessionid=uo1axxolqjeq7lmtabvi8yyhzwibvdva'
}

# 所有数据
data_rows = []
limit = 0
result_row = 1000
while (result_row >= 1000):
    # data = payload.format(name="page", place=str(limit))
    data = payload.replace("page", str(limit))
    response = requests.request("POST", url, headers=headers, data=data).json()
    res = response['data']['rows']
    data_rows.extend(res)
    result_row = len(res)
    limit = limit + 1
    sleep(3)
    # print(response.text)

# 创建一个新的Excel工作簿
wb = openpyxl.Workbook()
ws = wb.active

for row_idx, row_data in enumerate(data_rows, start=1):
    for col_idx, value in enumerate(row_data, start=1):
        cell_value = value if value is not None else ""
        ws.cell(row=row_idx, column=col_idx, value=cell_value)

wb.save('导出结果.xlsx')
print("导出完成")
