from selenium import webdriver
import time
import json

# 填写webdriver的保存目录
driver = webdriver.Chrome('D:\Data\jupyterNote Data\chromedriver.exe')

# 记得写完整的url 包括http和https
driver.get('https://www.58pic.com/login')

# 程序打开网页后20秒内 “手动登陆账户”
time.sleep(40)

with open('cookies.txt','w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))

driver.close()