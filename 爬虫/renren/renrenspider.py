def analyze(u):
    try:
        url = baseurl + u
        html = pq(requests.get(url, headers=headers).content.decode())
        # 获取标题和剧种
        t = html(".resource-tit h2").text()
        title = re.search("【(.*)】《(.*)》", t).groups()
        # 获取影视分级
        items = html('.level-item img').attr('src')
        level = get_level(items, info["level"])
        # 如果返回的分级为false则跳过这条
        if level == False: return
        # 获取主要信息
        main_info = get_info(html)
        # 获取剧种
        if "dramaType" in result_info:
            main_info["dramaType"] = title[0]
        # 获取评分
        if "score" in result_info:
            main_info["score"] = get_score(u[-5:])
        if 'url' in result_info:
            main_info['url'] = url
        # 获取影片封面
        if "imgurl" in result_info:
            main_info['imgurl'] = html('.imglink a').attr('href')
        # 获取本站排名
        if "rank" in result_info:
            main_info["rank"] = re.search("本站排名:(\d*)", html(".score-con li:first-child .f4").text()).group(1)
        # 获取简介
        if "introduction" in result_info:
            main_info["introduction"] = html(".resource-desc .con:last-child").text()
        result = {}
        # 写入标题和分级
        result["title"] = title[1]
        result["level"] = level
        # 遍历main_info,只写入有效数据
        for key, value in result_info.items():
            try:
                result[key] = main_info[key]
            except:
                result[key] = '暂无'
 
        print(result['title'])
        # 写入文件
        if export == 'csv':
            wirtecsv([i for i in result.values()])
        else:
            mycol.insert_one(result)
    except Exception as e:
        throw_error(e)
        analyze(u)
 
 
def main(num):
    try:
        url = baseurl + "/resourcelist/?page={}".format(num)
        doc = pq(requests.get(url, headers=headers).content.decode())
        urls = doc(".fl-info a").items() #遍历a标签
        if info['threads']:
            for i in urls:
                Thread(target=analyze,args=(i.attr("href"),)).start()
        else:
            for i in urls:
                analyze(i.attr("href"))
        time.sleep(1)
    except Exception as e:
        throw_error(e)
        main(num)