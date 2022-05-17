#保存到sql里面的代码
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