import requests
import json
from selenium import webdriver
import re
from urllib.request import urlretrieve

 
 
def get_url():
    url = f'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={name}'
    driver.get(url)
    driver.implicitly_wait(10)
    data = driver.find_element_by_xpath('//div[@class="songlist__item"]//span[@class="songlist__songname_txt"]/a').get_attribute('href')
    print(data)
    data = {'mid': data}
    return data
 
 
def get_music_url(data):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '65',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.douqq.com',
        'Origin': 'http://www.douqq.com',
        'Referer': 'http://www.douqq.com/qqmusic/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    print(data)
    url = 'http://www.douqq.com/qqmusic/qqapi.php'
    req = requests.post(url, data=data, headers=headers).text
    print(req)
    req = json.loads(req)
    print(req)
    req = req.replace('\/\/', '//').replace('\/', '/')
    print(type(req))
    print(req)
    rg = re.compile('"mp3_l":"(.*?)",')
    rs = re.findall(rg, req)[0]
    print(rs)
    return rs
 
 
def get_music(rs):
    urlretrieve(rs, name+'.mp3')
 
 
def go():
    data = get_url()
    rs = get_music_url(data)
    get_music(rs)
 
 
if __name__ == '__main__':
    name = input('请输入你想要下载的歌曲：')
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=r'C:\Users\1\PycharmProjects\untitled\验证码\chromedriver.exe',
                              chrome_options=option)
 
    go()