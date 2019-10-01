import requests
import urllib.parse
from tqdm import tqdm
import time
 
def get_songs(url,keyword):
    #对keyword进行urlencode加密
    key = urllib.parse.quote(keyword)
    headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36'
    }
    #row为最大显示的结果数
    params = {
        'rows': 20,
        'type': 2,
        'keyword': key,
        'pgc': 1,
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code ==200:
        return response.json()['musics']
    else:
        print('fail to get audiolist. status_code is',response.status_code)
 
#下载进度可视化
def downloadFILE(url,name):
    resp = requests.get(url=url,stream=True)
    content_size = int(int(resp.headers['Content-Length'])/1024)
    with open(name, "wb") as f:
        print("Pkg total size is:",content_size,'k,start...')
        for data in tqdm(iterable=resp.iter_content(1024),total=content_size,unit='k',desc=name):
            f.write(data)
        print(name , "download finished!")
 
 
def main():
    url = 'http://m.music.migu.cn/migu/remoting/scr_search_tag'
    keyword = input('其输入搜索关键词：')
    audiolist = get_songs(url,keyword)
    count = 0
    for item in audiolist:
        songName = item['songName']
        artist = item['artist']
        #mp3 = item['mp3']
        print(count,songName,artist)
        count+=1
    index = input('请输入需要下载的歌曲前序号(默认下载第一首)：')
    if index == '':
        index = 0
    target_link = audiolist[int(index)]['mp3']
    save_name = audiolist[int(index)]['songName']+' '+audiolist[int(index)]['artist']+'.mp3'
    downloadFILE(target_link,save_name)    
     
 
if __name__ == "__main__":
    main()