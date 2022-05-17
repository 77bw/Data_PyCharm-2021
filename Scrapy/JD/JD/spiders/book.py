import scrapy
import json
from JD.items import JdItem
# 1.导入类
# from scrapy_redis.spiders import RedisSpider

# 2.修改继承类
class BookSpider(scrapy.Spider):
    name = 'book'

# 3.注销start_urls&allowed_domains
#     'p.3.cn' 为解析图书列表允许的列名
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

# # 4.定义组件redis_key
#     redis_key = 'books'

#5.设置__init__

    # def __init__(self,*args,**kwargs):
    #     domain=kwargs.pop('domain','')
    #
    #     self.allowed_domains=filter(None,domain.split(','))


    def parse(self, response):
        big_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        print('大节点',len(big_list))
    #     for big in big_list:
    #         #获取大分类的节点链接、节点名称
    #         big_list_url='https:'+response.xpath('./@href').get()
    #         big_category=big.xpath('./text()').get()
    #         # 小分类的节点列表
    #         small_list = big.xpath('../following-sibling::dd[1]/em/a')
    #         # 遍历小分类的节点列表,获取到小分类名称、url
    #         for small in small_list[:1]:
    #             temp = {}
    #             temp['big_list_url'] = big_list_url
    #             temp['big_category'] = big_category
    #             temp['small_category'] = small.xpath('./text()').extract_first()
    #             temp['small_category_url'] = 'https:' + small.xpath('./@href').extract_first()
    #             # print(temp)
    #         # 构造请求,返回小分类的url
    #         yield scrapy.Request(
    #             temp['small_category_url'],
    #             callback=self.parse_book_list,
    #             meta={'meta1': temp}
    #         )
    # # 解析图片列表信息
    # def parse_book_list(self,response):
    #     # 接受parse方法返回的meta数据
    #     temp = response.meta['meta1']
    #     # 获取图片列表节点
    #     book_list = response.xpath('//*[@id="plist"]/ul/li/div')
    #     #遍历图书列表
    #     for book in book_list:
    #         #实列化item
    #         item=JdItem()
    #         # 书名信息、分类信息
    #         item['name'] = book.xpath('./div[3]/a/em/text()').extract_first().strip()
    #         item['big_category'] = temp['big_category']
    #         item['big_category_url'] = temp['big_list_url']
    #         item['small_category'] = temp['small_category']
    #         item['small_category_url'] = temp['small_category_url']
    #         # /div[1]/a/img/@src
    #         try:
    #             item['cover_url'] = 'https:' + book.xpath('./div[1]/a/img/@src').extract_first()
    #         except:
    #             item['cover_url'] = None
    #         try:
    #             item['detail_url'] = 'https:' + book.xpath('./div[3]/a/@href').extract_first()
    #         except:
    #             item['detail_url'] = None
    #         item['author'] = book.xpath(
    #             './div[@class="p-bookdetails"]/span[@class="p-bi-name"]/span[@class="author_type_1"]/a/text()').extract_first()
    #         item['publisher'] = book.xpath('./div[@class="p-bookdetails"]/span[2]/a/text()').extract_first()
    #         item['pub_date'] = book.xpath('./div[@class="p-bookdetails"]/span[3]/text()').extract_first().strip()
    #         # 获取价格的url
    #         # https://p.3.cn/prices/mgets?skuIds=J_11757834%2CJ_10367073%2CJ_11711801%2CJ_12090377%2CJ_10199768%2CJ_11711801%2CJ_12018031%2CJ_10019917%2CJ_11711801%2CJ_10162899%2CJ_11081695%2CJ_12114139%2CJ_12010088%2CJ_12161302%2CJ_11779454%2CJ_11939717%2CJ_12026957%2CJ_12184621%2CJ_12115244%2CJ_11930113%2CJ_10937943%2CJ_12192773%2CJ_12073030%2CJ_12098764%2CJ_11138599%2CJ_11165561%2CJ_11920855%2CJ_11682924%2CJ_11682923%2CJ_11892139&pduid=1523432585886562677791
    #         skuid = book.xpath('./@data-sku').extract_first()
    #         # print(skuid)
    #         pduid = '&pduid=1523432585886562677791'
    #         print(item)
    #         # 再次发送请求，获取价格信息
    #         if skuid is not None:
    #             url = 'https://p.3.cn/prices/mgets?skuIds=J_' + skuid + pduid
    #             yield scrapy.Request(
    #                 url,
    #                 callback=self.parse_price,
    #                 meta={'meta2': item}
    #             )
    #     def parse_price(self,response):
    #         item=response.meta["meta2"]
    #         data=json.loads(response.body)
    #         print(data)
    #         item['price']=data[0]['op']
    #         yield  item