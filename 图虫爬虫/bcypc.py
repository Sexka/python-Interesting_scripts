import requests
import re
 
url = 'https://bcy.net/coser/toppost100'  # 要进行抓取的url
web_url = "https://bcy.net"  # 官方网站
file = 'img/'  # 文件的保存路径最后加反斜杠
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
# 获取抓取数据页面
data = requests.get(url, headers=headers).text
wi_url_id = re.findall('<a href=".*?class="db posr ovf"', data)
# 对抓取图片单独页面url进行遍历
for s in wi_url_id:
    wi_id = web_url + s.lstrip('<a href="').rstrip('" class="db posr ovf"')
    n_data = requests.get(wi_id, headers=headers).text  # 获取单独的图片页面数据
    json_data = re.findall('"{.*?}"', n_data)[0].lstrip('"').rstrip('}}"')
    n_http = re.findall('"path.*?w650', json_data)
    # 对图片url进行遍历
    for b in n_http:
        try:
            img_data = b.lstrip('"path\\":\\"s') + '.image'
            img_url = 'https:/' + img_data.replace('u002F', '').replace('\\\\', '/')
            img = requests.get(img_url, headers=headers).content  # 获取图片数据
            img_name = img_url.rstrip('.jpg~tplv-banciyuan-w650.image')[-31:]  # 获取图片名
            # 对图片进行保存
            with open(file + img_name + '.jpg', 'wb') as f:
                f.write(img)
                print('以保存，图片url：' + img_url)
        except:
            print('保存失败')