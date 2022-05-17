import random
#每一代码需要在此进行更改
from jd_phone.settings import USER_AGENT_LIST
from scrapy import signals
import base64

#定制随机请求头
class RandomUserAgent(object):
    def process_request(self, request, spider):
         # print(request.headers['User-Agent'])
           ua=random.choice(USER_AGENT_LIST)
           request.headers['User-Agent']=ua
