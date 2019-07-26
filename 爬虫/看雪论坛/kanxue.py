import re,json,os,sys,time,requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import quote,unquote
 
def filterFName(FName):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_name = re.sub(rstr, "_", FName)
    return new_name
 
def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
 
def gethtml(url,encode):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
    r = requests.get(url,headers=headers)
    r.encoding = encode
    return r.text
 
def writehtml(path,str):
    f = open(path,'w+',encoding='utf-8')
    f.write(str)
    f.close
 
def postdata(url,pdata):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    rep = requests.post(url=url, data=pdata, headers=headers)
    return rep.text
 
def forstr(mstr):
    mstr=mstr.replace('{', '').replace('}', '').replace(' ', '').replace('"', '')
    pId = mstr.split(',')[2].split(':')[1]
    id = mstr.split(',')[0].split(':')[1]
    name =mstr.split(',')[1].split(':')[1].replace('"','')
    return id,pId,name
 
def getlv(lname,listtxt,num):
    global txt,count,zcount
    gurl = 'https://www.kanxue.com/chm-thread_last_read.htm'
    id,pId,name=forstr(listtxt)
    pdata = {"chmid": pId, "cateid": id, "nodename": quote(name, 'utf-8')}
    repdata = postdata(gurl, pdata)
    jsonstr = json.loads(repdata)
    txt = txt + '<h' + str(num) + '>' + name + '</h' + str(num) + '><br>'
    n = []
    for j in zlist:
        jid,pId1,name1=forstr(j)
        if pId1==id:
            n.append(j)
    if len(n)>0:
        for k in n:
            fname = k.split(',')[1].split(':')[1].replace('"', '').replace(' ', '')
            llname = lname + '->' +fname
            getlv(llname,k,num+1)
    if jsonstr['code'] != '-1':
        for m in range(len(jsonstr['message'])):
            html=gethtml('https:'+jsonstr['message'][m]['url'],'utf-8')
            ehtml = etree.HTML(html)
            try:
                strs = ehtml.xpath('//*[@class="message break-all"]')[-1]
            except:
                pass
            else:
                count+=1
                zcount+=1
                sys.stdout.write('\r'+'此目录已获取：'+str(count)+'篇文章,当前：' +lname+'->'+jsonstr['message'][m]['name'])
                sys.stdout.flush()
                strs = etree.tostring(strs, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
                strs=re.sub('<h[1,2,3,4,5,6,7,8,9, ]','<b ',strs)
                strs = re.sub('</h[1,2,3,4,5,6,7,8,9]>', '</b>', strs)
                strs = re.sub('<img src="upload','<img src="https://bbs.pediy.com/upload',strs)
                strs = re.sub('<img src="/view', '<img src="https://bbs.pediy.com/view', strs)
                strs = re.sub('a href="attach-', 'a href="https://bbs.pediy.com/attach-', strs)
                txt=txt+'<br><br><h'+str(num+1)+'>'+jsonstr['message'][m]['name']+'</h'+str(num+1)+'><br>'+strs
 
def getdata(url):
    global txt,zlist,count
    html=gethtml(url,'utf-8')
    pattern = re.compile('\{ id.*?\}')
    t=pattern.findall(html)
    toplist=[]
    zlist=[]
    for i in t:
        if 'pId: 0 'in i:
            toplist.append(i)
        else:
            zlist.append(i)
    for i in toplist:
        iid,itid,iname=forstr(i)
        zzlist = []
        for j in range(len(zlist), 0, -1):
            jid,jpid,jname=forstr(zlist[j-1])
            if jpid==iid:
                zzlist.append(zlist[j-1])
                zlist.remove(zlist[j-1])
        for j in range(len(zzlist), 0, -1):
            jid, jpid, jname = forstr(zzlist[j - 1])
            mkdir(savepath + filterFName(iname))
            dirname=iname+'->'+jname
            time_start=time.time()
            count = 0
            print('开始获取【'+iname+'->'+jname+'】...')
            txt = ''
            getlv(dirname,zzlist[j-1],2)
            time_end=time.time()
            print('')
            print(iname+'->'+jname+'：获取完成. 文章数：'+str(count)+',耗时：{:.2f} 秒.'.format(time_end - time_start))
            writehtml(savepath + filterFName(iname)+'\\'+filterFName(jname)+'.html', txt)
            print('*' * 100)
 
if __name__ == '__main__':
    global zlist,count,zcount
    count=0
    zcount=0
    url = 'https://www.kanxue.com/chm.htm'
    ztime=time.time()
    savepath='C:\\看雪知识库\\'
    getdata(url)
    print('全部任务完成,共获取文章： '+str(zcount)+' ,总耗时：{:.2f} 秒.'.format(time.time()-ztime))