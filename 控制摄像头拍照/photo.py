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


smtpserver  = 'smtp.163.com'         # smtp������
username    = ''    # ���������˺�
password    = ''            # �����¼����
sender      = ''    # ������
addressee   = ''     # �ռ���
exit_count  = 5                      # ������������
path= os.getcwd()            #��ȡͼƬ����·��


def getPicture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite(path+'/person.jpg', frame)
    cap.release()



def setMsg():
    msg = MIMEMultipart('mixed')#�ʼ�����
    msg['Subject'] = '�����Ѿ�������Ŷ'#����
    msg['From'] = ''#������
    msg['To'] = addressee#�ռ��ˡ�

    # �ʼ�������
    text = "��ĵ����Ѿ���������Ƭ���£�"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    # ����ͼƬ����
    sendimagefile = open(path+'/person.jpg', 'rb').read()
    image = MIMEImage(sendimagefile)

    image["Content-Disposition"] = 'attachment; filename="people.png"'
    msg.attach(image)
    return msg.as_string()


def sendEmail(msg):
    # �����ʼ�
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com')
    smtp.login(username, password)
    smtp.sendmail(sender, addressee, msg)
    smtp.quit()


# �ж������Ƿ���ͨ,�ɹ�����0�����ɹ�����1
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