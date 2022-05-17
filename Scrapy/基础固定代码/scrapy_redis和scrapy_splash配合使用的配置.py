#直接复制重写的去重类。然后带上settings的设置

from __future__ import absolute_import

from copy import deepcopy

from scrapy.utils.request import request_fingerprint
from scrapy.utils.url import canonicalize_url

from scrapy_splash.utils import dict_hash

from scrapy_redis.dupefilter import RFPDupeFilter


def splash_request_fingerprint(request, include_headers=None):
    """ Request fingerprint which takes 'splash' meta key into account """

    fp = request_fingerprint(request, include_headers=include_headers)
    if 'splash' not in request.meta:
        return fp

    splash_options = deepcopy(request.meta['splash'])
    args = splash_options.setdefault('args', {})

    if 'url' in args:
        args['url'] = canonicalize_url(args['url'], keep_fragments=True)

    return dict_hash(splash_options, fp)


class SplashAwareDupeFilter(RFPDupeFilter):
    """
    DupeFilter that takes 'splash' meta key in account.
    It should be used with SplashMiddleware.
    """
    def request_fingerprint(self, request):
        return splash_request_fingerprint(request)

#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

"""以上为重写的去重类，下边为爬虫代码"""

from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest


class SplashAndRedisSpider(RedisSpider):
    name = 'splash_and_redis'
    allowed_domains = ['baidu.com']

    # start_urls = ['https://www.baidu.com/s?wd=13161933309']
    redis_key = 'splash_and_redis'
    # lpush splash_and_redis 'https://www.baidu.com'

    # 分布式的起始的url不能使用splash服务!
    # 需要重写dupefilter去重类!

    def parse(self, response):
        yield SplashRequest('https://www.baidu.com/s?wd=13161933309',
                            callback=self.parse_splash,
                            args={'wait': 10}, # 最大超时时间，单位：秒
                            endpoint='render.html') # 使用splash服务的固定参数

    def parse_splash(self, response):
        with open('splash_and_redis.html', 'w') as f:
            f.write(response.body.decode())

#--------------------------------------------------------------------------------------------------------------
#settings的设置

# 渲染服务的url
SPLASH_URL = 'http://192.168.99.100:8050/'
# 下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# 使用Splash的Http缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 去重过滤器
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter" # 指纹生成以及去重类
#就主要多了这个关键的类
DUPEFILTER_CLASS = 'test_splash.spiders.splash_and_redis.SplashAwareDupeFilter' # 混合去重类的位置

SCHEDULER = "scrapy_redis.scheduler.Scheduler" # 调度器类
SCHEDULER_PERSIST = True # 持久化请求队列和指纹集合, scrapy_redis和scrapy_splash混用使用splash的DupeFilter!
ITEM_PIPELINES = {'scrapy_redis.pipelines.RedisPipeline': 400} # 数据存入redis的管道
REDIS_URL = "redis://127.0.0.1:6379" # redis的url