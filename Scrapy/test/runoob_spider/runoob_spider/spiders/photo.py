import scrapy
from runoob_spider.items import PhotoSpiderItem

class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['58pic.com']
    start_urls = ['https://www.58pic.com/c/']


    def start_requests(self):
        url=self.start_urls[0]
        temp='message2=1; qt_visitor_id=%221bf8bca3784cab2fbf8d02af07156e06%22; qt_type=0; loginBackUrl=%22https%3A%5C%2F%5C%2Fwww.58pic.com%5C%2Fc%5C%2F%22; did=%229cdc14914c6894df%22; history_did_data_9cdc14914c6894df=%22eyJkaXN0aW5jdF9pZCI6IjljZGMxNDkxNGM2ODk0ZGYiLCJ1dG1fY2FtcGFpZ24iOjAsInV0bV9zb3VyY2UiOjAsInV0bV9tZWRpdW0iOjAsInV0bV90ZXJtIjowLCJ1dG1fY29udGVudCI6MCwidGlkIjowfQ%3D%3D%22; qiantudata2018jssdkcross=%7B%22distinct_id%22%3A%2217e248249532e0-0788db7987df55-4303066-1440000-17e24824954751%22%7D; qtjssdk_2018_cross_new_user=1; loginTime=4; popupShowNum=1; Hm_lvt_41d92aaaf21b7b22785ea85eb88e7cea=1641290023,1641290025; FIRSTVISITED=1641290025.461; Hm_lvt_644763986e48f2374d9118a9ae189e14=1641290023,1641290025; risk_forbid_login_uid=%2272250085%22; tid_today_data_9cdc14914c6894df_20220104=%22eyJub1RvZGF5RGlkIjoxfQ%3D%3D%22; history_uid_data_72250085=%22eyJ1aWQiOjcyMjUwMDg1LCJkaXN0aW5jdF9pZCI6ImIwMWZiYjkzNTU4MDY4YzMiLCJ1dG1fY2FtcGFpZ24iOjAsInV0bV9zb3VyY2UiOjAsInV0bV9tZWRpdW0iOjAsInV0bV90ZXJtIjowLCJ1dG1fY29udGVudCI6MCwiZmlyc3RfdHJhZmZpY19zb3VyY2VfdHlwZSI6MCwidGlkIjowfQ%3D%3D%22; auth_id=%2272250085%7C5Y2D5Zu%2B55So5oi3XzAwODU%3D%7C1641894833%7C31ae2cd272168c071093da54a1fcc10a%22; success_target_path=%22https%3A%5C%2F%5C%2Fwww.58pic.com%5C%2Flogin%22; sns=%7B%22token%22%3A%7B%22ToUserName%22%3A%22gh_9b23fdd4e900%22%2C%22FromUserName%22%3A%22oAuSO1h8_TKt61Rr_Yk_7Dhi-zQw%22%2C%22CreateTime%22%3A%221641290032%22%2C%22MsgType%22%3A%22event%22%2C%22Event%22%3A%22SCAN%22%2C%22EventKey%22%3A%22login%22%2C%22Ticket%22%3A%22gQFE7zwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyVUFGSE5RMkFlZW0xT3pwa2h4Y28AAgQrGdRhAwR4AAAA%22%2C%22isThePublic%22%3A1%7D%2C%22type%22%3A%22weixin%22%7D; ssid=%2261d41931e71f84.04244037%22; last_login_type=6; qt_risk_visitor_id=%22fa217610f725759e51309ab8a8519801%22; newbieTask=%22%7B%5C%22is_login%5C%22%3A%5C%221%5C%22%2C%5C%22is_search%5C%22%3A%5C%220%5C%22%2C%5C%22is_download%5C%22%3A%5C%220%5C%22%2C%5C%22is_keep%5C%22%3A%5C%220%5C%22%2C%5C%22login_count%5C%22%3A%5C%221%5C%22%2C%5C%22upload_material%5C%22%3A%5C%220%5C%22%2C%5C%22before_login_time%5C%22%3A%5C%221641225600%5C%22%2C%5C%22is_task_complete%5C%22%3A%5C%220%5C%22%2C%5C%22task1%5C%22%3A%5C%220%5C%22%2C%5C%22task2%5C%22%3A%5C%220%5C%22%2C%5C%22task3%5C%22%3A%5C%220%5C%22%7D%22; _is_pay=0; _auth_dl_=NzIyNTAwODV8MTY0MTg5NDgzNHxkMzU1ZmY5M2MxOWI4MGY3YTFkOTYzYzNlN2RlZDkyYg%3D%3D; qt_uid=%2272250085%22; censor=%2220220104%22; inviteEvent_loginEvent_72250085=1; Hm_lpvt_41d92aaaf21b7b22785ea85eb88e7cea=1641290034; Hm_lpvt_644763986e48f2374d9118a9ae189e14=1641290034; imgCodeKey=%228fed5cf8787c93f1753da153546726ed%22; qt_utime=1641290102; big_data_visit_time=1641290102'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            cookies=cookies)
    def parse(self, response):
        node_list=response.xpath('//*[@class="wrap-list fl"]//a')
        for node in node_list:
            item=PhotoSpiderItem()

            item['author']=node.xpath('./p[2]/span/span[2]/text()').get()
            item['theme'] = node.xpath('./p[1]/span/text()').get()
            yield item

        url=response.xpath('/html/body/div[5]/a[2]/@href').get()
        if url != None:
            url = response.urljoin(url)
            yield scrapy.Request(
                url=url, callback=self.parse
            )
