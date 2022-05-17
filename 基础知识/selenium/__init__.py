from selenium import webdriver
import time
import json

# 填写webdriver的保存目录
driver = webdriver.Chrome('D:\Data\jupyterNote Data\chromedriver.exe')

# 记得写完整的url 包括http和https
driver.get('https://www.baidu.com/')
driver.implicitly_wait(10)  #隐式等待，如果执行完就继续，没有就一直等待直到10s为止
# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()
temp='BIDUPSID=5B142329744B593463103A1C53DE56A7; PSTM=1634014521; BAIDUID=5B142329744B5934C9BC7D7BCE3704DD:FG=1; BD_UPN=12314753; __yjs_duid=1_2fbf6c8599e68165d5d6096956ce853f1634189800278; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID_BFESS=bR8OJexroG04o2jHGoFdhhhmxeKK0gOTDYLEOwXPsp3LGJLVgdUVEG0PtoG1c9FbLCYgogKK3gOTH4AF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJAjoCPhfII3H48k-4QEbbQH-UnLq-jNfgOZ04n-ah02MbA4Mx7nhUKOMM732Rv-W20j0h7m3UTdsq76Wh35K5tTQP6rLtbbQGc4KKJxbn7nhJ8wQ45dLpFshUJiB5JMBan7_pjIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbRO4-TF-j5oWjM5; BDUSS=NIWEVleS01ZENJemxRcTloRG1EU3d0cHBlSW1WOExkN0RBRGw0TFBXOXg2TlpoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHFbr2FxW69hRU; BDUSS_BFESS=NIWEVleS01ZENJemxRcTloRG1EU3d0cHBlSW1WOExkN0RBRGw0TFBXOXg2TlpoSVFBQUFBJCQAAAAAAAAAAAEAAAC~qU91cG9yaXplMzU5NTM3MTgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHFbr2FxW69hRU; BD_HOME=1; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=6; H_PS_PSSID=34440_35106_31253_35239_34968_34584_34518_35233_34578_34872_35322_26350_35127; H_PS_645EC=9164%2F%2BkMXbt29D%2FV3ML8EXdIpRpJ7Eu1yk12tZ9R7ygb2znlvGkewaraML8XrTJOlB0B; ab_sr=1.0.1_MDNlMmIwZjllMzczZTY1M2M2MzY2ODUwNDdmZWQxNzg1NGNlNzRlYjBkNWY1MDE4MzUzMTUzYjg2ZDBlNzQ4NmIyMDQ5N2RmYWM1MGJmNzQwYzM0MmQ1Yjk3MDhkZGMwOWFmNjQyNDQ0ZWNhNTA5MzhkMmMzMjNhMTI2ZjJiODgxNTQzZTI3MzA0MDFhNGQyMTgwN2EzYTU5ODNkNTEwYQ==; BAIDUID_BFESS=2B5BBD00D0364A24C631A3DD44FCA157:FG=1; BA_HECTOR=ah210hag8h8g240hbp1gqusuf0r'
cookie={}
for data in temp.split(';'):
    key=data.split('=')[0]
    values=data.split('=')[1]
    cookie={key:values}
    # print(cookie)
    driver.add_cookie(cookie)
driver.find_element_by_xpath('//span[@class="user-name c-font-normal c-color-t"]').click()
# with open('cookies.txt','r') as f:
#     # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
#     cookies_list = json.load(f)
#     for cookie in cookies_list:
#         if 'expiry' in cookie:
#             del cookie['expiry']
#         driver.add_cookie(cookie)
#         print(cookie)
#     driver.refresh()
# driver.find_element_by_xpath('//span[@class="user-name c-font-normal c-color-t"]').click()
