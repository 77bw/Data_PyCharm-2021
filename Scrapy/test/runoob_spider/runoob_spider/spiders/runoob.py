import scrapy


class RunoobSpider(scrapy.Spider):
    name = 'runoob'
    allowed_domains = ['runoob.com']
    start_urls = ['http://runoob.com/']

    def parse(self, response):
        node_list=response.xpath('//div[@class="col middle-column-home"]/div')
        for small in node_list:
            title=small.xpath('./a/h4/text()').get()
            href=small.xpath('./a/@href').get()
            items={
                'title':title,
                'href':href
            }
            yield  items

