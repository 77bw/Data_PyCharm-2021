


import urllib.request #引入包
import requests#
import parsel
url="https://gz.lianjia.com/ershoufang/"
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
req=urllib.request.Request(url,headers=headers)
response=urllib.request.urlopen(req) #爬取网页
response

selector = parsel.Selector(req.text)
lis = selector.css('.sellListContent li')
for li in lis:
    # 标题
    title = li.css('.title a::text').get()
    if title:
        # 地址
        positionInfo = li.css('.positionInfo a::text').getall()
        # 小区
        community = positionInfo[0]
        # 地名
        address = positionInfo[1]
        # 房子基本信息
        houseInfo = li.css('.houseInfo::text').get()
        # 房价
        Price = li.css('.totalPrice span::text').get() + '万'
        # 单价
        unitPrice = li.css('.unitPrice span::text').get().replace('单价', '')
        # 发布信息
        followInfo = li.css('.followInfo::text').get()
        dit = {
            '标题': title,
            '小区': community,
            '地名': address,
            '房子基本信息': houseInfo,
            '房价': Price,
            '单价': unitPrice,
            '发布信息': followInfo,
        }
        print(dit)