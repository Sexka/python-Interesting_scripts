def main(html):
    bb=req(html)
    soup = BeautifulSoup(bb.text, 'lxml')
    b=soup.find('div',class_='tab_box').find_all('a')
    for j in b:
        images = []
        a1 = j['href']
        a2 = j['title']
        page = req(a1)
        zz = re.findall(r'<h1.*?<em>(.*?)</em>', page.text)[0]
        poj = 'F:\meizhuo\\' + a2
        if os.path.exists(poj):
            print('目录已存在')
            pass
        else:
            print('目录不存在，新建目录{}'.format(poj))
            os.mkdir(poj)
            os.chdir(poj)
            try:
                for k in range(1, int(zz) + 1):
                    all = a1[0:-5] + '_' + str(k) + '.html'
                    alll = req(all)
                    dow = BeautifulSoup(alll.text, 'lxml')
                    image = dow.find('img', class_='pic-large')['src']
                    images.append(image)
            except:
                pass
            print('下载好了', a2)
            print(images)
            pool = Pool(4)
            pool.map(down, images)
            pool.close()
            pool.join()
 
if __name__ == '__main__':
    zpoj='F:\meizhuo'
    if os.path.exists(zpoj):
        print('总目录已存在')
        pass
    else:
        print('总目录不存在，新建总目录{}'.format(zpoj))
        os.mkdir(zpoj)
        os.chdir(zpoj)
    #每个主题只有5页的壁纸，可以自行修改想要下载的主题的网址
    for i in range(1,6):
        html = 'http://www.win4000.com/zt/meitui_'+ str(i) + '.html'
        main(html)