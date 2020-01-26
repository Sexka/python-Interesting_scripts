import gevent
import gevent.monkey
gevent.monkey.patch_all()
import requests
import re
import os
import time
def get_file_num(path):        #获取path目录下的文件总数
    for a,b,files in os.walk(path):
        return len(files)
def get_ts(url,name,work_path):  #下载一个ts文件。url是下载地址，work_path是要保存磁盘的目录。
    print('start ' ,name)
    urls = 'https://1*'+url
    headers={'Connection': 'close'}
    try:  #下载太快出现连接错误时的解决方法。
        response = requests.get(urls,headers=headers)   
    except:
        urls = 'https://2*' + url
        try:
            response = requests.get(urls, headers=headers)
        except:
            urls = 'https://3*' + url
            try:
                response = requests.get(urls, headers=headers)
            except:
                print('下载失败：',name)
                return
    ts = response.content
    with open(work_path + name, 'wb') as f:
        f.write(ts)
    print(urls,'finish')
def get_url(path):  #从磁盘的path路径读取index.m3u8文件并通过正则将每一个ts文件下载地址的后边部分形成一个list。
    pattern = re.compile(r'/hls.+ts')
    with open(path,'r') as f:
        l=pattern.findall(f.read()[112:])
        return l
def downmovie(m3u8_path,work_path): #进行下载
    os.chdir(work_path)
    path = m3u8_path
    l = get_url(path)
    p = []
    for i,url in enumerate(l):
        if os.path.exists(str(i)):
            pass
        else:
            p.append(gevent.spawn(get_ts, url, str(i),work_path))
    gevent.joinall(p)
    f_num = get_file_num(work_path)
    if f_num!=len(l):  #验证是否下载完所有的ts文件，没有的话等30s再去下载。（解决暂时封ip）
        print('部分没有下载完成,请30s后再次启动下载！')
def com_ts(movie_name,work_path):  #合并ts文件为一个或两个MP4
    os.chdir(work_path)
    tss = ''
    f_num = get_file_num(work_path)
    for i in range(f_num):
        if i>1800:
            break
        tss = tss + str(i) + '+'
    shell_str = 'copy /b ' + tss[:-1] + ' '+movie_name+'.mp4'
    print(shell_str)
    os.system(shell_str)
    if i>1800:
        for i in range(1800, f_num):
            tss = tss + str(i) + '+'
        shell_str = 'copy /b ' + tss[:-1] + ' ' + movie_name + '2.mp4'
        print(shell_str)
        os.system(shell_str)
 
def del_ts(work_path):  #删除所有ts文件
    f_num = get_file_num(work_path)
    for i in range(f_num-1):
        os.remove(work_path+str(i))
 
if __name__ == '__main__':  #下边三个函数每次只能运行一个，否则会出错。确保全部ts下载完成再去合并，确保合并完再去删除。
    downmovie('C:/Users/admin/Desktop/index.m3u8','C:/Users/admin/Desktop/movies/')
    com_ts('电影名','C:/Users/wangzi/Desktop/movies/')
    del_ts('C:/Users/admin/Desktop/movies/')