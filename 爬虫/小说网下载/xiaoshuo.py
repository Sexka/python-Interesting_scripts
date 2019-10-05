import requests
from lxml import etree
import time
import os
import re
 
headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36",
         "Referer":"http://www.xbiquge.la/13/13959/"}
#伪造浏览器访问
url="http://www.xbiquge.la/13/13959/"
res=requests.get(headers=headers,url=url)
res.encoding= res.apparent_encoding
response=res.text
#print(response)
 
html=etree.HTML(response)
title=html.xpath("//*[@id='list']/dl/dd/a/text()")
#小说每个篇章的标题
title_url=html.xpath("//*[@id='list']/dl/dd/a/@href")
pingjie="http://www.xbiquge.la/"
real_url=[]
#小说每个篇章的地址
for neirong in title_url:
    real_url.append(pingjie+neirong)
#print("\n".join(real_url))
#print("\n".join(x for x in title_url))
 
os.chdir(os.getcwd())
if not os.path.exists(os.getcwd()+"/book"):
    print("目录不存在，准备创建目录")
    os.mkdir("book")
    os.chdir(os.getcwd()+"/book")
else:
    print("目录已存在")
    os.chdir(os.getcwd()+"/book")
 
 
#time.sleep(5)
localpath=os.getcwd()#原始目录
print("\n原始地址是:"+str(localpath))
#time.sleep(20)
 
 
for i in range(len(real_url)):
 
    # os.chdir(localpath)  # 目录重定位，不然会乱
    # # 给定位，然后判断文件夹在不在，若不在则创建
    # realpath = os.getcwd() + os.path.sep + str(title[i])+".txt"
    # if not os.path.exists(realpath):
    #     with open(title[i]+".txt","w")as w:
    #         pass
    #     print('\n文件夹' + str(title[i]) + '不存在,创建完成')
    # else:
    #     print('\n文件夹' + str(title[i]) + '已存在,无需创建')
    #
    #
    # print("\n当前目录是:" + str(os.getcwd()) + "\n")
 
 
 
 
 
 
 
 
    res = requests.get(headers=headers, url=real_url[i])
    res.encoding = res.apparent_encoding
    response = res.text
    html = etree.HTML(response)
    word=html.xpath("//*[@id='content']/text()")
    word=str(word)
 
    c=word.replace(r"\xa0\xa0\xa0\xa0","")
    c=c.replace(r"'\r',","\n")
    c=c.replace(r"\r","")
    c=re.sub(r"[\'\]\[]","",c)
    #c=re.sub(r",$,","",c)
    #print(c)
 
 
 
    with open(title[i]+".txt","w")as f:
        print("正在下载"+str(title[i])+"\n")
 
        f.write(c)
        print(str(title[i])+"下载完成"+"\n")
        f.write("\n\n================")