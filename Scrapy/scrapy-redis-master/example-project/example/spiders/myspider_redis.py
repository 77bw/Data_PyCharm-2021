from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'myspider_redis'
    redis_key = 'py21'

    def __init__(self, *args, **kwargs):
        # 动态定义允许的域列表。
        domain = kwargs.pop('domain', '')
        #filter函数在python3中返回过滤器对象，即将domain.split(',')中去掉的none，在python2中返回一个列表
        self.allowed_domains = filter(None, domain.split(','))
        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
