# -*- coding: utf-8 -*-
 
import requests,time,os
from lxml import etree
from urllib import request
 
name_url = {}            #创建一个字典
def sort():
    req = requests.get('https://www.tujigu.com/')           #首页
    req.encoding = 'utf-8'                               #中文出现乱码，调整编码
    req_xp = etree.HTML(req.text)                     #装换为xp，text是为了变成字符串形式，不然会报错
    text_list = req_xp.xpath('//*[@class="menu"]/li/a/text()|//*[@id="tag_ul"]/li/a/text()')                 #读取分类名
    href_list = req_xp.xpath('//*[@class="menu"]/li/a/@href|//*[@id="tag_ul"]/li/a/@href')                   #获取网址
    for href,text in zip(href_list,text_list):
        name_url[text] = href                     #已分类名做为key，网址作为值
    return text_list               #返回分类名列表，好为后面打印分类名
 
def dow(url,name):
    if not os.path.exists("图集谷"):          #检查并创建文件夹，强迫症~~~
        os.mkdir('图集谷')
    if not os.path.exists("图集谷/{}".format(name)):           #同上，创建分类
        os.mkdir('图集谷/{}'.format(name))
    atlas = requests.get(url)                 #get你选择的网址
    atlas.encoding = 'utf-8'                      #同上，乱码问题
    atlas_xp=etree.HTML(atlas.text)
    text_list = atlas_xp.xpath('//*[@class="biaoti"]/a/text()')       #获取图集名
    href_list = atlas_xp.xpath('//*[@class="biaoti"]/a/@href')
    for text,href in zip(text_list,href_list):
        req = requests.get(href)
        req.encoding = 'utf-8'
        req_xp1=etree.HTML(req.text)
        src_list = req_xp1.xpath('//*[@class="content"]/img/@src')
        num = 1          #创建图片名，美观
        #下面是为了删除一些图集中包含了文件夹不能创建的符号
        text = text.replace('\n', '').replace('/', '').replace('\\', '').replace(':', '').replace('*', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '').replace('?', '')
        if not os.path.exists("图集谷/{}/{}".format(name,text)):       #检测此图集是否下载过
            os.mkdir("图集谷/{}/{}".format(name,text))
            for src in src_list:
                request.urlretrieve(src,"图集谷/{}/{}/{}.jpg".format(name,text,num))     #保存图片
                num += 1
            print('{}-------------成功下载'.format(text))
        else:
            print('{}--------------内容已下载'.format(text))
 
def get():
    while 1:
        text_list = sort()       #从首页获取分类信息和url
        i = 1                    #序号
        for text in text_list[2:-1]:      #从2到-1是为了去除没用的分类
            print('%02d.{}'.format(text)%i)    #打印分类信息
            i += 1
        opt = input('输入您要爬取的内容（首页为默认）>>>>> ')
        if not opt.isdigit():           #判断输入内容
            print('傻X输入中文懂么')
            time.sleep(3)
            continue
        opt = int(opt)
        if not 0 < opt < len(text_list)-3:   #判断输入内容
            print('输入范围错误')
            time.sleep(3)
            continue
        opt += 1              #以为删除了首页，所以+1才能正确选择分类
        url=name_url[text_list[opt]]           #获取你选择的地址
        name = text_list[opt]             #分类的名字，好创建一个文件夹放入
        print('{}====开始爬取'.format(name))
        dow(url,name)                   #开始运行下载程序
        input('爬取完成，按下回车重新开始')
 
if __name__ == '__main__':
    get()              #开始运行主程序