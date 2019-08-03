import pdfkit
import requests
from lxml import etree
import re
 
confg = pdfkit.configuration(wkhtmltopdf=r'C:\Users\Administrator\AppData\Local\Programs\Python\Python37\wkhtmltox\bin\wkhtmltopdf.exe')
 
 
#获取链接
def get_listurl():
    url="https://www.dusaiphoto.com/article/detail/2/"
    list_url = [url,]
    html=requests.get(url).content.decode('utf-8')
    con=re.findall(r'<div class="card-text" style="overflow: hidden">(.+?)<div class="container-fluid">',html,re.S)[0]
    listurls=re.findall(r'<p class="mb-0">.+?<a href="(.+?)".+?style="color: #b8b8b8;"',con,re.S)
    for listurl in listurls:
        listurl=f'https://www.dusaiphoto.com{listurl}'
        list_url.append(listurl)
    print(list_url)
    return list_url
 
#获取正文内容
def get_content(url):
    html=requests.get(url).content.decode('utf-8')
    content=re.findall(r'<div class="mt-4">(.+?)<div class="mt-4 mb-4">',html,re.S)[0]
    return content
 
#保存html为pdf文档
def dypdf(contents):
    contents=etree.HTML(contents)
    s = etree.tostring(contents).decode()
    print("开始打印内容！")
    pdfkit.from_string(s, r'out.pdf',configuration=confg)
    print("打印保存成功！")
 
 
if __name__ == '__main__':
    contents=''
    urls=get_listurl()
    for url in urls:
        print(url)
        content=get_content(url)
        contents='%s%s%s'%(contents,content,'<p><br><p>')
 
    dypdf(contents)