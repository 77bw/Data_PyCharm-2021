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
# 1.根据本书口诀构建动态网站
aircle=["fei","xue","lian","tian","she","bai","lu","xiao","shu","shen","xia","yi","bi","yuan","yue"]
url_base="https://www.jinyongwang.net/"
#动态王志构建
url=[url_base+name+'/' for name in aircle ]
for u in url:
    #print(u)
    #提取书名
    book=u.split('/')[-2]
     # print(book)
    res=requests.get(u)
    html=res.text
    # html

    #3.使用BeautifulSoup,将已经下载的html内容解析为soup对象，每个节点就是一个对象
    soup=BeautifulSoup(html,'lxml')
    # soup

    #4。过滤节点元素，class="mlist"
    orpath=soup.find_all(class_="mlist")
    # orpath

    # 5使用正则表达式去除多余的标记，获取金庸小说里面所有的章节的超链接：如a href=/fei/484.html 得到/fei/484.html
    book="fei"
    data=[]
    pattern=re.compile('(?<=href=").*?(?=")')
    chape_list=re.findall(pattern,str(orpath))
    # chape_list

    #6.具体进入每一个章节的超链接，获取章节的内容
    for l in chape_list:
        web=url_base+l
        res=requests.get(web)
        html=res.text
        pattern=re.compile('(?<=<p>).*?(?=</p>)')
        text=re.findall(pattern,str(html))
       #  print(text)


        for i in range(len(text)-1): #提取相邻两段提取出人物，使用集合
    #       print(i,i+1)
            a=jieba.lcut(text[i])  #使用jieba对相邻段落进行分词
            b=jieba.lcut(text[i+1])
        # print(a)
        # print(b)
            first=set(a) & set(name_set)  #集合求交集，把段落中的出现的人物从我们爬取的人物库找出来
            second=set(b) & set(name_set)
    #           print(first)
    #           print(second)
            if (first and second):     #相邻段落有人物出现
                for  f in first:  #遍历首段落得人物
                    for s in second:  #遍历下一段落得人物
                        if(f!=s):   #只有人物相等但是出现相邻段落里，我们就确定人物他们是有关系的，符合知识图谱要求
    #                       print(f+"_"+s+"_"+"fei") #类似：苗人凤_胡一刀_fei
                            data.append(f+"_"+s+"_"+book)  #构造知识图谱结点
                        # print(data)
# 8.统计相邻小说人物出现次数，并统计数据，保存数据，写入文件
counts=Counter(data) #该类能够计算出字符串或列表等中不同元素出现的次数，返回值是一个字典
#print(counts)  #得到的次数就是我们构建知识图谱的边（权重）
    #9.保存写入数据到文件中
f=open('data_all.csv','w',encoding='utf-8',newline="")
csv_write=csv.writer(f)
csv_write.writerow(["source","target","book","weight"])
for c in counts:#遍历字典按列写入数据
      #  print(c)
    line=c.split("_") #获取字典中的key拆分'马春花_马行空_fei' 成 马春花,马行空,fei 字符串
        #print(line) # line列表类型
        #得到字典中的value
       # print(counts[c])
        #把统计粗来的数据追加到line里面
    line.append(counts[c])
    print(line)
    csv_write.writerow(line)
    print("成功")
f.close()