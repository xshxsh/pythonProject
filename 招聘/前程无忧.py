# 导入驱动并且定义驱动
import random
import openpyxl
from selenium import webdriver
import time

# 保存到excel
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(['job_name', 'company', 'salary', 'job_desc', 'company_desc', 'industry', 'release_time'])

# chromedriver.exe的路径
driver = r'F:\Code\crawler\browser_driver\driver.exe'
options = webdriver.ChromeOptions()
# 关闭左上方 Chrome 正受到自动测试软件的控制的提示
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(options=options, executable_path=driver)


# 定义该类
class QCWYjobs:
    def __init__(self, keyword, pages, city):
        # 定义静态方法，其中需要属于三个参数，分别是职位信息、爬取的页数、城市
        self.keyword = keyword
        self.pages = pages
        self.city = city

    # 定义职位输入方法 carrier
    def carrier(self):
        browser.find_element_by_id('kwdselectid').send_keys(self.keyword)

    # 处理单个页面
    def handlepage(self):
        # 遍历该同类父元素，在此基础上再逐个定位单个元素
        lists = browser.find_elements_by_xpath('.//div[@class="j_joblist"]/div[@class="e"]')
        for context in lists:
            # 岗位信息
            job_div = context.find_element_by_class_name('el')
            # 公司信息
            company_div = context.find_element_by_class_name('er')
            # 获取岗位信息
            job_name = job_div.find_element_by_class_name('t').find_element_by_class_name('jname.at').text
            company = company_div.find_element_by_class_name('cname.at').text
            salary = job_div.find_element_by_class_name('info').find_element_by_class_name('sal').text
            job_desc = job_div.find_element_by_class_name('info').find_element_by_class_name('d.at').text
            company_desc = company_div.find_element_by_class_name('dc.at').text
            industry = company_div.find_element_by_class_name('int.at').text
            release_time = job_div.find_element_by_class_name('t').find_element_by_class_name('time').text
            # welfare = job_div.find_element_by_class_name('tags').text
            data = f'{job_name},{company},{salary},{job_desc},{company_desc},{industry},{release_time}'
            # print(data)
            sheet.append([job_name, company, salary, job_desc, company_desc, industry, release_time])

    # 定义处理多个页面的动态方法，需要调用上方的单页处理动态方法
    def handlepages(self):
        # 需要遍历的页面数
        for p in range(0, self.pages):
            print(f'嘘，不要声张，我正在偷偷地爬取第{p+1}页数据...')
            self.handlepage()  # 调用单页面动态方法
            browser.find_element_by_class_name('e_icons.i_next').click()  # 点击下一页
            browser.implicitly_wait(10)  # 隐式等待，防止定位元素失败
            time.sleep(random.randint(1, 3))

    # 定义城市选择的动态方法
    def location(self):
        # 点击选择城市的按钮
        browser.find_element_by_id("work_position_input").click()
        time.sleep(1)
        # 获取城市列表
        cities = browser.find_elements_by_xpath(
            './/div[@id="work_position_click_center_right_list_000000"]/table/tbody/tr/td/em')
        # 遍历所有城市
        for locate in cities:
            # 如果定位到需要的城市
            if self.city == locate.text:
                # 点击选择
                locate.click()
                time.sleep(1)
                # 关闭城市选择窗口
                browser.find_element_by_id("work_position_click_bottom_save").click()

    # 定义运行该类的动态方法
    def run(self):
        url = 'https://www.51job.com/'
        # 前程无忧首页链接
        browser.get(url)
        # 进入
        # browser.maximize_window()
        # 最大化窗口
        # browser.implicitly_wait(10)
        # 隐式等待防止定位元素失败
        # browser.find_element_by_xpath('#a[@href="https:#search.51job.com"]').click()
        # 点击职位搜索按钮
        browser.implicitly_wait(10)
        # 隐式等待防止定位元素失败
        self.carrier()  # 调用职位输入的动态的方法
        self.location()  # 调用城市选择的动态的方法
        browser.find_element_by_xpath('.//div[@class="ush top_wrap"]/button').click()  # 点击搜索
        self.handlepages()  # 直接调用多处理页面动态方法
        browser.quit()  # 关闭浏览器
        wb.save('job_info.xlsx')


# 调用该类并运行
QCWYjobs(keyword='java web开发', pages=2, city='广州').run()
