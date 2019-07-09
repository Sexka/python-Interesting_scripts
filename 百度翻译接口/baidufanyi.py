# /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import random
import hashlib
q = '苹果'
salt = str(random.randint(0,50))
#申请网站 http://api.fanyi.baidu.com/api/trans
appid = ''
secretKey = ''
sign = appid+q+salt+secretKey
# sign=sign.encode("utf-8")
# m = hashlib.md5()
# m.update(sign)
# sign = m.hexdigest()
#转换为MD5
sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()
# print(sign)
head = {'q':f'{q}',
'from':'zh',
'to':'en',
'appid':f'{appid }',
'salt':f'{salt}',
'sign':f'{sign}'}
def fanyi(head):
    j = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate',head)
    print(j.json())
if __name__ == '__main__':
    fanyi(head)