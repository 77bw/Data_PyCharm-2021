import scrapy
import json
import pprint
from copy import deepcopy

class BookSpider(scrapy.Spider):
    name = 'book'
    #2.修改允许的域
    allowed_domains = ['jd.com']
    #1.修改起始的url
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath('//div[@class="mc"]/dl/dt')  # 获取大分类列表,每一图书分类的信息
        print(len(dt_list))
        for dt in dt_list:
            item = dict()  # 创建字典，存储相关信息
            item['b_cate'] = dt.xpath('./a/text()').extract_first()  # 大分类标题
            em_list = dt.xpath('./following-sibling::dd[1]/em')  # 获取小分类列表位置
            for em in em_list:  # 小分类列表
                item["s_href"] = em.xpath('./a/@href').extract_first()
                item['s_cate'] = em.xpath('./a/text()').extract_first()

                if item["s_href"] is not None:
                    item["s_href"] = 'https:' + item["s_href"]  # 补全url，之后进入下级链接，并进行抓取
                yield scrapy.Request(item["s_href"],
                                     callback=self.parse_book_list, meta={'item': deepcopy(item)})

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath('//div[@id= "plist"]/ul/li')
        for li in li_list:
            item['book_name'] = li.xpath(
                './/div[@class="p-name"]/a/em/text()').extract_first().strip()  # 书名前后有换行符，修掉
            item['book_img'] = li.xpath(
                './/div[@class="p-img"]//img/@src').extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath('.//div[@class="p-img"]//img/@data-lazy-img').extract_first()
                # 这里图片有两种情况，分别抓取
            item['book_img'] = 'https:' + item['book_img']
            # 补全地址
            item['book_author'] = li.xpath('.//span[@class="author_type_1"]/a/text()').extract()
            # 获取作者信息列表，注意部分没有
            item['book_author'] = ', '.join(item['book_author'])
            # 列表转字符串
            item['book_press'] = li.xpath(
                './/span[@class="p-bi-store"]/a/text()').extract_first()
            # 获取出版社信息
            item['book_date'] = li.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()
            # 获取出版日期，并规范格式
            item['book_sku'] = li.xpath('./div[1]/@data-sku').extract_first()
            # 获取商品编号
            yield scrapy.Request('https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_sku']),
                                 callback=self.parse_book_price, meta={'item': deepcopy(item)})
            # 通过分析得到价格信息的json数据地址，访问并获取价格

            # 翻页
            next_url = response.xpath(
                '//a[@class="pn-next"]/@href').extract_first()
            if next_url is not None:
                next_url = 'https://list.jd.com/' + next_url

                yield scrapy.Request(next_url, callback=self.parse_book_list, meta={'item': item})
                # 此时不需要deepcopy

    def parse_book_price(self, response):
        item = response.meta['item']
        item['book_price'] = json.loads(response.body.decode())[0]['op']
        # 将json转为字典，并提取价格，参考流程，在检查中搜索价格，找到对应字符，之后查看器网址与对应响应。
        pprint.pprint(item)