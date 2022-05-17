#更加完善的管道
# 保存数据到数据库，以及各个爬虫文件对应的数据
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time

from itemadapter import ItemAdapter
import json
import pymysql
class WangyiPipeline:
    def open_spider(self,spider):   #在爬虫开启的时候仅执行一次
        if spider.name=='position': #添加spider进行筛选，只能运行spider名字为position的文件wangyi.josn
            self.file=open('wangyi.json','w',encoding="utf-8")
    def process_item(self, item, spider):
        if spider.name == 'position':
            item=dict(item)  #将item强制转换为字典
            str_data=json.dumps(item,ensure_ascii=False)+',\n'  #进行序列化操作
            self.file.write(str_data)
        return item
    def close_spider(self,spider):  ##在爬虫关闭的时候仅执行一次
        if spider.name == 'position':
            self.file.close()

class Position2Pipeline:
    def open_spider(self,spider):
        if spider.name=='position2':
            self.file=open('wangyi_simple.json','w')
    def process_item(self, item, spider):
        if spider.name == 'position2':
            item=dict(item)  #将item强制转换为字典
            str_data=json.dumps(item,ensure_ascii=False)+',\n'  #进行序列化操作
            self.file.write(str_data)
        return item
    def close_spider(self,spider):
        if spider.name == 'position2':
            self.file.close()
'''
#保存数据到数据库
class MysqlPipeline(object):
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="test", port=3306,
                                    charset='utf8')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into demo(name,link,depart,job_type,work_type,adress,num,date,duty,requir) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (
        item['name'], item['link'], item['depart'], item['job_type'], item['work_type'], item['adress'], item['num'],
        item['date'],item['duty'],item['requir']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()


    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
'''
class MysqlPipeline(object):
    conn = None
    cursor = None
    '''
    host: 地址 本地的是127.0.0.1
    port: 端口号 3306
    user: 用户名
    password: 密码
    db: 数据库名
    charset: 数据库编码（可选）
    '''
    def open_spider(self, spider):
        # 进行异常处理，可能会因为我们的疏忽或者数据库的更改造成连接失败，所以，我们要对这部分代码块进行异常捕捉
        try:
            # 连接数据库
            self.conn = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', db='test',
                                        charset='utf8')
            print('连接成功<<')
        except Exception as e:
            print(f'连接失败!!>>{e}')
            exit()  # 可以直接结束运行，按需求来设定

    def process_item(self, item, spider):
        # 创建游标  游标就相当于鼠标的作用
        self.cursor = self.conn.cursor()
        try:
            # 插入数据
            self.cursor.execute('INSERT INTO hh (name,link,depart,job_type,work_type,adress,num,date) VALUES("{}", "{}","{}", "{}","{}", "{}","{}", "{}")'.format(item['name'], item['link'], item['depart'], item['job_type'], item['work_type'], item['adress'], item['num'],item['date']))
            print(f"文章<{item['name']}>数据提交中...")
            # 数据提交到数据库
            self.conn.commit()
        except Exception as e:
            print(f">>存储失败>>文章<{item['name']}>{e}")
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        # 先关闭游标
        self.cursor.close()
        # 再关闭连接
        self.conn.close()
