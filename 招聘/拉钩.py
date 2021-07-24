from selenium import webdriver
import time
import logging
import random
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['job_name', 'company_name', 'city','industry', 'salary', 'experience_edu','welfare','job_label'])
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def search_product(key_word):
    browser.find_element_by_id('cboxClose').click()     # 关闭让你选城市的窗口
    time.sleep(2)
    browser.find_element_by_id('search_input').send_keys(key_word)  # 定位搜索框 输入关键字
    time.sleep(2)
    # browser.find_element_by_class_name('search_button').click()     # 点击搜索
    button = browser.find_element_by_class_name('search_button')
    browser.execute_script("$(arguments[0]).click()", button)
    browser.maximize_window()    # 最大化窗口
    # time.sleep(2)
    # browser.find_element_by_class_name('body-btn').click()    # 关闭弹窗  啥领取红包窗口
    time.sleep(random.randint(1, 3))
    browser.execute_script("scroll(0,3000)")      # 下拉滚动条
    get_data()           # 调用抓取数据的函数
    # 模拟点击下一页   翻页爬取数据  每爬取一页数据  休眠   控制抓取速度  防止被反爬 让输验证码
    # 超过10页要登录...
    for i in range(9):
        browser.find_element_by_class_name('pager_next ').click()
        time.sleep(1)
        browser.execute_script("scroll(0,3000)")
        get_data()
        time.sleep(random.randint(3, 5))


def get_data():
    items = browser.find_elements_by_xpath('//*[@id="s_position_list"]/ul/li')
    for item in items:
        job_name = item.find_element_by_xpath('.//div[@class="p_top"]/a/h3').text
        company_name = item.find_element_by_xpath('.//div[@class="company_name"]').text
        city = item.find_element_by_xpath('.//div[@class="p_top"]/a/span[@class="add"]/em').text
        industry = item.find_element_by_xpath('.//div[@class="industry"]').text
        salary = item.find_element_by_xpath('.//span[@class="money"]').text
        experience_edu = item.find_element_by_xpath('.//div[@class="p_bot"]/div[@class="li_b_l"]').text
        welfare = item.find_element_by_xpath('.//div[@class="li_b_r"]').text
        job_label = item.find_element_by_xpath('.//div[@class="list_item_bot"]/div[@class="li_b_l"]').text
        data = f'{job_name},{company_name},{city},{industry},{salary},{experience_edu},{welfare},{job_label}'
        logging.info(data)
        sheet.append([job_name, company_name, city,industry, salary, experience_edu, welfare, job_label])


def main():
    browser.get('https://www.lagou.com/')
    time.sleep(random.randint(1, 3))
    search_product(keyword)
    wb.save('job_info.xlsx')


if __name__ == '__main__':
    keyword = 'Python 数据分析'
    # chromedriver.exe的路径
    chrome_driver = r'D:\pythonProject\browser_driver\chromedriver.exe'
    options = webdriver.ChromeOptions()
    # 关闭左上方 Chrome 正受到自动测试软件的控制的提示
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    browser = webdriver.Chrome(options=options, executable_path=chrome_driver)
    main()
    browser.quit()