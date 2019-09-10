import  requests
import json
import re
import pandas as pd
 
def  get_msg():
    url="https://h5api.m.taobao.com/h5/mtop.alimama.union.sem.landing.pc.items/1.0/?jsv=2.4.0&appKey=12574478&t=1568021813043&sign=c2a4d2497fc24e077d8f0a0fe63591c2&api=mtop.alimama.union.sem.landing.pc.items&v=1.0&AntiCreep=true&dataType=jsonp&type=jsonp&ecode=0&callback=mtopjsonp1&data=%7B%22keyword%22%3A%22%E5%AE%89%E5%85%A8%E5%A5%97%20%E7%94%B7%22%2C%22ppath%22%3A%22%22%2C%22loc%22%3A%22%22%2C%22minPrice%22%3A%2220%22%2C%22maxPrice%22%3A%22200%22%2C%22ismall%22%3A%22%22%2C%22ship%22%3A%22%22%2C%22itemAssurance%22%3A%22%22%2C%22exchange7%22%3A%22%22%2C%22custAssurance%22%3A%22%22%2C%22b%22%3A%22%22%2C%22clk1%22%3A%22f165a3cac48d521b64f09db3154c2140%22%2C%22pvoff%22%3A%22%22%2C%22pageSize%22%3A%22100%22%2C%22page%22%3A%22%22%2C%22elemtid%22%3A%221%22%2C%22refpid%22%3A%22mm_26632258_3504122_32538762%22%2C%22pid%22%3A%22430673_1006%22%2C%22featureNames%22%3A%22spGoldMedal%2CdsrDescribe%2CdsrDescribeGap%2CdsrService%2CdsrServiceGap%2CdsrDeliver%2C%20dsrDeliverGap%22%2C%22ac%22%3A%224yNrFGXsb1wCAQE%2ByggyM3e5%22%2C%22wangwangid%22%3A%22%22%2C%22catId%22%3A%22%22%7D"
    header = {
            "Referer":"https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=f165a3cac48d521b64f09db3154c2140&keyword=%E5%AE%89%E5%85%A8%E5%A5%97%20%E7%94%B7&minPrice=20&maxPrice=200&spm=a2e15.8261149.07626516001.dsortpricerange",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    }
    response = requests.get(url,headers=header )
    #print(response.content.decode())
    html_str = etree.HTML(response.content.decode())
    #print(html_str)
    dirt =  response.text
    open("爬淘宝01.txt", "w").write(dirt)
 
 
def find_condom():
    str_msg = open("爬淘宝01.txt", "r").read()[len("mtopjsonp1")+1:]
    #print(str_msg)
    str_msg = re.findall(r"(?<=mainItems\":).*(?=},\"ret)",str_msg)
    #print(str_msg)
    str_msg = json.loads(str_msg[0])
 
    main_key= ["loc", "price", "promoPrice","sellCount", "title", "wangwangId"]
    recode = {key:[]  for key in main_key}
 
 
    for item in str_msg :
        for key in main_key:
            recode[key].append(item[key])
 
    f = open("淘宝安全套.txt","w")
    for  i  in range(0, len(str_msg)):
        for  key  in main_key:
            print(recode[key][i],  end="\t\t")
            f.write(str(recode[key][i]))
            f.write("\t\t")
        print()
        f.write("\n")
    f.close()
 
 
if __name__=="__main__":
   #get_msg()
   find_condom()