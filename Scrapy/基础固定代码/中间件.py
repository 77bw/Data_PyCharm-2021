import random
#每一代码需要在此进行更改
from Six_Douban_spider.settings import USER_AGENT_LIST,PROXY_LIST
from scrapy import signals
import base64

#定制随机请求头
class RandomUserAgent(object):
    def process_request(self, request, spider):
         # print(request.headers['User-Agent'])
           ua=random.choice(USER_AGENT_LIST)
           request.headers['User-Agent']=ua

#定制随机ip代理
class RandomProxy(object):
    def process_request(self,request,spider):
        proxy=random.choice(PROXY_LIST)
        print(proxy)
        if "user_passwd" in proxy:
            #对账号密码进行编码
            b64_up=base64.b64encode(proxy['user_passwd'].encode())
            #设置认证
            request.headers['proxy_Authorization']="Basic "+b64_up.decode()
            #设置代理
            request.meta["proxy"]=proxy["ip_port"]
        else:
            #设置代理
            request.meta["proxy"]=proxy["ip_port"]

# 需要在settings中设置：
# USER_AGENT_LIST=[ "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"]
#
# PROXY_LIST=[
#     {"ip_port":'47.101.162.15:16817',"user_passwd":"1329696875:pnt9ozje"},
#     # {"ip_port":"111.59.199.58:8118"},
#     # {"ip_port":"47.243.190.108:7890"},
#     # {"ip_port":"106.15.197.250:8001"},
#     # {"ip_port":"125.73.131.137:9091"},
#     # {"ip_port":"183.21.81.88:40539"},
#     # {"ip_port":"139.198.179.174:3218"},
#     # {"ip_port":"223.241.78.141:8118"},
# ]

# 并在中间件开启


# 还有个测试阶段对于refer=none的应对
# class MyUseragent(object):
#     def process_request(self,request,spider):
#         referer=request.url
#         if referer:
#             request.headers["referer"] = referer
#         agent=random.choice(MY_USER_AGENT)
#         request.headers['User-Agent'] = agent
