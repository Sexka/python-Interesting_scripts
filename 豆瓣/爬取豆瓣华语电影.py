import  requests
import  json
from  lxml import etree
 
def  get_message(start_page):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=recommend&page_limit=20&page_start={}".format(start_page)
    header ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
             "Upgrade-Insecure-Requests": "1",}
    response = requests.get(url,headers= header)
    html_str = response.text
    #得到的数据直接是json数据，所以直接处理
    str = json.loads(html_str)
    #返回列表数据
    return str["subjects"]
 
def  save(record):
    with open("国语电视剧.txt","w",encoding="utf-8") as f:
        for  i  in range(len(record)):
            f.write("\n"+str(i+1)+"、")
            f.write(str(record[i]))
            print(record[i])
 
    print("保存结束！")
 
 
if __name__ == "__main__":
     start_page = 0
     record=[]
     #网页start_page最大为 220
     while start_page<=220:
        #1.得到数据；
        channel_list = get_message(start_page)
        #2.追加数据；
        record.extend(channel_list)
        #extend把列表数据按照列表元素添加到列表中
        start_page+=20
     #3.简单处理：按照评分从高到底排序，sorted临时排序
     record = sorted(record,key=lambda keys:keys['rate'],reverse=True)
     #4.数据保存
     save(record)