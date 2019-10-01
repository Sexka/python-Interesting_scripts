import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import time

#
#reload(sys)
#sys.setdefaultencoding('utf-8')


def pp(text):
    print text.encode('utf-8').decode('utf-8')

cookie = {"Cookie": 'INPUT YOUR COOKIE HERE'}
#url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

def getIdFromStag(stags, ids = {}):
    # url for search
    for stag in stags:
        m = 0
        flag = 0
        while m < 51:
            pageId = m
            print 'Loading PAGE', pageId, 'of Stag', urllib.unquote(stag)
            try:
                url = 'https://weibo.cn/search/user/?keyword=%s&sort=0&filter=stag&page=%d' % (stag, pageId)
                html = requests.get(url, cookies=cookie).content

                soup = BeautifulSoup(html, 'lxml')
                content = soup.find_all('a', href=re.compile(r'f=search', re.I))
                for i in range(len(content)):
                    item = content[i]
                    toAppend = item['href'].split('?')[0]
                    if toAppend in ids:
                        ids[toAppend] += 1
                    else:
                        ids[toAppend] = 1
                #time.sleep(1)
                if len(content) <= 0:
                    sys.stdout.write('\rWarning 047: len(content) = 0\t%d page, %s stag\t\t' % (m, urllib.unquote(stag)))
                    time.sleep(20)
                    if flag>=50:
                        m += 1
                        flag = 0
                        continue
                    flag += 1
                    continue
                m += 1
                flag = 0
            except:
                break
                time.sleep(1000)
                if flag:
                    m += 1
                    flag = 0
                    continue
                flag = 1
                continue
    return ids


def getUidFromOid(oid):
#    print 'Loading uid: oid=', oid
    url = 'https://weibo.cn%s' % oid
    html = requests.get(url, cookies=cookie).content

    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all('a', href=re.compile(r'/operation', re.I))[0]
    uid = content['href'].split('/')[1]
    return uid


def getStagFromUid(uid):
    url = 'https://weibo.cn/account/privacy/tags/?uid=%s&st=789d9e' % uid
    html = requests.get(url, cookies=cookie).content

    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all('a', href=re.compile(r'keyword', re.I))
    stags = []
    for item in content:
        istag = item['href'].split('=')[1].split('&')[0]
        stags.append(istag)
    return stags


def getUidsFromOids(oids, num=0, type=1):
    uids = []
    i = 0
    flag = 0
    while i < len(oids):
        if type:
            oid = oids[i]
        else:
            oid = oids[i][0]
        try:
            if i >= num:
                uid = getUidFromOid(oid)
                uids.append(uid)
#                time.sleep(1)
                sys.stdout.write('\rLoading %d-th Uid, oid = %s\t\t\t\t\t' % (i, oid))
            i += 1
            flag = 0
        except IndexError:
            if flag:
                sys.stdout.write('\rWarning 091, oid =%s %d/1000, trying to reconnect %d\t\t\t\t\t' % (oid, i, flag))
            time.sleep(50)
            if flag >= 100:
                sys.stdout.write('\nError 118, oid =%s %d/1000, Connection Failed\n' % (oid, i))
                i += 1
                flag = 0
                continue
            flag += 1
            continue
    return uids


def allStags(uids):
    stags = {}
    flag = 0
    for uid in uids:
        try:
            flag += 1
            uid = uid.split('\n')[0]
            stag = getStagFromUid(uid)
            #time.sleep(1)
            print 'Loading From Uid', uid, 'Number', flag
            for item in stag:
                if item in stags:
                    stags[item] += 1
                else:
                    stags[item] = 1
        except:
            continue
    return sorted(stags.iteritems(), key=lambda d: d[1], reverse=True)


def unquoteStag(stags):
    output = []
    for item in stags:
        t = item[0]
        output.append(urllib.unquote(t))
    return output


def getFollowPages(uids):
    toReturn = []
    i = 0
    flag = 0
    while i < len(uids):
        uid = uids[i]
        try:
            url = 'https://weibo.cn/%s/follow' % uid
            html = requests.get(url, cookies=cookie).content

            selector = etree.HTML(html)
            pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            toReturn.append((uid, pageNum))
            i += 1
            sys.stdout.write('\rLoaded %d-th uid, %d Pages.\t\t\t\t\t' % (i, pageNum))
            flag = 0
        except:
            if html:
                toReturn.append((uid, 0))
                i += 1
                sys.stdout.write('\rLoaded %d-th uid, %d Pages.\t\t\t\t\t' % (i, pageNum))
                flag = 0
                continue
            if flag:
                sys.stdout.write('\rWarning 172, uid =%s %d/1000, trying to reconnect %d\t\t\t\t\t' % (uid, i, flag))
            time.sleep(50)
            if flag >= 40:
                sys.stdout.write('\nError 175, uid =%s %d/1000, Connection Failed\n' % (uid, i))
                i += 1
                flag = 0
                continue
            flag += 1
            continue
    return toReturn


def getFollowRalationship(followPagedUid):
    ids = []
    m = 0
    flag = 0
    while m < len(followPagedUid):
        uid, pages = followPagedUid[m]
        if pages == 0:
            pages = 1
        pageId = 1
        while pageId <= pages:
            try:
                url = 'https://weibo.cn/%s/follow?page=%d' % (uid, pageId)
                html = requests.get(url, cookies=cookie).content

                soup = BeautifulSoup(html, 'lxml')
                content = soup.find_all('a', text="关注他"or"关注她")
                for i in range(len(content)):
                    item = content[i]
                    followed = item['href'].split('=')[1].split('&')[0]
                    # (uid, item) means uid follows item
                    ids.append((uid, followed))
                if not html:
                    sys.stdout.write('\rWarning 047: Account Banned, trying to reconnect %d' % flag)
                    time.sleep(20)
                    if flag >= 50:
                        sys.stdout.write('\nError 175, uid =%s PageId= %d, %d/%d, Connection Failed\n' % (uid, pageId, m, len(followPagedUid)))
                        pageId += 1
                        flag = 0
                        continue
                    flag += 1
                    continue
                pageId += 1
                flag = 0
                sys.stdout.write('\rLoaded %3d-th uid, Page %d/%d...\t\t\t\t' % (m+1, pageId-1, pages))
            except:
                if flag:
                    sys.stdout.write('\rWarning 172, uid =%s PageId= %d %d/1000, trying to reconnect %d\t\t\t\t\t' % (uid, pageId, m, flag))
                time.sleep(20)
                if flag >= 50:
                    sys.stdout.write('\nError 175, uid =%s PageId= %d, %d/1000, Connection Failed\n' % (uid, pageId, m))
                    pageId += 1
                    flag = 0
                    continue
                flag += 1
                continue
        m += 1
    return ids

def weiboContent(uid, pages=20, uidnum=0):
    flag = 0
    toReturn = []
    page = 0
    while page <= pages:
        try:
            url = 'https://weibo.cn/u/%s?page=%d' % (uid, page+1)
            html = requests.get(url, cookies=cookie).content

            soup = BeautifulSoup(html, 'lxml')
            content = soup.find_all('span', {'class': 'ctt'})
            if page == 0 and len(content) >= 3:
                content = content[3:len(content)]
            for i in range(len(content)):
                toReturn.append([uid, page*10+i+1, content[i].getText()])
            if not html:
                sys.stdout.write('\rWarning 251: Account Banned, trying to reconnect %d, uid %d/1000, page %d/20' % (flag, uidnum, page))
                time.sleep(20)
                if flag >= 50:
                    sys.stdout.write('\nError 254, uid =%s Page= %d, %d/1000, Connection Failed\n' % (uid, page, uidnum))
                    page += 1
                    flag = 0
                    continue
                flag += 1
                continue
            page += 1
            flag = 0
            sys.stdout.write('\rLoaded %3d-th uid, Page %d/%d...\t\t\t\t' % (uidnum, page, pages))
        except:
            if flag:
                sys.stdout.write('\rWarning 265, uid =%s Page= %d %d/1000, trying to reconnect %d\t\t\t\t\t' % (uid, page, uidnum, flag))
            time.sleep(20)
            if flag >= 50:
                sys.stdout.write('\nError 268, uid =%s PageId= %d, %d/1000, Connection Failed\n' % (uid, page, uidnum))
                page += 1
                flag = 0
                continue
            flag += 1
            continue
    return toReturn

def writeContent(uids, text):
    start = False
    try:
        f = open(text, 'r')
        for line in f:
            pass
        contentNum = int(line.split('\t')[1])
        startUid = line.split('\t')[0]
        f.close()
    except:
        contentNum = 0
        startUid = uids[0]
    f = open(text, 'a')
    for i in range(len(uids)):
        if start is True:
            t = weiboContent(uids[i], uidnum=i+1)
            for item in t:
                f.write('%s\t%d\t%s\n' % (item[0], item[1], item[2].encode('utf-8')))
        if uids[i] == startUid:
            start = True
            sys.stdout.write('Started! uid = %s, content %d/200' % (startUid, i+1))
            t = weiboContent(uids[i], uidnum=i+1)
            for item in t:
                    if item[1] >= contentNum:
                        f.write('%s\t%d\t%s\n' % (item[0], item[1], item[2].encode('utf-8')))
    f.close()
    return
f = open('testContent2.txt', 'r')
i=0
for line in f:
    print line
    i+=1
    if i%50==0:
        time.sleep(2)
