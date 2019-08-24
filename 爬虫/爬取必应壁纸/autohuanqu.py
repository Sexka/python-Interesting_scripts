import ctypes
import time
import requests
import os
from threading import Thread
from tkinter import Tk, Label, Button,Entry,StringVar,messagebox
# r'C:\Users\86156\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
# '放到AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup下把本文件后缀设为pyw 就会开机自启'
class Bz(object):
    def __init__(self):
        self.curent_url = 'https://tenapi.cn/img/acg.php'
        self.root = Tk()
        self.root.attributes("-alpha", 0.8)
        self.root.title('壁纸切---by wyc--->吾爱17788210295')
        self.root.geometry('218x55+1300+20')
        self.b1 = Button(self.root, text=' 换一类 ', command=self.change_type, fg='#00f235',width=8).place(x=0, y=0)
        self.b2 = Button(self.root, text='下一张>>  频率(分)', command=self.change_next, fg='blue',width=22).place(x=63, y=0)
        self.b3 = Button(self.root, text='停止切换', command=self.stop, fg='red', width=8).place(x=0, y=30)
        self.label = Label(self.root, text='二次元',fg='#9e3dff')
        self.label.place(x=85, y=30)
        e = StringVar()
        self.input=Entry(self.root,textvariable=e,fg='#ffaf0a')
        e.set(0.1)       #默认0.1分钟   6s
        self.input.place(x=153, y=30)
        self.url_list = {1: ['影视', 'http://pic.tsmp4.net/api/yingshi/img.php'],
                         2: ['随机', 'http://lorempixel.com/1920/1080/'],
                         3: ['女神', 'http://pic.tsmp4.net/api/nvsheng/img.php'],
                         4: ['风景', 'http://pic.tsmp4.net/api/fengjing/img.php'],
                         5: ['二次元', 'https://tenapi.cn/img/acg.php']}
        self.path = 'D:\壁纸'
        self.filepath = self.path + '/img.jpg'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.flag = True
        self.start = 1
 
    def stop(self):
        self.flag = False
 
    def change_type(self):
        if self.start > 5:
            self.start = 1
        list = self.url_list.get(self.start)
        curent_type = list[0]
        self.curent_url = list[1]
        self.label['text'] = curent_type
        self.start += 1
 
    def change_next(self):
        data = requests.get(url=self.curent_url).content
        with open(self.filepath, 'wb') as f:
            f.write(data)
        self.config()
 
    def get_img(self):
        try:
            self.num = eval(self.input.get()) * 60  #捕获结束界面后的异常
        except Exception:
            pass
        try:
            data = requests.get(url=self.curent_url).content
            with open(self.filepath, 'wb') as f:
                f.write(data)
            time.sleep(self.num)       # 睡眠单位秒
            self.config()
        except Exception:
            pass
 
    def config(self):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, self.filepath, 0)  # 设置桌面壁纸.
 
    def img(self):
        while self.flag:
            self.get_img()
 
    def run(self):
        t1 = Thread(target=self.img)
        # t1.setDaemon(True)           #设置守护线程 --->是否完全关闭
        t1.start()
        self.root.mainloop()
        if self.flag:
            root = Tk()
            root.withdraw()
            messagebox.showinfo("by Wyc", "只关闭了界面! 图片还在切换! 请进入任务管理器结束进程")
if __name__ == '__main__':
    b = Bz()
    b.run()