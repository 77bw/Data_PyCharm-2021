# Scrapy settings for test_splash project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'test_splash'

SPIDER_MODULES = ['test_splash.spiders']
NEWSPIDER_MODULE = 'test_splash.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test_splash (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# 渲染服务的url
SPLASH_URL = 'http://192.168.99.100:8050/'
# 下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# 去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# 使用Splash的Http缓存
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#    'cookie':'BIDUPSID=5B142329744B593463103A1C53DE56A7; PSTM=1634014521; BAIDUID=5B142329744B5934C9BC7D7BCE3704DD:FG=1; BD_UPN=12314753; __yjs_duid=1_2fbf6c8599e68165d5d6096956ce853f1634189800278; BDUSS=WpDMmxnSFY2eE9mMG1RZkNsOG54M3BaS0tRWjQxSDBtQlpjMndzUXNwWjZVcjFoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrFlWF6xZVha; BDUSS_BFESS=WpDMmxnSFY2eE9mMG1RZkNsOG54M3BaS0tRWjQxSDBtQlpjMndzUXNwWjZVcjFoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrFlWF6xZVha; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=bR8OJexroG04o2jHGoFdhhhmxeKK0gOTDYLEOwXPsp3LGJLVgdUVEG0PtoG1c9FbLCYgogKK3gOTH4AF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJAjoCPhfII3H48k-4QEbbQH-UnLq-jNfgOZ04n-ah02MbA4Mx7nhUKOMM732Rv-W20j0h7m3UTdsq76Wh35K5tTQP6rLtbbQGc4KKJxbn7nhJ8wQ45dLpFshUJiB5JMBan7_pjIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-j5oWjM5; BAIDUID_BFESS=C3265481C90D56DFDC307532966B8ADB:FG=1; BD_HOME=1; BDSFRCVID_BFESS=bR8OJexroG04o2jHGoFdhhhmxeKK0gOTDYLEOwXPsp3LGJLVgdUVEG0PtoG1c9FbLCYgogKK3gOTH4AF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJAjoCPhfII3H48k-4QEbbQH-UnLq-jNfgOZ04n-ah02MbA4Mx7nhUKOMM732Rv-W20j0h7m3UTdsq76Wh35K5tTQP6rLtbbQGc4KKJxbn7nhJ8wQ45dLpFshUJiB5JMBan7_pjIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-j5oWjM5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=34440_35106_31253_35239_34968_34903_34584_34518_35233_34578_35322_26350_35127; __yjs_st=2_NTNhMDAwZjdkN2Q1NTFlNjE3ZDFkZDhmZjIyN2YyZDUzYzYyOWVkZDNkNmE3OTM4ZTg0OTJjZGM1MTEyYmY2MjZlNzQwMWZiY2E0ZDI0YjFiMTM2OTYxZTZjMjkxZDc4MjhmMjkwMDI5NjcwY2UwYWRlMjM4NjFiODA4MDgyMzY1MGZmOGU1OWVjYTk3YzM2NDJmNzVjYzFhOWVmZTJmNTA0Zjg1Y2I5M2VhYmFkNTQxMzkyN2Q1MDZlZDM0ZWUzN2Y0NmNiZDA1N2E2ODM3NGI3YTEyYmI4M2I2NWEwZWViMGMzMmVhMWMzZjlmNjU3NDJmNWZhMjRiNWFlOTE0M183Xzk2MjhhMDMy; ab_sr=1.0.1_ZDJlNjRiOGJmNWZiZWY5ZWEwZjVhMjM5MTA3MTZmNTcxNWQyYmM2ZWYwOWRmNzQ5N2E4NzBjNTU1NDIwNWVhMTA3ZGU1ZjU5NjMxMTMyMjhlYzA2M2FhNTE3M2IyZTliMWQxOTRmZGRhMzNiZDgyYzQwMGQ2ZDJkM2IyOTZlZWE4NzE3ODU2Y2I5NWY4ODllYjE2YTJhYzEwZTQxNTc0ZjhiMzJmNTJlNzQ4OWNhNTYwNWI1YWNjZTBlN2RjNzlj; baikeVisitId=7a9c934e-94c1-4591-9f83-71645f996e9a; COOKIE_SESSION=8_0_9_9_0_2_0_0_9_2_0_0_0_0_0_0_0_0_1638791141|9#545527_180_1638715835|9; H_PS_645EC=64d2OzPPbVT+A/NUxM89wqkhcB9KO/mWvyw4d1Y70+u2dYPwIm9bIwxWCp8; BA_HECTOR=25aga4ag8g21002gqn1gqrtv50q'
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'test_splash.middlewares.TestSplashSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'test_splash.middlewares.TestSplashDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'test_splash.pipelines.TestSplashPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
