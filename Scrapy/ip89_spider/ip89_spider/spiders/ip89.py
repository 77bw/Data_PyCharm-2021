# scrapy的入门
import scrapy

#创建爬虫类 并且这个类必须继承自scrapy.Spider
class Ip89Spider(scrapy.Spider):
    name = 'ip89'  #爬虫名字    必须唯一
    allowed_domains = ['89ip.cn']   #允许采集的域名
    start_urls = ['http://89ip.cn/']   #开始采集的网站

    #解析响应数据  提取数据 或者网站等  response是start_urls里面的链接爬取后的结果，也就是网页源码
    def parse(self, response):

        #提取数据
        #提取ip PORT
        selectors=response.xpath('//tr')    #  //这个是选择所有的tr标签
        #循环遍历tr标签下的td标签
        for selector in selectors:
            ip=selector.xpath('./td[1]/text()').get() # .在当前节点下继续选择
            port=selector.xpath('./td[2]/text()').get()  # .在当前节点下继续选择

            #print(ip,port)
            #保存文件
            items={
                'ip':ip,
                'port':port
            }
            yield items
            #翻页操作
            next_page=response.xpath('//a[@class="layui-laypage-next"]/@href').get()
        if next_page:
            print(next_page)
            #拼接网址
            next_url=response.urljoin(next_page)  #拿着response的url跟着next_page的url进行拼接

            #发出请求 Request callback是回调函数 就是将请求得到的响应交给自己处理
            yield scrapy.Request(next_url,callback=self.parse)   #yield是生成器


from scrapy import cmdline, Spider
if __name__ == '__main__':
    cmdline.execute("scrapy crawl ip89".split())
