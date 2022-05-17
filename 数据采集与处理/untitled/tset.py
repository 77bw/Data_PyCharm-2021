from selenium import webdriver
import time

url = 'http://www.baidu.com'

driver = webdriver.Chrome()

driver.get(url)

# 通过xpath进行元素定位
#driver.find_element_by_xpath('//*[@id="kw"]').send_keys('南京')
# 通过css选择器进行元素定位
# driver.find_element_by_css_selector('#kw').send_keys('南京')
# # 通过name属性值进行元素定位
# driver.find_element_by_name('wd').send_keys('南京')
# 通过class属性值进行元素定位
# driver.find_element_by_class_name('s_ipt').send_keys('南京')
# 通过链接文本进行定位 ,hao123进行精确定位
# driver.find_element_by_link_text('hao123').click()
# 通过链接文本进行定位 ,hao进行模糊定位
# driver.find_element_by_partial_link_text('hao').click()

# 目标元素在当前html中是唯一标签的时候或者是众多定位出来的标签中的第一个的时候才能使用
#print(driver.find_element_by_tag_name('title'))

#driver.find_element_by_id('su').click()

#time.sleep(3)
#driver.quit()
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