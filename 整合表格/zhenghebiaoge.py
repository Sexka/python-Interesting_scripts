import pandas as pd
import numpy as np
import os,csv,sys
 
adr = os.path.dirname(os.path.realpath(sys.argv[0]))#获取当前文件所在目录   __file__和realpath的差别，https://blog.csdn.net/qq_41817302/article/details/88684703
file_list =[]
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):#files:当前路径下所有非目录子文件。root，当前目录路径。dirs：当前目录下的所有子目录
        for file in files:#遍历当前路径下所有非目录子文件
            if os.path.splitext(file)[1] == '.xlsx':#通过splitext把后缀跟名字分开，以列表格式，判断你要的格式，然后把路径加入进列表
                file_list.append(os.path.join(root,file))
    return file_list#返回列表
file_name(adr)
 
print('是否整合以下所有表格：')
for a in file_list:
    print(a)#打印当前文件夹的所有xlsx文件路径
print(input('任意键继续'))
excel_num = pd.ExcelFile(file_list[0])#读取列表里的第0个路径，使用sheet_name获取工作表数量
header_data = pd.read_excel(file_list[0],sheet_name=len(excel_num.sheet_names)-1,header=0)#读取文件
tr_header = header_data.columns#使用colunms获取每一列的列名
header_list =np.array(tr_header).tolist()#使用tolist转化成列表
#print(header_list)
f = open('汇总.csv','a',newline='',encoding='utf-8')  #创建一个汇总表格
write = csv.writer(f)  #实例化对象
write.writerow(header_list)
 
for i in file_list:
    excel = pd.ExcelFile(i)  #实例化对象通过ExcelFile 获取下列sheet的个数，直接使用excel.sheet_names可以获取sheet名字
    read_file = pd.read_excel(i,sheet_name=len(excel.sheet_names)-1,header = 0)  #通过read_excel读取，i 是路径 ，sheet_name是要打开的工作簿，可以是工作簿名字，也可以是索引，col确定标签行
    #print(read_file)
    #number = read_file.shape[0]-1
    #read_file.drop([number],inplace=True,axis=0) #删除标签行里指定字符的行，axis=0为行，1为列，inplace为重新赋值
    tr_read_file = np.array(read_file)  #通过array以及tolist把DF转化为list
    read_list = tr_read_file.tolist()
    print(read_list)
 
    for i in read_list:  #把获取到的数据写入
        write.writerow(i)
f.close()  #关闭表格