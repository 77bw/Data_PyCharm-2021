from selenium import webdriver
import time
url = 'https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
song_name=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[1]/h1').text
singer=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/a').text
frist_title=driver.find_element_by_xpath('/html/body/div[1]').text #获取首页前面一行
summary=driver.find_element_by_xpath('//*[@id="album_desc"]/div').text#获取简介
print(song_name)
print(singer)
comments = driver.find_element_by_class_name('js_hot_list').find_elements_by_class_name('js_cmt_li') # 使用class_name找到评论
print(len(comments)) # 打印获取到的评论个数
for comment in comments: # 循环
    sweet = comment.find_element_by_tag_name('p') # 找到评论
    print ('评论：%s\n ---\n'%sweet.text) # 打印评论
print(frist_title)
print(summary)
driver.close()