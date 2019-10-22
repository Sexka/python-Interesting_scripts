'''
        多进程实现复制文件
    步骤：
        （1）获得源文件夹路径；
        （2）获取源文件夹下各文件的文件名
        （3）获得目标文件夹
        （4）复制文件
 
    知识点：
        （1）os模块：
            1>listdir(path),得到路径path下的所有文件夹名和文件名。（只有一层）
            2>mkdir(path),新建该路径的文件夹
        （2）multiprocess 多进程
            1>Pool()   进程池
            2>Manger().Queue()  队列（进程通信）
 
 
         2019年10月22日
'''
 
 
import multiprocessing
import os
import time
#1得到复制的文件夹名
def get_old_folder_name():
    old_folder_name =  input("请输入复制目录:")
    return old_folder_name
 
 
#2得到文件夹下的文件名
def get_file_names( folder ):
     file_names = os.listdir(folder)
     return file_names
 
 
#3新建文件夹
def creat_folder():
    new_folder_name = input("请输入新的文件夹名:")
    try:
        os.mkdir(new_folder_name)
    except:
        pass
    return  new_folder_name
 
 
#4复制文件到指定文件夹下
def copy_file(file_name, old_folder_name, new_folder_name,queue):
    try:
        #不知道文件类型，直接使用二进制读取。
        old_f = open(old_folder_name+"/"+file_name, "rb")
        read_str = old_f.read()
        old_f.close()
 
        new_f = open(new_folder_name +"/" + file_name, "wb")
        new_f.write(read_str)
        new_f.close()
    except:
        pass
    #避免”复制“文件夹而产生的文件数量不够，程序不能结束
    queue.put(1)
    #time.sleep(1)没有实际作用，只是为了看进度条的效果
    time.sleep(1)
 
#5主函数
def  main(queue):
    old_folder_name = get_old_folder_name()
    print("原文件夹： ",old_folder_name)
    file_names =  get_file_names(old_folder_name)
    print("文件数量： ",len(file_names))
    new_folder_name = creat_folder()
    print("新文件夹：  ",new_folder_name)
    for  item in file_names :
        pool.apply_async(copy_file, (item,old_folder_name,new_folder_name ,queue))
 
    pool.close()
    file_num = 0
    file_sum = len(file_names)
    while True:
        if not queue.empty():
            queue.get()
            file_num+=1
            print("\r",end="")
            print("▓"*int(file_num/file_sum *50), end="")
            print("  已完成 %.2f%%" % (file_num/file_sum*100), end="")
        if file_num == file_sum:
            print()
            break
    print("复制完成！")
 
#5函数入口
if __name__ == "__main__":
    pool  = multiprocessing.Pool(5)
    queue = multiprocessing.Manager().Queue()
 
    main(queue)