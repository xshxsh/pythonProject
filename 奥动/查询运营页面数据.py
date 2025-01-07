import requests
import pandas as pd
from tqdm import tqdm
import time

def fetch_driver_data():
    url = 'https://apioperation.aulton.com/account/api/v1.0/customer/listDriverPage/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ru;q=0.7',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://operation.aulton.com',
        'Referer': 'https://operation.aulton.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'token': '554c3a391b7248d2bf6011c50dd61a05'
    }

    # 首先获取总数据量
    initial_payload = {
        "pageSize": 500,
        "pageIndex": 1,
        "registerCityId": 257
    }
    
    response = requests.post(url, headers=headers, json=initial_payload)
    if not response.ok:
        print(f"Error fetching initial data: {response.status_code}")
        return None
    
    total_data = response.json()
    if 'total' not in total_data:
        print("Invalid response format")
        return None
    
    total_records = total_data['total']
    page_size = 500  # 增加每页数量以提高效率
    total_pages = (total_records + page_size - 1) // page_size
    
    print(f"Total records: {total_records}")
    print(f"Total pages: {total_pages}")
    
    all_data = []
    
    # 使用tqdm显示进度
    for page in tqdm(range(1, total_pages + 1), desc="Fetching data"):
        payload = {
            "pageSize": page_size,
            "pageIndex": page,
            "registerCityId": 257
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.ok:
                page_data = response.json()
                if 'data' in page_data:
                    all_data.extend(page_data['data'])
            else:
                print(f"Error on page {page}: {response.status_code}")
            
            # 添加短暂延迟避免请求过快
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error fetching page {page}: {str(e)}")
    
    if all_data:
        # 转换为DataFrame
        df = pd.DataFrame(all_data)
        
        # 导出到Excel
        output_file = 'driver_data.xlsx'
        df.to_excel(output_file, index=False)
        print(f"\nData exported to {output_file}")
        print(f"Total records exported: {len(all_data)}")
    else:
        print("No data was collected")

if __name__ == "__main__":
    fetch_driver_data()
