
import requests
from bs4 import  BeautifulSoup
from bs4.element import Tag
from requests.exceptions import RequestException 
import re 
import json 
from datetime import datetime 

class Proxy:

    __ips = []
    __avilables=[]
    __count = 0

    __hosts = {
            'xila':'http://www.xiladaili.com',
            }
    __headers = {
            'host': 'www.xiladaili.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
    def __init__(self):
        self.proxies = None

    def get(self):
        for host in self.hosts:
            pass 

    def xila(self, host):
        reponse = requests.get(host, headers=self.__headers)
        status_code = reponse.status_code 
        text = reponse.text 
        print('[get xila web :) status:%d]'%status_code)
        soup = BeautifulSoup(text, 'lxml')
        scroll_1 = soup.find(id='scroll')
        trs_1 = scroll_1.table.tbody.find_all('tr') 
        for tr in trs_1:
            dic = {'ip':tr.td.string,'proxy': tr.contents[5].string}
            self.__ips.append(dic) 
            self.__count += 1

        scroll_2 = scroll_1.find_next(id='scroll')
        trs_2 = scroll_2.table.find_all('tr')
        for tr in trs_2:
            if tr.td:
                dic = {'ip':tr.td.string,'proxy': tr.contents[5].string}
                self.__ips.append(dic) 
                self.__count += 1

        scroll_3 = scroll_2.find_next(id='scroll')
        trs_3 = scroll_3.table.find_all('tr')
        for tr in trs_3:
            if tr.td:
                dic = {'ip':tr.td.string,'proxy': tr.contents[5].string}
                self.__ips.append(dic) 
                self.__count += 1
        with open('./proxies.txt', 'w') as f:
            for d in self.__ips:
                json.dump(d,f)
                f.write('\n')

    def check_avilable(self):
        if self.__ips is None:
            print('proxy not get, please call get_proxy() first, :(')

        test_url = 'https://www.baidu.com'
        for d in self.__ips:
            proxy = d['ip']
            if re.compile('^H.*?P,H.*?S$').search(d['proxy']):
                proxies = {
                        'http': 'http://'+proxy,
                        'https': 'https://'+proxy 
                }
            if re.compile('^H.*P$').search(d['proxy']):
                proxies = {
                        'http': 'http://'+proxy,
                }
            if re.compile('^HTTPS$').search(d['proxy']):
                proxies = {
                        'https': 'https://'+proxy,
                }
            try:
                reponse = requests.get(test_url, proxies=proxies, timeout=10)
                if reponse.status_code == 200:
                    print(d['ip'] +'\t'+d['proxy']+ '>>>> is avilable')
                    self.__avilables.append(d)
            except RequestException as err:
                log = '[time]: {} \t  [ip]: {} \t [proxy]: {} \t [err]: {} \n'.format(datetime.utcnow(), d['ip'], d['proxy'], err)
                print(log)
                with open('./log.txt', 'a') as f:
                    f.write(log)

        with open('./avilables.txt', 'w') as f:
            for d in self.__avilables:
                json.dump(d,f)
                f.write('\n')

    def set_ips(self):
        if self.__ips:
            print('already exits ips')

        with open('./proxies.txt', 'r') as f:
            while True:
                line = f.readline()
                if line:
                    d = json.loads(line)
                    self.__ips.append(d)
                else:
                    break 

    def get_ips(self):
        with open('./avilables.txt', 'r') as f:
            while True:
                line = f.readline()
                if line:
                    d = json.loads(line)
                    self.__avilables.append(d)
                else:
                    break 
        for d in self.__avilables:
            yield d

if __name__ == '__main__':
    proxy = Proxy()
    #proxy.xila('http://www.xiladaili.com')
    #proxy.set_ips() 
    #proxy.check_avilable()
    gene = proxy.get_ips()
    while True:
        input('input:')
        print(next(gene))