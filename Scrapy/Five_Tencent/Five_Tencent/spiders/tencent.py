'''
创建crawlspider类，能处理一堆链接返回给方法处理，不用跟之前一样一堆链接返回一堆请求，增加速度
可以现在scrcdapy shell 中小工具中使用进行测试
crawl spider 经常应用与数据在一个页面上进行采集的情况（不用meta传参），如果数据在多个页面上采集，这个时候通常使用spider类
'''
import scrapy
from scrapy.linkextractors import LinkExtractor    #LinkExtractor链接提取器，提取链接的
from scrapy.spiders import CrawlSpider, Rule


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://careers.tencent.com/search.html?&start=0#a']

    #链接提取规则
    rules = (
        #LinkExtractor设置链接提取规则，一般使用allow参数，接收正则表达式allow符合正则里面的都要 deny符合里面的正则都舍弃
        #le=LinkExtractor(allow='position detail.php\?id=\d+&keywords=&tid=0&lid=0',deny=None)
        #follow参数决定是否在链接提取器提取的链接对应的响应中继续应用链接提取器链接
        #使用rule类生成链接规则提取对象，LinkExtractor能提取很多链接

        #设置详情页面链接提取规则
    #     Rule(LinkExtractor(allow=r'position detail.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item'),
    # )

        #设置翻页链接提取规则
        Rule(LinkExtractor(allow=r'position detail.php\?id=\d+&keywords=&tid=0&lid=0'), callback='parse_item',
             follow=True), )
    #不能重写Parse方法
    def parse_item(self, response):
        print('python21',response.url)
