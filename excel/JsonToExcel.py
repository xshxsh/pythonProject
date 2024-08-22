import json
import pandas as pd

if __name__ == '__main__':
    # 读取本地json文件
    with open('aulton-application.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 将json数据转换为DataFrame
    df = pd.DataFrame(data)

    # 将DataFrame写入Excel文件
    df.to_excel('output.xlsx', index=False)

    print("JSON数据已成功转换为Excel文件")
