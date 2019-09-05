from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq
import time
 
 
class ZhiLian:
    def __init__(self):
        # 设置 chrome 无界面化模式
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
 
    def get_url(self, search='python'):
        """
        获取搜索职位的url, demo里面默认搜索python
        :param search:
        :return:
        """
        self.driver.get("https://www.zhaopin.com/")
        element = self.driver.find_element_by_class_name("zp-search__input")
        element.send_keys(f"{search}")
        element.send_keys(Keys.ENTER)
        # 切换窗口
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 等待js渲染完成后，在获取html
        time.sleep(4)
        html = self.driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        return html
 
    def data_processing(self):
        """
        处理数据
        :return:
        """
        html = self.get_url()
        doc = pq(html)
        contents = doc(".contentpile__content__wrapper")
        for content in contents.items():
            jobname = content(".contentpile__content__wrapper__item__info__box__jobname__title").text()
            companyname = content(".contentpile__content__wrapper__item__info__box__cname").text()
            saray = content(".contentpile__content__wrapper__item__info__box__job__saray").text()
            demand = content(".contentpile__content__wrapper__item__info__box__job__demand").text()
            yield jobname, companyname, saray, ",".join(demand.split("\n"))
 
 
datas = ZhiLian().data_processing()
for data in datas:
    print(data)