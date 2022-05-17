import scrapy
from gushiwen_spider.items import GushiwenSpiderItem

class GushiwenSpider(scrapy.Spider):
    name = 'gushiwen'
    allowed_domains = ['gushiwen.cn']
    start_urls = ['https://www.gushiwen.cn/default_1.aspx']

    # 该爬虫先从上面起始的第一个URL地址开始发出请求，并得到请求响应的数据，得到响应数据后，数据的解析就用如下的parse函数进行解析
    def parse(self, response):
        gsw_list=response.xpath('//div[@class="left"]/div[@class="sons"]')  # xpath返回的是列表(每个div sons标签，也就是每首诗)
        for gsw in gsw_list:  # 对每首诗进行遍历
            title=gsw.xpath('.//b/text()').get()   # xpath返回的是列表(取列表第一个也就是诗的标题)
            if title:
                source = gsw.xpath('.//p[@class="source"]/a/text()').extract()  # 获取 作者 和 朝代 的列表
                author = source[0]  # 获取 作者
                dynasty = source[1]  # 获取 朝代
                content_list=gsw.xpath('.//div[@class="contson"]//text()').getall()
                content=''.join(content_list).strip()   # 列表中的每个元素用空串拼接，去除列表并用strip()方法移除字符串头尾指定的字符
                item=GushiwenSpiderItem()
                item['title']=title
                item['author']=author
                item['dynasty']=dynasty
                item['content']=content
                yield item

        #翻页逻辑实现
        next_href=response.xpath('//a[@id="amore"]/@href').get()
        if next_href != None:
            yield scrapy.Request(url=next_href,callback=self.parse)