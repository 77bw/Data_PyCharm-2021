import time
from threading import Thread
def sing(num,name):
    for i in range(num):
        print(name,":唱歌...")
        time.sleep(1)


def dance(count,name):
    for i in range(count):
        print(name,":跳舞...")
        time.sleep(1)

if __name__ == '__main__':
    #args:以元组的方式给执行任务传递参数
    sing_thread=Thread(target=sing,args=(3,"bw"))
    #kwargs:以字典方式给执行任务传递参数
    dance_thread=Thread(target=dance,kwargs={'name':'小明','count':2})
    sing_thread.start()
    dance_thread.start()