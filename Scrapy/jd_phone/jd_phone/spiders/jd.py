import scrapy
from jd_phone.items import JdPhoneItem
import time
from selenium import webdriver
class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_8557&page=2&sort=sort_rank_asc&trans=1&JL=6_0_0&ms=9#J_main']

    def parse(self, response):
        item=JdPhoneItem()
        big_node=response.xpath('//ul[@class="gl-warp clearfix"]/li')
        for big in big_node:
            item['name']=big.xpath('.//a/em/text()').get()
            item['price']=big.xpath('.//div[@class="p-price"]//i/text()').get()
            item['vender_name']=big.xpath('.//div[@class="p-shop"]//a/text()').get()
            yield item

