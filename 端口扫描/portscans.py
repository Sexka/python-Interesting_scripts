# -*- coding:utf-8 -*-
#@Auhor : Agam
#@Time  : 2019-06-18
#@Email : agamgn@163.com
import sys
import socket


# 端口扫描py脚本<主机>,开始端口至末尾端口

class scan():
    # 定义打开、关闭的端口list
    host_port_open = list()
    host_port_close = list()

    def __init__(self, host_str, start_port, end_port):
        self.host_str = host_str
        self.start_port = int(start_port)
        self.end_port = int(end_port)

    def main_head(self):
        ## 遍历 用户传入的参数 起止端口
        for tmp in range(self.start_port, self.end_port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # 如果检测端口打开,则执行
                s.connect((self.host_str, tmp))
                s.shutdown(2)
                print('%s：%d is open ' % (self.host_str, tmp))
            except:
                # 如果检测端口关闭,则执行
                print('%s：%d is close ' % (self.host_str, tmp))

def main():
    # 获取用户输入的字符长度
    if len(sys.argv) == 4:
        try:
            host_ip = sys.argv[1]
            start_port = int(sys.argv[2])
            end_port = int(sys.argv[3])
        except Exception as ret:
            print("端口输入错误。。。。。")
            return
    else:
        print("请按照以下方式运行:")
        print("python3 xxxx.py host_ip start_port end_port")
        return
    print(host_ip, start_port, end_port)
    scaning = scan(host_ip, start_port, end_port)
    scaning.main_head()

if __name__ == "__main__":
    main()
