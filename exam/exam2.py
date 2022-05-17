from selenium import webdriver
import time
url = 'http://www.baidu.com'
driver = webdriver.Chrome()
driver.get(url)
a=driver.find_element_by_xpath('//*[@id="s-top-left"]').text
b=driver.find_element_by_id("u1").text
c=driver.find_element_by_id("head_wrapper").text #获取热搜
d=driver.find_element_by_id("u")
p=driver.find_element_by_id("u1")
print(driver.title) #标题
print(a)
print(b)
print(c)
print(d)
print(p)
driver.find_element_by_id("kw").send_keys("大数据")
driver.find_element_by_id("su").click()
time.sleep(5)
q=driver.find_element_by_xpath('//*[@id="head"]').text
w=driver.find_element_by_id("u1")
d=driver.find_element_by_id("u")
e=driver.find_element_by_xpath('//*[@id="wrapper_wrapper"]').text #获取进入网页大数据整个内容
print(q)
print(w)
print(w.text)
print(e)
print(d)
driver.close()