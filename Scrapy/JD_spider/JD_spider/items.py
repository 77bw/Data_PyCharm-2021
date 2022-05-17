# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名，大分类，大分类页面url，小分类，小分类页面url，封面图片链接，详情页面url，作者，出版社，出版时间，价格
    name=scrapy.Filed()
    big_category = scrapy.Field()
    big_category_link = scrapy.Field()
    small_category = scrapy.Field()
    small_category_link = scrapy.Field()
    cover_url = scrapy.Field()
    detail_url=scrapy.Filed()
    bookname = scrapy.Field()
    author = scrapy.Field()
    publisher=scrapy.Filed()
    pub_date=scrapy.Filed()
    price = scrapy.Field()

