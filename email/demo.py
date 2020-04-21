from email import encoders
import os
import traceback
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
 
 
 
 
# 中文处理
def _format_addr(s):
    #.parseaddr(address)是模块中专门用来解析邮件地址的函数,返回一个tuple
    name, addr = parseaddr(s)
    #元组拆包  name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
    #formataddr(pair)和parseaddr函数相反，formataddr函数是构建邮件地址的，传入一个tuple，返回str
 
 
def send_email(to_addr_in, filepath_in, userId, user):
    # 邮件发送和接收人配置
    i = 0
    from_addr = ''
    password = ''  # 这是你邮箱的第三方授权客户端密码，并非你的登录密码
    for user,pwd in user.items():
        if i == userId:
            from_addr = user.replace('\r', '').replace('\n', '').replace('\t', '')
            password = pwd.replace('\r', '').replace('\n', '').replace('\t', '')
            break
        i+=1
    smtp_server = 'smtp.163.com'
    to_addr = to_addr_in
    to_addrs = to_addr.split(',')
    msg = MIMEMultipart()
    msg['From'] = _format_addr('群发测试标题 <%s>' % from_addr)  # 显示的发件人
    msg['To'] = ",".join(to_addrs)  # 多个显示的收件人
    msg['Subject'] = Header('群发邮件测试--描述', 'utf-8').encode()  # 显示的邮件标题
    # 需要传入的路径
    # filepath = r'D:\test'
    filepath = filepath_in
    r = os.path.exists(filepath)
    if r is False:
        msg.attach(MIMEText('Hello world,邮件测试！！！\r\n', 'plain', 'utf-8'))
    else:
        # 邮件正文是MIMEText:
        msg.attach(MIMEText('这里是邮件的正文内容！！！\n请查收附件...    \n', 'plain', 'utf-8'))
        # 遍历指定目录，显示目录下的所有文件名
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join(filepath, allDir)
            #print(child.encode('utf-8').decode('gbk'))  # .decode('gbk')是解决中文显示乱码问题
            # 添加附件就是加上一个MIMEBase，从本地读取一个文件
            with open(child, 'rb') as f:
                # 设置附件的MIME和文件名，这里是txt类型:
                mime = MIMEBase('file', 'xls', filename=allDir)
                # 加上必要的头信息:
                mime.add_header('Content-Disposition', 'attachment', filename=allDir)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)
    try:
        server = smtplib.SMTP(smtp_server, 25)
        # server.starttls()
        server.set_debuglevel(1)  # 用于显示邮件发送的执行步骤
        server.login(from_addr, password)
        #print(to_addrs)
        server.sendmail(from_addr, to_addrs, msg.as_string())
        server.quit()
        return 1
    except Exception:
        return -1
 
 
 
 
def read_user(user):
    f = open("mail_user.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    i=1
    username = ''
    pwd = ''
    while line:
        line = line.replace('\r', '').replace('\n', '').replace('\t', '')
        if i%2 != 0:
            username = line
            #print("username=",username)
        else:
            pwd = line
            #print("pwd=", pwd)
            user[username] = pwd
        line = f.readline()
        i+=1
    f.close()
    #print("\n")
    #print(user)
 
if __name__ == '__main__':
    # 账号密码存放
    user = {}
    read_user(user)
    i = 0
    userId = 0
    f = open("to_user.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        i+=1
        line = line.replace('\r','').replace('\n','').replace('\t','')
        if send_email(line, 'test',userId, user) == -1:
            print(i)
            break
        userId += 1  #使用哪个用户ID发送邮件。
        if userId >= len(user):
            userId = 0
        time.sleep(3) #不延迟的话，发送100以上账号就会被停用。
        line = f.readline()
    f.close()