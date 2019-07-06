import urllib.request
import json
import threading
import random
import os
size=0
pageid=1
downloadnum=0
def get(url):
    url=url
    request=urllib.request.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0')
    request.add_header('X-Forwarded-For',str(random.randint(0,255))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))+'.'+str(random.randint(0,255)))
    result=urllib.request.urlopen(request).read()
    return result
def save(url,filename):
    with open(filename,"wb") as f:
        f.write(get(url))
        print(filename+"OK")
    global size
    size+=os.path.getsize(filename)
    global downloadnum
    downloadnum+=1
def download(result,filepath):
    for i in range(0,len(result)):
        if (result[i]['src']):
            save(result[i]['src'],filepath+"/"+result[i]['trackName']+'.m4a')
        else:
            print("%s下载失败(可能是付费专辑)" %(result[i]['trackName']))
def main():
    filepath=input("请输入存放路径\n")
    if os.path.exists(filepath):
        if (os.listdir(filepath)):
            print("文件夹'%s'已经存在且不为空" %(filepath))
            main()
        else:
            print("文件夹'%s'为空,将使用该文件夹" %(filepath))
    else:
        os.mkdir(filepath)
        print("文件夹'%s'将被创建" %(filepath))
    id=input("请输入id\n")
    try:
        id=int(id)
    except Exception as e:
        print("错误:"+e)
        print("可能原因:ID非纯数字")
        main()
    print("开始下载".center(30,"#"))
    pageid=1
    hasMore=1
    while hasMore:
        url="https://www.ximalaya.com/revision/play/album?albumId="+str(id)+"&pageSize=30&pageNum="+str(pageid)
        result=get(url).decode('utf-8')
        hasMore=json.loads(result)['data']['hasMore']
        result=json.loads(result)['data']['tracksAudioPlay']
        download(result,filepath)
        pageid+=1
    print("下载结束".center(30,"#"))
    print("文件存放路径%s,一共下载%s集,占用空间%.2fMb" %(os.getcwd()+"/"+filepath,downloadnum,size/1024/1024))
if __name__ == "__main__":
    main()