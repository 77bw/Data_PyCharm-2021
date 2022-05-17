import os #数据导入和保存
import re #正则表达式
import requests #爬取网站网页数据
from bs4 import BeautifulSoup #解析爬取网页用
import jieba #中文分词
from collections import Counter #Counter:对序列中出现的各个元素进行统计
import csv

url="https://www.jinyongwang.net/data/renwu"
res=requests.get(url) #获得整个页面
html=res.text
soup=BeautifulSoup(html,'lxml')
orpath=soup.find_all(class_='datapice')
pattern=re.compile('(?<=alt=").*?(?=")')
name_list=re.findall(pattern,str(orpath))
name_set=set(name_list)
print(name_list)