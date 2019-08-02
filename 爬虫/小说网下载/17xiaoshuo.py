import requests
from bs4 import BeautifulSoup
def get_fiction():
    for line in open("目录.txt"): 
        link=line
        r=requests.get(link)
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text, 'lxml')
        title=soup.find('div',class_='readAreaBox content').h1.text.strip()
        text=soup.find('div',class_='p').text.strip()
        text.replace('\r\n','')
        with open('小说.txt', 'a+',encoding='utf-8') as f:
                f.write('\n'+title+'\n'+text)
                print(title+'已完成')
def get_url():
    
    link=str(input("（本程序支持www.17k.com）请输入小说目录地址："))
    r=requests.get(link)
    r.encoding='utf-8'
    soup=BeautifulSoup(r.text, 'lxml')
    urllist=soup.find_all('a')
    for url in urllist:
        xc='chapter'
        dc=url.get('href')
        if xc in dc:
            with open('目录.txt', 'a+',encoding='utf-8') as f:
                f.write('http://www.17k.com'+dc+'\n')

if __name__ == '__main__':
    get_url()
    get_fiction()