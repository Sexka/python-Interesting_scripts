import requests
import urllib.parse
import json
import time
import os

while  1:
       
        musicname=input("请输入歌曲名字：")
        key={"key":musicname}
        key=urllib.parse.urlencode(key)
        #歌曲列表页面url
        url1="http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?"+key+"&pn=1&rn=30"

        headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}
        result1=requests.get(url1,headers=headers)
        # print(result1.text)
        data1=json.loads(result1.text)["data"]["list"]#json数据转化为字典，list里存放了歌曲信息
        # print(type(data1))

        rid=[]
        name=[]
        artist=[]
        urllist=[]
        print("歌曲列表：")
       
        for i in data1:
                ridnum=i["rid"]
                namee=i["name"]
                artistt=i["artist"]
                time.sleep(0.2)
                # print(ridnum)
               
                rid.append(ridnum)
                name.append(namee)
                artist.append(artistt)
               
        #在桌面新建文件夹       
        if os.path.exists(r"C:\Users\Administrator\Desktop\music"):#判断文件夹images是否存在
            pass
        else:
            os.mkdir(r"C:\Users\Administrator\Desktop\music")  #创建文件夹images


        for y in range(0,len(rid)):
                rid_={"rid":rid[y]}
                rid_=urllib.parse.urlencode(rid_)
                #构造列表页面各个歌曲的url
                url2="http://www.kuwo.cn/url?format=mp3&"+rid_+"&response=url&type=convert_url3"
                # print(url2)
                urllist.append(url2)
                #打印列表页面各个歌曲的名字，作者
                print(str(y)+">>>{}{}{}".format(name[y],"——",artist[y]))

        A=1
        while A==1:
                getlist=input("请选择你要下载的歌曲:")

                url3=urllist[int(getlist)]#你选择的歌曲的url
                name_=name[int(getlist)]#你选择的歌曲名字
                artist_=artist[int(getlist)]#你选择的歌曲的作者

                result2=requests.get(url3,headers=headers)
                # print(type(result2.text))
                data2=json.loads(result2.text)["url"]#你选择的歌曲的mp3的url
                # print(data2)
                # print(type(data2))



                print("正在下载................................")
                result3=requests.get(data2,headers=headers)
                mp3=result3.content

                #写文件
                with open(r"C:\Users\Administrator\Desktop\music\{}{}{}.mp3".format(name_,"——",artist_),"wb") as f:
                        f.write(mp3)
               
                print("下载成功！\n............................")
                A=int(input("还需要下载本列表其他歌曲（确认1，取消0）:"))
                print("........................................")