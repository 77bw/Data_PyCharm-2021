from flask import Flask
from flask import request  #获取参数
from flask import render_template  #引用flask的模板
import utils
from flask import jsonify #返回json数据
import string
import decimal
from jieba.analyse import extract_tags

#创建一个 flask实例
app=Flask(__name__)
#1. 构建最简单路由
@app.route("/") #我们使用route()装饰器来告诉flask触发函数url.,返回两种结果一个字符串，一个是整个页面
def hello_word(): #返回字符串
    return render_template("main.html")  #使用render_template模板返回main.html的页面
#2.构建一个复杂一点页面元素，复制一个路由,
@app.route("/ab")
def hello_word1(): #返回包含页面元素
    # format字符串格式
    return f"""   
    <form>
        账号：<input ><br>
        密码：<input>
    </form>
     """
#3. 传递参数，需要引入包：from flask import request
@app.route("/abc")
def hello_word2(): #返回包含页面元素
    id=request.values.get("id") #使用flask的request的get传递参数
    return f"""
    <form action="/login">
        账号：<input name="name" value="{id}"><br>
        密码：<input name="pwd">
        <input type="submit">
    </form>
     """
#再定义一个login的路由
@app.route("/login") #我们使用route()装饰器来告诉flask触发函数url.,返回两种结果一个字符串，一个是整个页面
def hello_word3(): #返回字符串
    name=request.values.get("name")
    pwd=request.values.get("pwd")
    print(f'name:{name},pwd:{pwd}')
    return f"name={name},pwd={pwd}"
#4. 使用render_template返回一个模板页面，导入包from flask import render_template
#构建一个index.html页面，然后再定义一个路由
@app.route("/tem") #我们使用route()装饰器来告诉flask触发函数url.,返回两种结果一个字符串，一个是整个页面,增加请求方式
def hello_word4(): #返回字符串
    return render_template("index.html") #返回一个模板

#5. 我们如果需要局部的变化而不是整个页面，就用ajiax发送异步请求，这里需要jquery框架，方便写ajiax代码
#在html里面引入jquery.编写ajiax请求代码。
#回到我们的后台编写py定义路由
@app.route('/ajax',methods=["get","post"])
def hell_world5():
    name=request.values.get("name")
    score=request.values.get("score")
    print(f"name:{name},score:{score}")
    return '10000'
#6.我们定义一个时间路由(与ajax的url一致)，然后定义一个方法，用它调用显示时间函数。
#我们再新建一个工具类utils.py放我们编写的工具接口等。
@app.route('/time',methods=["get","post"])
def get_time():
    return utils.get_time()
#7. 在utils封装查询数据库函数，然后在app.py注册新的路由，并定义函数
@app.route('/c1',methods=["get","post"])
def get_c1_data():
    data=utils.get_c1_data()
    #dada 是元组，利用jsonify转换为字典
    return jsonify({"confirm":str(data[0]),"suspect":str(data[1]),"heal":str(data[2]),"dead":str(data[3])})
#8.在utils封装查询数据库函数get_c2_data,然后在py注册新的路由
@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})
#9.在utils封装查询数据库函数get_l1_data,然后在py注册新的l1路由
@app.route('/l1')
def get_l1_data():
    data=utils.get_l1_data()
    #创建5个空的列表
    day,confirm,suspect,heal,dead=[],[],[],[],[]
    #数据集中的前七条是没有数据的所以之间切片切掉
    for a,b,c,d,e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        heal.append(e)
    return jsonify({"day":day,"confirm":confirm,"suspect":suspect,"heal":heal,"dead":dead})
#10.在utils封装查询数据库函数get_l2_data,然后在py注册新的l2路由
@app.route('/l2')
def get_l2_data():
    data=utils.get_l2_data()
    #创建5个空的列表
    day,confirm_add,suspect_add=[],[],[]
    #数据集中的前七条是没有数据的所以之间切片切掉
    for a,b,c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day":day,"confirm_add":confirm_add,"suspect_add":suspect_add})
#11.在utils封装查询数据库函数get_r1_data,然后再py注册新的r1路由
@app.route('/r1')
def get_r1_data():
    data=utils.get_r1_data()
    city=[]
    confirm=[]
    for k,v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city":city,"confirm":confirm})

#12.在utils封装查询数据库函数get_r2_data,在app.py导入包：string,jieba,decimal,然后在py注册新的r2路由
@app.route('/r2')
def get_r2_data():
    data = utils.get_r2_data() #格式如：(('安徽全省退出高风险地区51112',), ('大邱医院改造集装箱收治患者55592',))
    d=[]
    for i in data:
        k=i[0].rstrip(string.digits)#从右边截取数字出来，得到文字
        v=i[0][len(k):]  #获取热搜数字
        ks=extract_tags(k) #使用结巴读取关键字
        for j in ks:
            if not j.isdigit(): #如果不是数字就是关键次
                d.append({"name": j})
    return jsonify({"kws":d})
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app.run()