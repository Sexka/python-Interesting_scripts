from lxml import etree
import requests
import os
import time
from multiprocessing import Pool
import random
import shutil
 
def reqq(html):
    a = requests.get(html, timeout=30)
    return a
 
def downn(image):
    # with open(image[-15:], 'wb+') as f:
    with open(os.path.basename(image), 'wb+') as f:
        im = reqq(image)
        f.write(im.content)
    return 0
def mkdir(name):
    path = name.strip() #去除首位空格
    path = path.rstrip("\\") #去除尾部\符号
    if os.path.exists(path):
        # print(name + '目录已存在')
        os.chdir(path)
        pass
    else:
        print('目录不存在，新建目录{}'.format(path))
        os.mkdir(path)
        os.chdir(path)
 
def datedown_log(item_nv):
    # 数据下载结果写入datadown_log.txt文件
    f = open('E:\\2717.com\\datadown_log.txt', 'a')
    content_wm = "{}'\r\n".format(item_nv)
    f.write(content_wm)
    f.close()
def removeDir(dirPath):
    # 删除文件夹
    if (os.path.exists(dirPath)):
        shutil.rmtree(dirPath)
def timeSleep(sleepTime):
    #sleepTime = random.randint(1, 5)
    print("休息：" + str(sleepTime) + " 秒。")
    iii = 0
    while iii < sleepTime:
        print("倒计时：" + str(sleepTime - iii - 1) + " 秒。")
        time.sleep(1)
        iii += 1
 
imagesUrl = [] #图片集合
def getNextPic(url):
    # https://www.2717.com/ent/meinvtupian/2019/316129_58.html
    htmlFileName = os.path.basename(url)
    htmlNext = url.replace(htmlFileName, "")
    l = reqq(url)
    q = etree.HTML(l.content)
    ima = q.xpath('//*[@id="picBody"]/p/a/img/@src')[0]  # 一页一图
    imagesUrl.append(ima)
    nextUrl = q.xpath('//*[@id="nl"]/a/@href')[0]
    print("正在疯狂爬取，图片地址！-->{}、{}".format(len(imagesUrl), ima))
    if len(imagesUrl) % 10 == 0:
        timeSleep(random.randint(0, 3))
    if nextUrl != "##":
        htmlNextPic = htmlNext + nextUrl
        getNextPic(htmlNextPic)
    else:
        #print(imagesUrl)
        return imagesUrl
if __name__ == '__main__':
    downImgNum = 0 # 下载图片数量
    for k in range(1, 237):
        images = []
        removeDir = []
        # https://www.2717.com/ent/meinvtupian/list_11_1.html
        html = 'http://www.2717.com/ent/meinvtupian/list_11_{}.html'.format(str(k))
        req = requests.get(html)
        a = etree.parse(html, etree.HTMLParser())
        re = a.xpath('//*[@class="MeinvTuPianBox"]/ul/li/a[1]/@href')
        #print(re)
        #print(len(re))
        mkdirName = a.xpath('//*[@class="MeinvTuPianBox"]/ul/li/a[2]/text()')
        #print(mkdirName)
        #print(len(mkdirName))
        #break
        try:
            i = 0
            for path in mkdirName:
                mkdir('E:/2717.com/'+path+'/')
                os.chdir('E:/2717.com/'+path+'/')
                try:
                    j = re[i]
                    getNextPic('http://www.2717.com/' + j)
                    print("正在下载。。。" + path + "第 " + str(k) + " 页" + "，第 " + str(i+1) + " 条")
                    imgIndex = 1 # 第几张图片
                    imaIndex = 1 # 当前第几张图
                    for downImg in imagesUrl:
                        #b = os.path.isfile((os.path.basename(downImg)))
                        # print('E:/mm530.net/' + path + '/' + os.path.basename(downImg))
                        #print(b)
                        if(os.path.exists('E:/2717.com/'+path+'/'+ os.path.basename(downImg))):
                            print("图片已经下载过，{}，第{}/{}张图片-->{}".format(path, str(imaIndex), str(len(imagesUrl)), downImg))
                            imaIndex += 1  # 当前第几张图
                            continue
                        else:
                            print("现在下载，{}，第{}/{}张图片-->{}".format(path, str(imgIndex), str(len(imagesUrl)), downImg))
                            if imgIndex % 10 == 0:
                                timeSleep(random.randint(1, 3))
                            downn(downImg)
                            imgIndex += 1
                            # print("----------下载完成----------")
                            downImgNum += 1
                            print("==========>>>共下载{}张图片！现在下载，第{}页 第{}/30条！<<<==========".format(downImgNum, str(k), str(i+1)))
                    imagesUrl.clear()  # 图片集合清空
                except Exception as err:
                    print(err)
                    print("下载出错。。。" + path + "第 " + str(k) + " 页" + "，第 " + str(i + 1) + " 条")
                    datedown_log(err)
                    removeDir.append('E:/2717.com/'+path+'/')
                finally:
                    i += 1
                    timeSleep(random.randint(1, 5))
                    imagesUrl.clear()  # 图片集合清空
        except Exception as err2:
            print('第{}页，第{}条。error'.format(str(k), str(i)))
            print(err2)
            datedown_log(err2)
        # 下载一页休息
        timeSleep(random.randint(1, 30))
        # 删除空目录
        #if(len(removeDir) > 0):
            #removeDir(removeDir[0])
            #removeDir.remove(removeDir[0])