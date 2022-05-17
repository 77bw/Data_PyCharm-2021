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

with open('cookies.txt','r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        if 'expiry' in cookie:
            del cookie['expiry']
        driver.add_cookie(cookie)
        print(cookie)
    driver.refresh()
#验证一下是否成功登录
# driver.find_element_by_xpath('//span[@class="user-name c-font-normal c-color-t"]').click()
