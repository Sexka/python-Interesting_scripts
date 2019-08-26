import re
import requests
from requests.exceptions import ConnectionError
import json
 
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
 
#get网站通用框架
def get_url(url):
    try:
        r=requests.get(url,headers=headers)
        r.encoding='utf-8'
        html=r.text
        return html
        # return r.content.decode()
    except ConnectionError as e:
        print('采集错误%d'%e)
 
def re_html(html):
    contents=[]
    #正则表示，获取内容
    content=re.findall(r'<div class="cont.*?<span>(.*?)</span>.*?</div>',html,re.S)
    #获取昵称
    name=re.findall(r'<h2>(.*?)</h2>',html,re.S)
    for i in content:
        #把正文的<br/>标签替换成空，并添加到列表里
        contents.append(i.replace('<br/>',''))
    for a in range(len(name)):
        data = {
            'name':name[a],
            'content':contents[a]
        }
        datas = json.dumps(data,indent=4,ensure_ascii=False)
        print(datas)
        with open('糗事百科.json','a',encoding='utf8') as f:
            f.write(datas)
 
def main():
    for i in range(1,36):
        #循环糗百每一页的网址
        print('第%s页'%i)
        url='https://www.qiushibaike.com/textnew/page/%s/?s=5222421'%i
        data=get_url(url=url)
        re_html(html=data)
 
if __name__ == '__main__':
    main()