from flask import Flask, request
import pymysql
from flask import jsonify
import logging
from logging import handlers

app = Flask(__name__)
host=""
name=""
password=""
database=""
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)



@app.route('/')
def hello_world():
    return '<h1>查询地址:<a href="/find">find</a></h1>'

@app.route("/add")
def add():
    return "ok"

@app.route("/find")
def find():
    print(request.remote_addr)
    print(request.full_path)
    log = Logger('all.log', level='debug')
    log.logger.info('ip:'+request.remote_addr+",path"+request.full_path)
    dicts = {}
    lists=[]
    find_name=request.args.get("name")
    if find_name!=None:
        datas=find_by_name(find_name)
        if len(datas)==0:
            return "暂无收录，请自行决定，或者添加"
        for data in datas:
            dicts['地址'] = data[2]
            dicts['公司名字']=data[1]
            dicts['类型'] = data[4]
            lists.append(dicts)
            dicts={}
    find_address = request.args.get("address")
    if find_address!=None:
        datas = find_by_address(find_address)
        if len(datas)==0:
            return "暂无收录，请自行决定，或者添加"
        for data in datas:
            dicts['地址'] = data[2]
            dicts['公司名字'] = data[1]
            dicts['类型'] = data[4]
            lists.append(dicts)
            dicts = {}

    if find_name==None and find_address==None:
        return "请输入正确的url参数<br>" \
               "find?name='''<br>" \
               "find?address='''<br>" \
               "find?name='''&address='''<br>" \
               "find?address='''&name='''<br>"
    return jsonify(lists)



def connect():
     # 连接mysql字符串
    db = pymysql.connect(host,name, password, database)
    # 新建游标
    cursor = db.cursor()
    return cursor

def find_by_name(name):
    cursor=connect()
    # 执行sql语句
    cursor.execute("select * from data where name='{0}'".format(name))
    data = cursor.fetchall()
    return data

def find_by_address(address):
    cursor=connect()
    # 执行sql语句
    cursor.execute("select * from data where address LIKE '%{0}%'".format(address))
    data = cursor.fetchall()
    return data



if __name__ == '__main__':
    app.run(debug=True)
