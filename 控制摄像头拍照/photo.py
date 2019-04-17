# -*- coding:utf-8 -*-
#@Auhor : Agam
#@Time  : 2019-04-17
#@Email : agamgn@163.com
import cv2
import smtplib
import sys
import os
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


smtpserver  = 'smtp.163.com'         # smtp服务器
username    = ''    # 发件邮箱账号
password    = ''            # 邮箱登录密码
sender      = ''    # 发件人
addressee   = ''     # 收件人
exit_count  = 5                      # 尝试联网次数
path= os.getcwd()            #获取图片保存路径


def getPicture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(path+'/person.jpg', frame)
    cap.release()



def setMsg():
    msg = MIMEMultipart('mixed')#邮件类型
    msg['Subject'] = '电脑已经启动了哦'#主题
    msg['From'] = ''#发件人
    msg['To'] = addressee#收件人。

    # 邮件的正文
    text = "你的电脑已经开机！照片如下！"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    # 构造图片链接
    sendimagefile = open(path+'/person.jpg', 'rb').read()
    image = MIMEImage(sendimagefile)

    image["Content-Disposition"] = 'attachment; filename="people.png"'
    msg.attach(image)
    return msg.as_string()


def sendEmail(msg):
    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, addressee, msg)
    smtp.quit()


# 判断网络是否联通,成功返回0，不成功返回1
def isLink():
    # return os.system('ping -c 4 www.baidu.com')
    return os.system('ping www.baidu.com')


def main():
    reconnect_times = 0
    while isLink():
        time.sleep(10)
        reconnect_times += 1
        if reconnect_times == exit_count:
            sys.exit()

    getPicture()
    msg = setMsg()
    sendEmail(msg)


if __name__ == '__main__':
    main()