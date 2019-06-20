import requests
import lxml.etree
from time import sleep
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    # ",referer": "https://www.mzitu.com/tag/ugirls/"
}


# ��ȡҳ������
def getpage(url):
    # 1 ��������
    response = requests.get(url, headers=headers)
    # 2 �����xml�ĵ�
    xml = lxml.etree.HTML(response.text)
    # 3 ��ȡ��Ҫ��element �����ǻ�ȡ����Ϊpage��div��ǩ�µ�span��ǩ������ ��ȡ��������Ϊ��1 / 99
    page = xml.xpath(
        '//div[@class="page"]/span')  # <div class="page"><a href="/">��һҳ</a><span>1 / 99</span><a href="/?p=2">��һҳ</a></div>
    # 4 ͨ�����ַ����ָ��������ȡ��Ӧ��ֽ��ҳҳ��
    str = page[0].text.split(' ')[2]
    return (int)(str)


# ����ҳ��
def foreachurlpages(url, page, pages, path):
    i = page
    while i <= pages:
        temp = url + "?p={i}".format(i=i)
        print("��{page}ҳ��ʼ���أ���ǰҳurl��{url}".format(page=i, url=temp))
        count = foreachImage(temp, path)
        print("��{page}ҳ���������".format(page=i))
        i = i + 1
        if (count == 0):
            print("������ִ��󣬵�{page}ҳ��������")
            i = i - 1
        os.system('cls')


def foreachImage(url, path):
    response = requests.get(url, headers=headers)
    xml = lxml.etree.HTML(response.text)
    imgname = xml.xpath('//div[@class="description"]/h3')
    imgurl = xml.xpath('//div[@class="card progressive"]/img')
    print("��ǰҳ����{}�ű�ֽ".format(len(imgurl)))
    count = 0
    for n, u in zip(imgname, imgurl):
        name = n.text.split(' ')[0]
        url = u.xpath('@src')[0]
        count += 1
        print("��{}�ű�ֽ ������{}  ��ֽurl��{}".format(count, name, url))
        download(name, url, path)
    return count


def download(name, url, path):
    response = requests.get(url, headers=headers)  # �����棬ģ��������ύ
    NAME = ""
    for i in range(len(name)):
        if name[i] not in '/\*:"?<>|':
            NAME += name[i]
    filename = path + '\\' + NAME + ".jpg"
    with open(filename, "wb") as f:
        f.write(response.content)
        f.close()


if __name__ == '__main__':
    url = "https://bing.ioliu.cn/"  # ��ֽ��ҳurl
    pages = getpage(url)  # ��ȡҳ������������ת��Ϊint����
    print("��ֽ��ҳ����{pages}".format(pages=pages))  # ��ӡ��Ӧ��ֽҳ��
    path = input("����ͼƬ�洢·����")
    page = (int)(input("�ӵڼ�ҳ��ʼ���أ�1-{}����".format(pages)))
    if page <= 0 or page > pages:
        print("ҳ�����ڷ�Χ��")
        print("3����˳�")
        sleep(1)
        print("2����˳�")
        sleep(1)
        print("1����˳�")
        sleep(1)
    else:
        foreachurlpages(url, page, pages, path)
        print("�������")
        print("3����˳�")
        sleep(1)
        print("2����˳�")
        sleep(1)
        print("1����˳�")
        sleep(1)
