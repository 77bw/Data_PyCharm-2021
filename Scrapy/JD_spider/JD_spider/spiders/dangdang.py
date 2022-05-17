import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['https://book.dangdang.com/']

    redis_key="dangdang"

    def parse(self, response):
        #大分类分组
        div_list=response.xpath('//div[@class="con flq_body"]/div')
        for div in div_list:
            item={}
            item["b_cate"]=div.xpath('./dl/dt//text()').get_all()
            item["b_cate"]=[i.strip() for i in item["b_cate"] if len(i.strip())>0]
            #中间分组
            dl_list=response.xpath('./div//dl[@class="inner_dl"]')
            for dl in dl_list:
                item["m_cate"]=dl.xpath('./dt//text()').get().strip()
                #小分类分组
                a_list=dl.xpath('./dd/a')
                for a in a_list:
                    item["s_href"]=a.xpath('./@href').get()
                    item["s_cate"]=a.xpath('./text()').get()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta={"item":item}
                        )
    def parse_book_list(self,response):
        item=response.meta["item"]
        li_list=response.xpath('//ul[@class="bigimg"]/li')
        for li in li_list:
            item['book_img']=li.xpath('./a[@class="pic"]/img/@src').get()
            item["book_namae"]=li.xpath('./p[@class="name"]/a/@title').get()
            item["book_desc"]=li.xpath('')
            print(item)