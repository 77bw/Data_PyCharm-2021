# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
from JD_spider.settings import USER_AGENT_LIST,PROXY_LIST
from scrapy import signals
import base64

#定义一个中间件类
class MyUseragent(object):
    def process_request(self,request,spider):
        referer=request.url
        referer="http://www.google.com"
        if referer:
            request.headers["referer"] = referer


#定制随机请求头
class RandomUserAgent(object):

    def process_request(self, request, spider):
         # print(request.headers['User-Agent'])
           ua=random.choice(USER_AGENT_LIST)
           request.headers['User-Agent']=ua
# #定制随机ip代理
# class RandomProxy(object):
#     def process_request(self,request,spider):
#         proxy=random.choice(PROXY_LIST)
#         print(proxy)
#         if "user_passwd" in proxy:
#             #对账号密码进行编码
#             b64_up=base64.b64decode(proxy['user_passwd'].encode())
#             #设置认证
#             request.headers['proxy_Authorization']="Basic "+b64_up.decode()
#             #设置代理
#             request.meta["proxy"]=proxy["ip_port"]
#         else:
#             #设置代理
#             request.meta["proxy"] = proxy["ip_port"]
#定制随机ip代理
class RandomProxy(object):
    def process_request(self,request,spider):
        proxy=random.choice(PROXY_LIST)
        print(proxy)
        if "user_passwd" in proxy:
            #对账号密码进行编码
            b64_up=base64.b64decode(proxy['user_passwd'].encode())
            #设置认证
            request.headers['proxy_Authorization']="Basic "+b64_up.decode()
            #设置代理
            request.meta["proxy"]=proxy["ip_port"]
        else:
            #设置代理
            request.meta["proxy"] = proxy["ip_port"]