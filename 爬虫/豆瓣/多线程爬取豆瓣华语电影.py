import requests
import time
from lxml import etree
 
import threading
from queue import Queue
#构造url的地址
header={"Host": "movie.douban.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
def url_page():
    global urls
    for i in range(10):
        i*=25
        url="https://movie.douban.com/top250?start={}&filter=".format(i)
        qu.put(url)
def get_url():#请求url，提取信息
    url=qu.get()
    global fb
    response=requests.get(url,headers=header)
    html=response.text
    doc=etree.HTML(html)
    items=doc.xpath('//div[@class="info"]')
    for item in items:
        movies_url=item.xpath('./div[@class="hd"]/a/@href')[0]
        movies_name=item.xpath('./div[@class="hd"]/a//text()')
        movies_name = [x.strip() for x in movies_name if x.strip() != '']
        movies_name="".join(movies_name).replace(",","")
        movies_yanyuan=item.xpath('./div[@class="bd"]/p/text()')[0].strip()
        movies_type = item.xpath('./div[@class="bd"]/p/text()')[1].strip()
        movies_pingfen = item.xpath('./div[@class="bd"]/div/span[@class="rating_num"]/text()')[0].strip()
        movies_people = item.xpath('./div[@class="bd"]/div/span/text()')[-1].strip()
        print("正在抓取{}".format(movies_name))
        fb.write("{},{},{},{},{},{}\n".format(movies_name,movies_yanyuan,movies_type,movies_pingfen,movies_people,movies_url))
if __name__ == '__main__':
    urls=[]
     
    qu=Queue(30)
    fb = open("豆瓣电影.csv", "w", encoding="utf-8")
    fb.write("电影名称,演员,类型,评分,评价人数,详情网页\n")
    print("开始抓取")
    url_page()
    while True:
        for i in range(2):
            t=threading.Thread(target=get_url)
            t.start()
        if qu.empty():
            break
        t.join()
    print("抓取成功，保存成功")