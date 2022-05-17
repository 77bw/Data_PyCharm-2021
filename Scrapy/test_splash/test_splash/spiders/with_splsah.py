import scrapy
from scrapy_splash import SplashRequest # 使用scrapy_splash包提供的request对象


class WithSplsahSpider(scrapy.Spider):
    name = 'with_splsah'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/s?wd=python/']

    def start_requests(self):
        cookies = {'BIDUPSID': '5B142329744B593463103A1C53DE56A7', 'PSTM': '1634014521',
                   'BAIDUID': '5B142329744B5934C9BC7D7BCE3704DD:FG', 'BD_UPN': '12314753',
                   '__yjs_duid': '1_2fbf6c8599e68165d5d6096956ce853f1634189800278',
                   'BDUSS': 'WpDMmxnSFY2eE9mMG1RZkNsOG54M3BaS0tRWjQxSDBtQlpjMndzUXNwWjZVcjFoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrFlWF6xZVha',
                   'BDUSS_BFESS': 'WpDMmxnSFY2eE9mMG1RZkNsOG54M3BaS0tRWjQxSDBtQlpjMndzUXNwWjZVcjFoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHrFlWF6xZVha',
                   'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                   'BDSFRCVID': 'bR8OJexroG04o2jHGoFdhhhmxeKK0gOTDYLEOwXPsp3LGJLVgdUVEG0PtoG1c9FbLCYgogKK3gOTH4AF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                   'H_BDCLCKID_SF': 'tJAjoCPhfII3H48k-4QEbbQH-UnLq-jNfgOZ04n-ah02MbA4Mx7nhUKOMM732Rv-W20j0h7m3UTdsq76Wh35K5tTQP6rLtbbQGc4KKJxbn7nhJ8wQ45dLpFshUJiB5JMBan7_pjIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-j5oWjM5',
                   'BAIDUID_BFESS': 'C3265481C90D56DFDC307532966B8ADB:FG', 'BD_HOME': '1',
                   'BDSFRCVID_BFESS': 'bR8OJexroG04o2jHGoFdhhhmxeKK0gOTDYLEOwXPsp3LGJLVgdUVEG0PtoG1c9FbLCYgogKK3gOTH4AF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
                   'H_BDCLCKID_SF_BFESS': 'tJAjoCPhfII3H48k-4QEbbQH-UnLq-jNfgOZ04n-ah02MbA4Mx7nhUKOMM732Rv-W20j0h7m3UTdsq76Wh35K5tTQP6rLtbbQGc4KKJxbn7nhJ8wQ45dLpFshUJiB5JMBan7_pjIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-j5oWjM5',
                   'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0', 'delPer': '0', 'BD_CK_SAM': '1', 'PSINO': '6',
                   'H_PS_PSSID': '34440_35106_31253_35239_34968_34903_34584_34518_35233_34578_35322_26350_35127',
                   '__yjs_st': '2_NTNhMDAwZjdkN2Q1NTFlNjE3ZDFkZDhmZjIyN2YyZDUzYzYyOWVkZDNkNmE3OTM4ZTg0OTJjZGM1MTEyYmY2MjZlNzQwMWZiY2E0ZDI0YjFiMTM2OTYxZTZjMjkxZDc4MjhmMjkwMDI5NjcwY2UwYWRlMjM4NjFiODA4MDgyMzY1MGZmOGU1OWVjYTk3YzM2NDJmNzVjYzFhOWVmZTJmNTA0Zjg1Y2I5M2VhYmFkNTQxMzkyN2Q1MDZlZDM0ZWUzN2Y0NmNiZDA1N2E2ODM3NGI3YTEyYmI4M2I2NWEwZWViMGMzMmVhMWMzZjlmNjU3NDJmNWZhMjRiNWFlOTE0M183Xzk2MjhhMDMy',
                   'ab_sr': '1.0.1_ZDJlNjRiOGJmNWZiZWY5ZWEwZjVhMjM5MTA3MTZmNTcxNWQyYmM2ZWYwOWRmNzQ5N2E4NzBjNTU1NDIwNWVhMTA3ZGU1ZjU5NjMxMTMyMjhlYzA2M2FhNTE3M2IyZTliMWQxOTRmZGRhMzNiZDgyYzQwMGQ2ZDJkM2IyOTZlZWE4NzE3ODU2Y2I5NWY4ODllYjE2YTJhYzEwZTQxNTc0ZjhiMzJmNTJlNzQ4OWNhNTYwNWI1YWNjZTBlN2RjNzlj',
                   'baikeVisitId': '7a9c934e-94c1-4591-9f83-71645f996e9a',
                   'COOKIE_SESSION': '8_0_9_9_0_2_0_0_9_2_0_0_0_0_0_0_0_0_1638791141|9#545527_180_1638715835|9',
                   'H_PS_645EC': '64d2OzPPbVT+A/NUxM89wqkhcB9KO/mWvyw4d1Y70+u2dYPwIm9bIwxWCp8',
                   'BA_HECTOR': '25aga4ag8g21002gqn1gqrtv50q'}
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse_splash,
            args={'wait':10}, #最大超时时间，单位：秒
            endpoint='render.html',
            cookies=cookies
        )  #使用splash服务的固定参数

    def parse_splash(self, response):
        with open('with_splsah.html','w', encoding = 'utf-8') as f:
            f.write(response.body.decode())
