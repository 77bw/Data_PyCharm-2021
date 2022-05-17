# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

#设置重复过滤器的模板（要是没有设置用的是python里面的集合。指纹的集合，用redis数据库里面的）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
#设置调度器（原先要是不设置用scrapy的调度器，设置了用redis数据库的调度器，具有能与redis交互的功能）
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#设置当爬虫结束的时候是否保持redis数据库中的去重集合与任务队列（即保持数据持久化，可以实现增量爬取）
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    #当开启该管道，该管道将会把数据存到redis数据库中，实现各台机器数据的共享
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

#设置redis数据库
REDIS_URL = "redis://127.0.0.1:6379"


LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
#减慢下载速度，每隔1s发送一个请求
DOWNLOAD_DELAY = 1
