#模拟登陆的操作，cookies参数的作用
#要在setting中设置ROBTS协议，USER_ASGENT

import scrapy
from selenium import webdriver

class CsdnSpider(scrapy.Spider):

    name = 'csdn'
    allowed_domains = ['csdn.net']
    start_urls = ['http://csdn.net/']



#重写start_request方法，将cookie传递给parse方法处理
    def start_requests(self):
        url=self.start_urls[0]

        temp='uuid_tt_dd=10_19003385840-1634015412138-689211; ssxmod_itna=eqROGIEDkDCDODzp+wP7IqDKMdXN+UnYfDBkDAIYDZDiqAPGhDC34/ArdSrMoaTqDy74Bp3dnA2expAbUW7fPIFUT4GLDmKDyUYoeGGAxBYDQxAYDGDDPDo2PD1D3qDkD7r=CScOqi3Dbr=Di4D+WwQDmqG0DDtHn4G2D7tcbxY=WLi6bCUYwM+4ai=DjkbD/3pTujrWaawl3QWPGE5DCEDCT2FG0DiTYqGy4KGufktZB3bkkkNMDmvqQghiUfhYbxpdKAx49B+P4rpW8YP4DNeNbgxh4VhbKY+1+HqDG8Dt+7h3eD==; ssxmod_itna2=eqROGIEDkDCDODzp+wP7IqDKMdXN+UnYD8LlB7xGNeeGaKxUgZB4AKOF6HGFtz=i93zZUPC72KYoSkE0FtOt05QAP5lYYhIV4tAdhGjn9k0rAdMgOlfwIrNjlDzHZxnR3u/F0jHsXRujR+TX5WRX53TQAFM+ffwpcDRQl8iNdGj6VnWifSgrMD66+nbWfecWovuN3aaN3r1ArLk9w+n0HfPu873U9tMp50kArfhBaUGIk0wQ8tBEhFR7AnbrbPzHzKKkUh+39ftksPKcdE4Xk8461zEXKx3WkwOTS4RXQycj/nv2==PsS+okqkYTdXwPWg1RgPjLoR+H8gK8iNh3r4jr8xHLxwu4Gz4w=7a4WrSg=GqQKxwElrcopn7wlkT6QGkm3lBKHGHcgDMja7WbDrsRjr+2Ilis0nNnWi8C3heQy+odEtH+AHREghKfWKfAoISxHftpMLkEeD7jejG094ziGklt4n5cRFPl+yKyyExcOXxCxhWqVKmqiD38HV4BelYOCUSe9wQ25=QOAuqVBKfh56FDjKDeTq4D; UserName=weixin_48068696; UserInfo=27c7171f40664688b657ac8b15e116bf; UserToken=27c7171f40664688b657ac8b15e116bf; UserNick=-bw-; AU=E7B; UN=weixin_48068696; BT=1634016277855; p_uid=U010000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_48068696%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19003385840-1634015412138-689211!5744*1*weixin_48068696; __gads=ID=e107be63a190db4a-226667d96dcc0026:T=1634016323:RT=1634016323:S=ALNI_MaJamMfUcKlEJTI4Z40oXfIZwpegA; c_dl_fref=https://so.csdn.net/so/search; c_dl_prid=1634567649461_437254; c_dl_rid=1634880869913_710061; c_dl_fpage=/download/weixin_38719643/13771252; c_dl_um=distribute.pc_search_result.none-task-blog-2%7Eall%7Ebaidu_landing_v2%7Edefault-3-83713274.pc_search_result_control_group; csrfToken=V4XCkas-ktfnkZtLxMinn3d4; c_first_ref=default; c_first_page=https%3A//www.csdn.net/; c_segment=11; dc_sid=43b779a2bca21bc92d8c41c1c882ec9d; is_advert=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1636165200,1636165273,1636165376,1636429228; csdn_highschool_close=close; firstDie=1; dc_session_id=10_1636460365904.628280; c_pref=https%3A//blog.csdn.net/panshao521_/article/details/113115960%3Fops_request_misc%3D%25257B%252522request%25255Fid%252522%25253A%252522163643778916780357263330%252522%25252C%252522scm%252522%25253A%25252220140713.130102334.pc%25255Fall.%252522%25257D%26request_id%3D163643778916780357263330%26biz_id%3D0%26utm_medium%3Ddistribute.pc_search_result.none-task-blog-2%7Eall%7Efirst_rank_ecpm_v1%7Erank_v31_ecpm-1-113115960.pc_search_result_cache%26utm_term%3Densure_ascii%253Dfalse%25E5%2587%25BA%25E7%258E%25B0%25E4%25B9%25B1%25E7%25A0%2581%26spm%3D1018.2226.3001.4187; c_ref=https%3A//www.csdn.net/; c_utm_term=extract_first%28%29; c_page_id=default; log_Id_click=605; dc_tos=r2b2hc; log_Id_pv=351; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1636462419; log_Id_view=1825'

        cookies={data.split('=')[0]:data.split('=')[-1]for data in temp.split(';')}

        yield scrapy.Request(
            url=url,
            callback=self.parse,
            cookies=cookies
        )

    def parse(self, response):
        print(response.xpath('/html/head/title/text()').get())
