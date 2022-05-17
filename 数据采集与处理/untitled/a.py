from  selenium import webdriver
import  time
browser = webdriver.Chrome()
browser.get('HTTPS://www.taobao.com')
input = browser.find_element_by_id('q')
input.send_keys('iphone')
time.sleep(2)
input.clear()
input.send_keys('milk')
time.sleep(2)
button=browser.find_elements_by_class_name('btn-search')
button.click()