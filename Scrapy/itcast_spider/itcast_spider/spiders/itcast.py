import scrapy
from itcast_spider.items import ItcastSpiderItem
class ItcastSpider(scrapy.Spider):

    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml"]

    def parse(self, response):
        for each in response.xpath("//div[@class='li_txt']"):
            # 实列化对象
            item = ItcastSpiderItem()
            item['name']=each.xpath("h3/text()").get()
            item['title']=each.xpath("h4/text()").get()
            item['info']=each.xpath("p/text()").get()


            # items={
            #     'namae':name,
            #     'title':title,
            #     'info':info
            # }

            yield item



