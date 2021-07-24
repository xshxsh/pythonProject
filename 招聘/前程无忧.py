# 导入驱动并且定义驱动
from selenium import webdriver
import time, csv

# chromedriver.exe的路径
driver = r'D:\pythonProject\browser_driver\chromedriver.exe'
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
        # 输入职位信息

        # 定义单页处理的动态方法handlepage

    def handlepage(self):

        lists = browser.find_elements_by_xpath('#div[@class="dw_table"]#div[@class="el"]')  # 在所有需要定位的元素上方获取同父元素，筛选范围
        for l in lists:  # 遍历该同类父元素，在此基础上再逐个定位单个元素
            # 使用+号拼接元素
            temp = '职位:' + l.find_element_by_class_name('t1').text + ' ' + \
                   '公司:' + l.find_element_by_class_name('t2').text + ' ' + \
                   '地点:' + l.find_element_by_class_name('t3').text + ' ' + \
                   '薪资:' + l.find_element_by_class_name('t4').text
            print(temp)  # 打印输出

    # 定义处理多个页面的动态方法，需要调用上方的单页处理动态方法
    def handlepages(self):
        # 需要遍历的页面数
        for p in range(0, self.pages):
            self.handlepage()  # 调用单页面动态方法
            browser.find_element_by_id('rtNext').click()  # 点击下一页
            browser.implicitly_wait(10)  # 隐式等待，防止定位元素失败

    # 定义城市选择的动态方法

    def location(self):
        browser.find_element_by_id("work_position_input").click()
        # 点击选择城市的按钮
        time.sleep(1)
        # 固定等待1s
        cities = browser.find_elements_by_xpath(
            '#div[@id="work_position_click_center_right_list_000000"]#td#em')  # 获取城市列表
        # 因为前程无忧会自动定位城市并默认选择，这里没有关闭自动定位设置，直接写代码
        if self.city != '广州':  # 如果需要的城市不是广州
            for locate in cities:  # 遍历所有城市
                if self.city == locate.text:  # 如果定位到需要的城市
                    locate.click()  # 点击选择
                    browser.find_element_by_id(
                        "work_position_click_center_right_list_category_000000_030200").click()  # 去掉默认选择的城市
                    browser.find_element_by_id("work_position_click_bottom_save").click()
                    # 点击确认选择的按钮
                    break  # 跳出该循环
        else:  # 如果需要的城市是自动定位的城市，即取消选择城市
            browser.find_element_by_xpath('#span[@class="p_but gray work_position_click_close"]').click()

    # 定义运行该类的动态方法
    def run(self):
        url = 'https://www.51job.com/'
        # 前程无忧首页链接
        browser.get(url)
        # 进入
        browser.maximize_window()
        # 最大化窗口
        # browser.implicitly_wait(10)
        # 隐式等待防止定位元素失败
        # browser.find_element_by_xpath('#a[@href="https:#search.51job.com"]').click()
        # 点击职位搜索按钮
        browser.implicitly_wait(10)
        # 隐式等待防止定位元素失败
        self.carrier()  # 调用职位输入的动态的方法
        # self.location()  # 调用城市选择的动态的方法
        browser.find_element_by_xpath('.//div[@class="el on"]/button').click()  # 点击搜索
        self.handlepages()  # 直接调用多处理页面动态方法
        browser.quit()  # 关闭浏览器


# 调用该类并运行
QCWYjobs(keyword='java web开发', pages=2, city='广州').run()
