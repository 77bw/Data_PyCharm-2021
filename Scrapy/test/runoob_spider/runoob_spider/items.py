# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RunoobSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PhotoSpiderItem(scrapy.Item):
    author = scrapy.Field()  # 作者
    theme = scrapy.Field()  # 主题