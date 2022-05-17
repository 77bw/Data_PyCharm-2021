# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql
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
            self.cursor.execute('INSERT INTO demo (author,theme) VALUES("{}", "{}")'.format(item['author'], item['theme']))
            print(f"文章<{item['author']}>数据提交中...")
            # 数据提交到数据库
            self.conn.commit()
        except Exception as e:
            print(f">>存储失败>>文章<{item['author']}>{e}")
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        # 先关闭游标
        self.cursor.close()
        # 再关闭连接
        self.conn.close()
class RunoobSpiderPipeline:
    def __init__(self):
        self.filename = open('thousandPic.json', 'w')

    def process_item(self, item, spider):
        #  ensure_ascii=False 可以解决 json 文件中 乱码的问题。
        item=dict(item)
        text = json.dumps(dict(item), ensure_ascii=False) + ',\n'  # 这里是一个字典一个字典存储的，后面加个 ',\n' 以便分隔和换行。
        self.filename.write(text)
        return item

    def close_spider(self, spider):
        self.filename.close()
