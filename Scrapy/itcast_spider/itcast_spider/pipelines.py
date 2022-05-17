# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class ItcastSpiderPipeline(object):

    def __init__(self):
        self.file=open('teacher.json','w')
    def process_item(self, item, spider):
        #把itcast.py的yield items生成器所产生的打印出来
        #print(item)

        #将item对象强转成字典,该操作只能在scrapy中使用
        item=dict(item)

        #将字典数据序列化
        #序列化：序列化是将对象转化为字节序列的过程。对象序列化后可以在网络上传输，或者保存到硬盘上。
        json_data=json.dumps(item,ensure_ascii=False)+',\n'

        #将数据写入文件
        self.file.write(json_data)

        #默认使用完管道之后需要将数据返回给引擎
        return item
    def __del__(self):
        self.file.close()