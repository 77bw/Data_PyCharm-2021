# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    depart= scrapy.Field()
    job_type = scrapy.Field()
    work_type = scrapy.Field()
    adress = scrapy.Field()
    num = scrapy.Field()
    date = scrapy.Field()

    duty=scrapy.Field()
    requir=scrapy.Field()

class Position2Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    depart= scrapy.Field()
    job_type = scrapy.Field()
    work_type = scrapy.Field()
    adress = scrapy.Field()
    num = scrapy.Field()
    date = scrapy.Field()