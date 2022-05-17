import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='123456',
                     database='test')
print('连接成功')
# 使用cursor()方法获取操作游标
cursor1 = db.cursor()
cursor2 = db.cursor()
# SQL 查询语句

cursor1.execute('SELECT price FROM shop ORDER BY price DESC LIMIT 1')

cursor2.execute('SELECT price FROM shop ORDER BY price  LIMIT 1')

price_max=cursor1.fetchall()
price_min=cursor2.fetchall()
print('最高工资:',price_max[0][0],'元','最低工资:',price_min[0][0],'元')
# 关闭数据库连接
db.close()