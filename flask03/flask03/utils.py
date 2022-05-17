import time
import pymysql #与数据库交互需要用到
#1.获取系统时间函数

def get_time():
    time_str=time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")

#2.获取数字函数(封装一个模块)
def get_conn(): #封装连接
    """
    :return: 连游标
    """
    #创建连接
    conn=pymysql.connect(host="localhost",
                        user="root",
                        password='123456',
                        db="cov1",
                        charset='utf8')
    #创建游标
    cursor=conn.cursor()#执行完毕返回的结果集默认以元组显示
    return conn,cursor

def close_conn(conn,cursor): #执行完毕关闭连接和游标
    cursor.close()
    conn.close()

def query(sql,*args): #封装查询
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果((),())的元组形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res

def test():
    sql = "select * from details"
    res = query(sql)
    return res[0] #(或者res)
#中间4个数据
def get_c1_data():
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]

def get_c2_data():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res

def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res

def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res

def get_r1_data():
    sql = 'select city,confirm from ' \
          '(select city,confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'order by confirm desc limit 5'
    res = query(sql)
    return res

def get_r2_data():
    sql = "select content from hotsearch order by id desc limit 20"
    res = query(sql)
    return res

#做一个测试
if __name__ == '__main__':
    #get_r2_data()
    #print(get_l2_data())
    #print(get_l1_data())
    print(get_r2_data())
    #print(get_c1_data())
    # print(test())
    # print(test())




