# 比较完整的scrapy的爬取过程，包括参数的构建，数据的保存，在pipelines的管道中保存
#meta获取参数item实现在不同参数在不同解析函数中的使用
import scrapy
from wangyi.items import WangyiItem

class PositionSpider(scrapy.Spider):
    name = 'position'
    allowed_domains = ['163.com']
    start_urls = ['https://hr.163.com/position/list.do']

    def parse(self, response):
        #提取数据
        #获取所有职位节点列表  xpath换成class是因为一更新网站该id就会变动
        node_list=response.xpath('//*[@class="position-tb"]/tbody/tr')
        #遍历节点列表  使用枚举就可以获取期中节点列表相对应的数据
        for num,node in enumerate(node_list):
            #设置过滤条件，将目标节点获取出来
            if num % 2==0:
                #实列化对象，将内容存到item里面去
                item=WangyiItem()
                item['name']=node.xpath('./td[1]/a/text()').get()
                #response.urljoin用于拼接相对路径的url，可以理解为自动补全
                item['link'] = response.urljoin(node.xpath('./td[1]/a/@href').get())
                item['depart'] = node.xpath('./td[2]/text()').get()
                item['job_type'] = node.xpath('./td[3]/text()').get()
                item['work_type'] = node.xpath('./td[4]/text()').get()
                item['adress'] = node.xpath('./td[5]/text()').get()
                #对前后空行的处理，strip()字符串处理
                item['num'] = node.xpath('./td[6]/text()').get().strip()
                item['date'] = node.xpath('./td[7]/text()').get()

                #构建详情页面的请求
                yield scrapy.Request(
                    url=item['link'],
                    callback=self.parse_detail,
                    meta={'item':item} ,#将item传进去给’item‘，即上面的name，link，depart等等
                    dont_filter=True  #出现这个提示的原因是scrapy的filter功能将请求自动过滤掉，从而不会出现请求的结果,所以添加了这个过滤器
                )
        #翻页提取
        part_url=response.xpath('/html/body/div[2]/div[2]/div[2]/div/a[last()]/@href').get()
        #判断终止条件
        if part_url !='javascript:void(0)':
            next_url=response.urljoin(part_url)
            #构建请求对象，并且返回给引擎
            yield scrapy.Request(url=next_url,callback=self.parse,dont_filter=True)

    def parse_detail(self,response):
        #将meta传参数获取，即获取上面meta的值
        item=response.meta['item']

        #提取剩余的字段数据
        item['duty']=response.xpath('/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/text()').getall()
        item['requir']=response.xpath('/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div[2]/div/text()').getall()

        #返回引擎
        yield  item
