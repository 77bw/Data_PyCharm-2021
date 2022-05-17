import  urllib.request
url="https://www.baidu.com"
with urllib.request.urlopen(url)as r:
    print(r.read())
