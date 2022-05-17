import scrapy
from Six_Douban_spider.items import SixDoubanSpiderItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        el_list=response.xpath('//*[@class="info"]')
        print(len(el_list))

        for el in el_list:
            item=SixDoubanSpiderItem()
            item['name']=el.xpath('./div[1]/a/span[1]/text()').get()
            item['info']=el.xpath('./div[2]/p[1]/text()[1]').get()
            item['score']=el.xpath('./div[2]/div/span[2]/text()').get()
            item['desc']=el.xpath('./div[2]/p[2]/span/text()').get()
            yield item



        url=response.xpath('//span[@class="next"]/a/@href').get()
        if url !=None:
            url=response.urljoin(url)
            yield  scrapy.Request(
                url=url,callback=self.parse
            )