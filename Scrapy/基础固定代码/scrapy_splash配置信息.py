SPLASH_URL = 'http://192.168.99.100:8050/'  # 渲染服务的url
DOWNLOADER_MIDDLEWARES = {   # 下载器中间件
'scrapy_splash.SplashCookiesMiddleware': 723,
'scrapy_splash.SplashMiddleware': 725,
'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'  # 去重过滤器
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'   # 使用Splash的Http缓存