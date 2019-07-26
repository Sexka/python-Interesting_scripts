import requests
import json
import re
import threading
import time
from multiprocessing.dummy import Pool as ThreadPool #多线程
 
 
def get_weather(city):
    url=f"https://wthrcdn.etouch.cn/weather_mini?city={city}"
    try:
        requests.packages.urllib3.disable_warnings() #取消警告报错 （提示警告InsecureRequestWarning的问题处理）
        html=requests.get(url, verify=False).json()  # 请求API接口，取消了HTTPS验证
        dates=html['data']['forecast'][0]
        wind = re.findall("\<\!\[CDATA\[(.*?)\]\]\>", dates["fengli"], re.S)[0]  # 正则获取风力大小
        #print(dates)
        print('\n')
        print('-----------------------------------')
        print(f"城市：{city}")
        print(f"日期：{dates['date']}")
        print(f"最高温度：{dates['high']}")
        print(f'风力大小：{wind}')
        print(f"最低温度：{dates['low']}")
        print(f"风向：{dates['fengxiang']}")
        print(f"天气：{dates['type']}")
        print('-----------------------------------')
        print('\n')
    except:
        print(f"获取{city}天气情况失败！")
 
 
 
def get_weather2(url):
    try:
        requests.packages.urllib3.disable_warnings() #取消警告报错 （提示警告InsecureRequestWarning的问题处理）
        html=requests.get(url, verify=False).json()  # 请求API接口，取消了HTTPS验证
        dates=html['data']['forecast'][0]
        wind = re.findall("\<\!\[CDATA\[(.*?)\]\]\>", dates["fengli"], re.S)[0]  # 正则获取风力大小
        #print(dates)
        print('\n')
        print('-----------------------------------')
        print(f"日期：{dates['date']}")
        print(f"最高温度：{dates['high']}")
        print(f'风力大小：{wind}')
        print(f"最低温度：{dates['low']}")
        print(f"风向：{dates['fengxiang']}")
        print(f"天气：{dates['type']}")
        print('-----------------------------------')
        print('\n')
    except:
        print(f"获取天气情况失败！")
 
 
 
 
def get_thread():
    threads=[]
    city_data=[
        '深圳','广州','上海','赣州','北京','天津','南京','大理','武汉','长沙','九江'
    ]
    num=range(len(city_data))
    #print(num)
    for i in num:
        t=threading.Thread(target=get_weather,args=(city_data[i],))
        threads.append(t)
 
    for i in num:
        threads[i].start()
        time.sleep(0.5)
 
    for i in num:
        threads[i].join()
 
    print("获取城市天气情况完成！")
 
 
 
 
def get_thread2():
    urls=[]
    city_data=[
            '深圳','广州','上海','赣州','北京','天津','南京','大理','武汉','长沙','九江'
        ]
    for data in city_data:
        url=f'https://wthrcdn.etouch.cn/weather_mini?city={data}'
        urls.append(url)
    print(urls)
    try:
        # 开4个 worker，没有参数时默认是 cpu 的核心数
        pool = ThreadPool()
        results = pool.map(get_weather2,urls)
        pool.close()
        pool.join()
        print("获取城市天气情况完成！")
    except:
        print("Error: unable to start thread")
 
 
get_thread()
get_thread2()