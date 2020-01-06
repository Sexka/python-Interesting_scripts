import requests
import re
import os
import gevent
from Crypto.Cipher import AES
from gevent import monkey,pool
from collections import Counter
import time
import sys
gevent.monkey.patch_all()
 
 
url="http://www.91mmd.xyz/play?type=ckplayer&linkId=1886894"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","connection":"close"}
r=requests.get(url,headers=headers)
 
#是否加密flag
haskey=False
m3u8_url=Counter(re.findall("http.*?index\.m3u8", r.text)).most_common(1)[0][0]
#找到提取内容重复次数最多的链接
if not "hls" in m3u8_url:
    m3u8_url=re.sub("index.m3u8","1000kb/hls/index.m3u8",m3u8_url)
    # video_index=re.sub("index.m3u8",r.text.split("\n")[-1],m3u8_url)
 
#判断是哪一种m3u8,需要有视频的那页
r=requests.get(m3u8_url,headers=headers)
ts_list=[]
for index,ts in enumerate(re.findall('(\w*?\.ts)', r.text)):
    ts_list.append((str(index).zfill(5),m3u8_url.replace("index.m3u8", ts)))
#视频链接存入列表，为保存顺序加index，补齐5位方便合成 列表内容是（index,url）
 
a=len(ts_list)
b=a
c=0
 
#判断文件里有没有key.key来确定是否有加密
if 'URI="key.key"' in r.text:
    key_url=re.sub("index.m3u8","key.key",m3u8_url)
    key=requests.get(key_url,headers=headers).text
    cryptor=AES.new(key, AES.MODE_CBC, key)
    #新建一个对象来处理key
    haskey=True
 
 
 
def save_video(ts):
    try:
 
        #用了协程所以需要共享一些参数，懒得搞直接上global
        global a
        global b
        file_name=ts[0]
        root = os.getcwd()
        if not os.path.exists(root+"/"+file_name):
            r = requests.get(url=ts[1], headers=headers,timeout=10)
            with open(file_name+".ts", "wb")as f:
                if haskey==True:
                    #这里判断有没有加密，如果有就解密
                    f.write(cryptor.decrypt(r.content))
                else:
                    f.write(r.content)
        a=a-1
 
        #简陋的进度条
        hashes = '#' * int((b-a)/int(b) * 40)
        spaces = ' ' * (40 - len(hashes))
        sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, (b-a)/b*100))
        sys.stdout.flush()
    except:
        #统计失败文件次数
        global c
        a=a-1
        c=c+1
         
def rename(name="学习资料"):
    os.system("(for %a in (*.ts) do @echo file '%a') > list.txt")
    os.system(f"ffmpeg -f concat -safe 0 -i list.txt -c copy {name}.mp4")
    os.system('del /Q *.ts')
    os.system('del /Q list.txt')
    os.system("exit")
     
     
if __name__=="__main__":
    pool = gevent.pool.Pool(50)
    threads = []
    for i in ts_list:
        threads.append(pool.spawn(save_video,i))
    gevent.joinall(threads)
    #视频是拿来学习python的，根本不会去看，所以也没必要考虑重试
    #下载完成后会有一次改名机会
    print(f"下载完成 失败:{c}/{b}")
    name=input("重命名：")
    if name:
        rename(name)
    else:
        rename()