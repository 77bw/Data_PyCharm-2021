import  urllib.request
from selenium import webdriver
import time
driver=webdriver.Chrome()
first_url='https://www.lagou.com/jobs/list_python?'

def get_cookie():
    driver.get(first_url)
    driver.find_element_by_xpath('//a[@class="login"]').click()
    time.sleep(2.5)
    driver.find_element_by_xpath('//div[@class="forms-bottom forms-bottom-code"]/div[1]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//div[@class="input_border"]/input').send_keys('13592916928')
    driver.find_element_by_xpath('//input[@type="password"]').send_keys('a13592916928')
    time.sleep(3)
    driver.find_element_by_class_name('login-password').click()
    time.sleep(15)

    cookies_list=driver.get_cookies()
    print(cookies_list)
    for cookie in cookies_list:
        driver.add_cookie(cookie)
        time.sleep(3)

    driver.refresh()

get_cookie()