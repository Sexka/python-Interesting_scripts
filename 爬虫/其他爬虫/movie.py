#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
r'''
===========================
*     乐队我做东 m3u8     *
===========================
'''
 
import os, sys, urllib, requests, re, random
from lxml import etree
from time import sleep
 
def getWorkdir(subdir):
    if os.name == 'nt':
        #电脑
        workdir = os.path.join('F:\\BaiduNetdiskDownload', subdir)
    elif os.name == 'posix':
        #手机
        workdir = os.path.join('/storage/emulated/0/Download', subdir)
    else:
        workdir = os.path.join(os.getcwd(), subdir)
    if not os.path.exists(workdir):
        os.mkdir(workdir)
    return workdir
 
def getM3U8(p_title):
    print('\n%s' % p_title)
    #解析期页面，得到m3u8链接
    try:
        p_content = requests.get(host_toc+phase_urls[phase_titles.index(p_title)], headers=header, timeout=30).content.decode('utf-8', errors='ignore')
    except:
        print('   ... failed opening phase page ... %s' % host_toc+phase_urls[phase_titles.index(p_title)])
        return
    url_m3u8 = re.findall(r'cms_player = {"yun":true,"url":"(.*?)"', p_content, re.S)[0].replace('\/', '/')
    parsed_flag, m3u8_items, host_m3u8 = reParser_m3u8(url_m3u8)
    if parsed_flag == 'Y':
        getTS(p_title, m3u8_items, host_m3u8)
    else:
        print('   ... failed parsing m3u8 content ... %s' % url_m3u8)
 
def reParser_m3u8(url):
    try:
        m3u8_content = requests.get(url, headers=header, timeout=30).content.decode('utf-8', errors='ignore')
    except:
        return 'N', [], ''
    if re.findall('^(\S+m3u8)$', m3u8_content, re.M):
        #如果有嵌套的m3u8
        sub_url_m3u8 = os.path.split(url)[0] + '/' + re.findall('^(\S+m3u8)$', m3u8_content, re.M)[0]
        return reParser_m3u8(sub_url_m3u8)
    else:
        #解析并返回播放列表（ts文件序列）
        return 'Y', re.findall('^(\S+ts)$', m3u8_content, re.M), os.path.split(url)[0]+'/'
 
def getTS(p_title, m3u8_items, host_m3u8):
    with open(os.path.join(workdir, '%s.txt' % p_title), 'w', encoding='utf-8') as f:
        for ts in m3u8_items:
            f.write(host_m3u8+ts+'\n')
    print('   ... playlist fetched')
    #下载ts文件
    print('   ... downloading ts ... %d files' % len(m3u8_items))
    p_dir = os.path.join(workdir, p_title)
    if not os.path.exists(p_dir):
        os.mkdir(p_dir)
    flag_combine = True
    for ts in m3u8_items:
        try:
            ts_resp = requests.get(host_m3u8+ts).content
        except:
            print('   ... failed reading ts ... %s' % host_m3u8+ts)
            flag_combine = False
        else:
            try:
                with open(os.path.join(p_dir, os.path.split(ts)[1]), 'wb') as f:
                    f.write(ts_resp)
            except:
                print('   ... failed saving ts ... %s' % os.path.split(ts)[1])
                flag_combine = False
    #合并ts文件
    if flag_combine:
        print('   ... combining ts')
        os.chdir(p_dir)
        os.system('copy/b *.ts %s.ts' % p_title)
        print('   ... done')
    else:
        print('   ... pls check failed ts & manually combine\n   ... done')
 
print(__doc__)
 
subdir = 'Band'
workdir = getWorkdir(subdir)
 
headerpool = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36', 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0', 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0', 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0', 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)', 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1', 'Opera/8.0 (Windows NT 5.1; U; en)']
 
header = dict()
header["user-agent"] = random.choice(headerpool)
 
#目录页
url_toc = 'https://www.116bt.com/vodshow/4193.html'
host_toc = urllib.parse.urlsplit(url_toc)[0] + '://' + urllib.parse.urlsplit(url_toc)[1]
 
#解析目录页，得到每期的名字、链接
toc = requests.get(url_toc, headers=header, timeout=30).content.decode('utf-8', errors='ignore')
toc_html = etree.HTML(toc)
phase_urls = toc_html.xpath('//ul[@class="detail-play-list clearfix tab-pane ff-playurl ff-playurl-tab-2 fade"]/li/a/@href')
phase_titles = toc_html.xpath('//ul[@class="detail-play-list clearfix tab-pane ff-playurl ff-playurl-tab-2 fade"]/li/a/@title')
for p_title in phase_titles:
    print(p_title)
phase_titles.append('q')
phase_titles.append('a')
 
#选择要下载的期号
while True:
    phase_chosen = ''
    while phase_chosen not in phase_titles:
        phase_chosen = input('\nWhich one to get? (a)ll? (q)uit? ... ')
    if phase_chosen == 'q':
        sys.exit()
    elif phase_chosen == 'a':
        for p_title in phase_titles:
            getM3U8(p_title)
            sleep(2)
    else:
        getM3U8(phase_chosen)
        sleep(2)