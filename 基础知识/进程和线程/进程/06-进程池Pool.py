#Pool线程池:必须依赖于主进程而存活
#模式：非阻塞（异步）：apply_async 在进程池创建完进程后立刻返回，不会等待进程执行结束。（即主进程执行完成就结束）
# 阻塞：apply 在创建完进程且进程中所有的任务执行完毕后才会返回（主线程会等待所有子进程执行完成以后程序在退出完成）
#端口号：每一个进程都有自己独特的端口号
import time
import random
from multiprocessing import Pool
import  os
def study():
    start=time.time()
    time.sleep(random.randint(1,3))
    end=time.time()
    print('进程学习花费了{}秒,进程端口号:{}'.format(end-start,os.getpid()))

def sing():
    start=time.time()
    time.sleep(random.randint(1,3))
    end=time.time()
    print('唱歌花费了{}秒,进程端口号:{}'.format(end-start,os.getpid()))

def watch_TV():
    start=time.time()
    time.sleep(random.randint(1,3))
    end=time.time()
    print('看电视花费了{}秒,进程端口号:{}'.format(end-start,os.getpid()))

def game():
    start=time.time()
    time.sleep(random.randint(1,3))
    end=time.time()
    print('打游戏花费了{}秒,进程端口号:{}'.format(end-start,os.getpid()))

def listen_music():
    start=time.time()
    time.sleep(random.randint(1,3))
    end=time.time()
    print('听音乐花费了{}秒,进程端口号:{}'.format(end-start,os.getpid()))

if __name__ == '__main__':
    pool=Pool(3) #进程池最大可以存放三个进程
    lambda_list=[study,sing,watch_TV,game,listen_music]
    for i in lambda_list:
        #非阻塞状态
        # pool.apply_async(i)
        #阻塞状态 一个一个的执行，有点像单进程
        pool.apply(i)
    # time.sleep(3)
    #非阻塞切换为阻塞，添加以下两个条件
    # pool.close()
    # pool.join()#插位置
    print('我是主进程')

