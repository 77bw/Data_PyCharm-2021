"""
步骤1、 采用selenium自动登录获取cookie，保存到文件;
步骤2、 读取cookie，比较cookie的有效期，若过期则再次执行步骤1；
步骤3、 在请求其他网页时，填入cookie，实现登录状态的保持。
"""
import time
from selenium import webdriver
import json

browser = webdriver.Chrome("D:\Data\jupyterNote Data\chromedriver.exe")

def get_cookies():
    """
    通过selenium获取cookie保存在文件中
    :return:
    """
    url = 'https://login.taobao.com/'
    browser.get(url)
    browser.find_element_by_id('fm-login-id').send_keys('13592916928')
    browser.find_element_by_id('fm-login-password').send_keys('3214836abcdefg.')
    time.sleep(15)
    # browser.find_element_by_id('//button[@type="submit"]').click()
    # 获取cookie，这里得到的是一个列表
    cookies_list = browser.get_cookies()
    print(cookies_list)
    browser.close()
    with open("../cookies.txt", "w") as fp:
        json.dump(cookies_list, fp)  # 这里切记，如果我们要使用json.load读取数据，那么一定要使用json.dump来写入数据，
        # 不能使用str(cookies)直接转为字符串进行保存，因为其存储格式不同。这样我们就将cookies保存在文件中了。


def read_cookie():
    """
    读取cookie,添加到browser中
    :return:
    """
    url = 'https://i.taobao.com/my_taobao.htm?nekot=c3RyYXRiYm0=1638870426128'
    browser.get(url) # 这里必须先访问一次否则页面不能打开
    with open('../cookies.txt', 'r') as fp:
        cookies_list = json.load(fp)
        for cookies in cookies_list:
            print(cookies)
            browser.add_cookie(cookies)
    browser.get(url)

get_cookies()
read_cookie()