from os import path
from PIL import Image
import numpy as np
import jieba
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plt 
import matplotlib

d=path.dirname(__file__)

matplotlib.rcParams['font.sans-serif']=['SimHei']  #使用指定的汉字字体类型（此处为黑体）
text=open(path.join(d,'aaa.txt'), encoding='UTF-8').read()
image=np.array(Image.open('wc.jpg')) 

# 字体
font=r'C:\\Windows\\fonts\\simhei.ttf' 
# 停用字
sw = set(STOPWORDS) 
sw.add("转发内容")
sw.add("发布时间")
sw.add("转发理由")
sw.add("原始用户")
sw.add("转发微博")
sw.add("转发微博已被删除")
sw.add("发起的投票")
sw.add("大家都在抢")
sw.add("让红包飞")
sw.add("的红包")
sw.add("微博红包雨来袭")
sw.add("最高可得2018元")
sw.add("财神卡2018")
sw.add("手慢无")
sw.add("来荒野行动吃鸡领红包")
sw.add("集齐全套财神卡")
sw.add("现金兑换百分百")
sw.add("红包雨每场限时开启半小时")
sw.add("我要开启财神卡交换大法")
sw.add("我用超6的手速抢到了财神卡")
sw.add("变身土豪就靠它")
sw.add("赶紧来和我交换吧")
sw.add("速速到微博首页深度下拉开抢吧")

# 词频统计
import re
object_list = []
pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式
string_data = re.sub(pattern, '', text) # 将符合模式的字符去除

remove_words = [u'[',u']',u'【',u'】',u'转发',u'内容', u'，',u'发布时间', u'转发理由', u'\xa0', u'原始', u'转发微博已被删除',u'发起的投票',u'大家都在抢',u'让红包飞',u'。',u' ',u'、',u'cn',u'现金',u'最高可得2018元',
                u'用户',u'\n',u'红包',u'财神卡2018',u'的',u'…',u'！',u'/',u'转发',u':',u'-',u'#',u'时间',u'@',u'发布'
,u'“',u'”',u'？',u'《',u'》',u'：',u'～',u'http',u'_',u'~',u'##',u'（',u'）',u'了'
                ] # 自定义去除词库
seg_list_exact = jieba.cut(string_data, cut_all = False) # 精确模式分词
for word in seg_list_exact: # 循环读出每个分词
    if word not in remove_words: # 如果不在去除词库中
        object_list.append(word) # 分词追加到列表

import collections
word_counts = collections.Counter(object_list) # 对分词做词频统计
word_counts_top10 = word_counts.most_common(15) # 获取前15最高频的词
print (word_counts_top10) # 输出检查


# 饼图
# plt.pie([i[1] for i in word_counts_top10],labels =[labels [0] for labels  in word_counts_top10],autopct='%1.1f%%',
# 		explode=(0.1, 0, 0, 0,0, 0,0, 0,0, 0,0, 0,0, 0,0)
# 	)
# plt.title("微博前15最高频的词")
# plt.show()





# mask = np.array(Image.open('wc.jpg')) # 定义词频背景
# wc =WordCloud(
#     font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
#     mask=mask, # 设置背景图
#     max_words=50, # 最多显示词数
#     max_font_size=100, # 字体最大值
#     scale=20,
#     random_state=20
# )

# wc.generate_from_frequencies(word_counts) # 从字典生成词云
# image_colors = ImageColorGenerator(mask) # 从背景图建立颜色方案
# wc.recolor(color_func=image_colors) # 将词云颜色设置为背景图方案
# plt.imshow(wc) # 显示词云
# plt.axis('off') # 关闭坐标轴
# plt.show() # 显示图像




wordcloud=WordCloud(max_font_size=60,max_words = 50,background_color='white',mask=image,font_path=font,stopwords=sw,scale=20,random_state=20).generate(text)
plt.imshow(wordcloud,interpolation="bilinear")
plt.axis("off")
plt.show()
