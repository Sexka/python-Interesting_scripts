import requests
import re
import os
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
}
def download(url,chapters_name,title,path):
    html = requests.get(url,headers = headers)
    text = re.findall('<body class="clearfix">(.*?)<div class="chapter-view">',html.text,re.S)[0]
    chapterImages = re.findall('(\\[[^\\]]*\\])',text,re.S)
    host = re.findall('pageImage = "(.*?)";',text,re.S)[0].split('/')[2]
    chapterPath = re.findall('chapterPath = "(.*?)"',text,re.S)[0]
    #print(host)
    #print(chapterImages)
    chapterImages_list = eval(chapterImages[2])
    for x in chapterImages_list:
        print(x)
        download_url = 'http://' + host + '/' + chapterPath +  x
        print(download_url)
        file1 = requests.get(download_url,headers = headers)
        with open(path + '\\' + x,'ab') as code:
            code.write(file1.content)
def get_chapter(url):
    html = requests.get(url,headers = headers)
    html.encoding='utf-8'
    text = re.findall('<div class="chapter-body clearfix">(.*?)<div class="chapter-category clearfix">',html.text,re.S)[0].replace('\n','').replace(' ','')
    #print(data)
    title = re.findall('<h1><span>(.*?)</span></h1>',html.text,re.S)[0]
    data = re.findall('<li><ahref="(.*?)"class=""><span>(.*?)</span>',text,re.S)
    print(title)
    for x in data:
        url = 'https://www.36mh.com' + x[0]
        chapters_name = x[1]
        print(chapters_name)
        path1 = os.getcwd()
        path2 = path1 + '\\' + title + '\\' + chapters_name
        os.makedirs(path2)
        #print(path2)
        download(url,chapters_name,title,path2)
if __name__ == '__main__':
    print('请输入链接，例如：https://www.36mh.com/manhua/yukuaideshiyi/')
    url = input()
    get_chapter(url)