# 完善管道数据的保存
import time

import scrapy
from wangyi.items import Position2Item
# from scrapy_redis.spiders import RedisSpider
class RedisPositionSpider(scrapy.Spider):
    name = 'redis_position'
    allowed_domains = ['163.com']
    start_urls = ['https://hr.163.com/position/list.do']
    # redis_key = "po1"
    # def __init__(self, *args, **kwargs):
    #     # 动态定义允许的域列表。
    #     domain = kwargs.pop('domain', '')
    #     #filter函数在python3中返回过滤器对象，即将domain.split(',')中去掉的none，在python2中返回一个列表
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(RedisPositionSpider, self).__init__(*args, **kwargs)
    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )
    def parse(self, response):
        #提取数据
        #获取所有职位节点列表  xpath换成class是因为一更新网站该id就会变动
        node_list=response.xpath('//*[@class="position-tb"]/tbody/tr')
        #遍历节点列表  使用枚举就可以获取期中节点列表相对应的数据
        for num,node in enumerate(node_list):
            #设置过滤条件，将目标节点获取出来
            if num % 2==0:
                #实列化对象，将内容存到item里面去
                item=Position2Item()
                item['name']=node.xpath('./td[1]/a/text()').get()
                #response.urljoin用于拼接相对路径的url，可以理解为自动补全
                item['link'] = response.urljoin(node.xpath('./td[1]/a/@href').get())
                item['depart'] = node.xpath('./td[2]/text()').get()
                item['job_type'] = node.xpath('./td[3]/text()').get()
                item['work_type'] = node.xpath('./td[4]/text()').get()
                item['adress'] = node.xpath('./td[5]/text()').get()
                #对前后空行的处理，strip()字符串处理
                item['num'] = node.xpath('./td[6]/text()').get().strip()
                item['date'] = node.xpath('./td[7]/text()').get()
                yield  item
        #翻页提取
        part_url=response.xpath('/html/body/div[2]/div[2]/div[2]/div/a[last()]/@href').get()
        #判断终止条件
        if part_url !='javascript:void(0)':
            next_url=response.urljoin(part_url)
            #构建请求对象，并且返回给引擎
            yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)


