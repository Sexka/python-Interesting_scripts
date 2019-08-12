import requests
import os
from lxml import etree
from multiprocessing import Pool
 
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}
DETAIL_URLS_LIST = []
 
 
def get_url():
    for i in range(4,5):#要抓几页就改一下这个
        url = 'http://www.52guzhuang.com/forum-59-%d.html' %i
        yield url
 
 
def get_detail_url():
    urls = get_url()
    for url in urls:
        response = requests.get(url, headers=HEADERS).content.decode('gbk')
        html = etree.HTML(response)
        detail_url_list = html.xpath('//*[@id="threadlist"]/div[3]/div/div/div/div[3]/div[1]/a[2]/@href')
        for detail_url in detail_url_list:
            DETAIL_URLS_LIST.append(detail_url)
 
 
def parse_url():
    get_detail_url()
    for detail_url in DETAIL_URLS_LIST:
        response = requests.get(detail_url, headers=HEADERS)
        html = etree.HTML(response.content.decode('gbk'))
        img_title = html.xpath('//*[@id="thread_subject"]/text()')[0]
        img_urls = html.xpath('//td[@class="plc"]/div[@class="pct"]//div[@align="center"]/ignore_js_op/img[@class="zoom"]/@zoomfile')
        yield img_title,img_urls
        # for img_url in img_urls:
        #     print(img_url)
 
 
def save_images(title, urls):
    for url in urls:
        image_url = 'http://www.52guzhuang.com/'+ url
        image = requests.get(image_url,headers=HEADERS).content
        file_path = 'img' + os.path.sep + title
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
        img_path = file_path + os.path.sep + url[-25:]
        if os.path.exists(img_path) is True:
            print('已经下载'+ img_path)
        if os.path.exists(img_path) is False:
            print('正在下载'+ img_path)
            with open(img_path,'wb') as f:
                f.write(image)
 
 
if __name__ == '__main__':
    pool = Pool()
    for title, urls in parse_url():
        pool.apply_async(save_images(title,urls))
    pool.close()
    pool.join()