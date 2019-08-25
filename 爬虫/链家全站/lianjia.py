import requests
from lxml import etree
import pandas as pd
from requests.exceptions import ConnectionError
from threading import Thread
 
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
#get链接
def get_url(url):
    try:
        r = requests.get(url,headers=headers)
        r.encoding = 'utf8'
        html = etree.HTML(r.text)
        if r.status_code == 200:
            return html
    except ConnectionError as e:
        print('采集错误')+e
 
 
def xpath_html(html):
    #获取需要的数据
    type = []
    big = []
    direction = []
    finish = []
    follow = []
    money = []
    name = html.xpath('.//a[@class="title"]//text()')
    district = html.xpath('//div[@class="houseInfo"]/a/text()')
    sum = html.xpath('//div[@class="houseInfo"]/text()')
    sites = html.xpath('//div[@class="positionInfo"]/text()')
    site = html.xpath('//div[@class="positionInfo"]/a/text()')
    moneys = html.xpath('//div[@class="totalPrice"]//text()')
    unitPrice = html.xpath('//div[@class="priceInfo"]//div[2]//span//text()')
    followInfo = html.xpath('//div[@class="followInfo"]//text()')
    try:
        crumbs = html.xpath('.//div[@class="crumbs fl"]//h1//a//text()')[0]
    except:
        crumbs='null'
 
    for i in sum:
        #获取的是一个以a|b|c|d这种格式的一个总和数据
        #用split来分割，分别获取。
        try:
            type.append(i.split(' | ')[1])
            big.append(i.split(' | ')[2])
            direction.append(i.split(' | ')[3])
            finish.append(i.split(' | ')[4])
        except:
            type.append('null')
            big.append('null')
            direction.append('null')
            finish.append('null')
    for a in sites:
        follow.append(a.replace('  -  ', ''))
 
    for b in range(0, (len(moneys)), 2):
        money.append(moneys[b] + moneys[b + 1])
    try:
        tp=pd.DataFrame({
            'name':name,
            'district':district,
            'type':type,
            'big':big,
            'direction':direction,
            'finish':finish,
            'follow':follow,
            'money':money,
            'site':site,
            'unitPrice':unitPrice,
            'followInfo':followInfo
        })
    except:
        tp='null'
     
    #这里加个报错是因为，有缺失值，暂时没有找到解决方法，但是不想让他停止就暂时这样解决
    try:
        tp.to_csv('D://爬虫爬的玩意//%s.csv'%crumbs,mode='a',encoding='utf8',index=False,header=None)
    except:
        print('保存失败')
 
 
def main(html_l,start_url,end_url):
    #获取每个城市的链接
    qgg = html_l.xpath('//div[@class="city_province"]/ul//li/a//@href')
    try:
        for index in qgg:
            for i in range(start_url,end_url):
                #拼接上翻页的后缀，实现每个城市的翻页
                url=index+str('ershoufang/pg{}/'.format(i))
                print('第%s页'%i)
                data = get_url(url)
                xpath_html(html=data)
    except ConnectionError as e:
        print('失败')
 
if __name__ == '__main__':
    #选择城市的链接
    url_l='https://www.lianjia.com/city/'
    dete=get_url(url=url_l)
    thad=[]
    t1 = Thread(target=main,args=(dete,1,20))
    t2 = Thread(target=main,args=(dete,20,40))
    t3 = Thread(target=main,args=(dete,40,60))
    t4 = Thread(target=main,args=(dete,60,80))
    t5 = Thread(target=main,args=(dete,80,101))
    thad +=[t1,t2,t3,t4,t5]
    for i in thad:
        i.start()
    for i in thad:
        i.join()