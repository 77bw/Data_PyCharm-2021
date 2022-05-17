# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
class SixDoubanSpiderPipeline:
    def open_spider(self,spider):   #在爬虫开启的时候仅执行一次
        if spider.name=='douban': #添加spider进行筛选，只能运行spider名字为position的文件wangyi.josn
            self.file=open('douban.json','w',encoding="utf-8")
    def process_item(self, item, spider):
        if spider.name == 'douban':
            item=dict(item)  #将item强制转换为字典
            str_data=json.dumps(item,ensure_ascii=False)+',\n'  #进行序列化操作
            self.file.write(str_data)
        return item
    def close_spider(self,spider):  ##在爬虫关闭的时候仅执行一次
        if spider.name == 'douban':
            self.file.close()