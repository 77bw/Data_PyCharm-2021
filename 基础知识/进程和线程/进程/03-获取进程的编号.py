'''
获取进程的id
os模块提供了 os.getpid() 获取当前进程的id
           os.getppid()   获取当前进程的父进程id

'''
import os
from multiprocessing import Process
import  time
def sing(num,name):
    print('唱歌当前进程的id:{},父进程的id:{}'.format(os.getpid(),os.getppid()))
    for i in range(num):
        print(name+'唱歌中')
        time.sleep(0.5)

def dance(num,name):
    for i in range(num):
        print('跳舞当前进程的id:{},父进程的id:{}'.format(os.getpid(), os.getppid()))
        print(name+'跳舞中')
        time.sleep(0.5)

if __name__=='__main__':
    # 使用进程类创建线程对象
    # target:指定执行进程的函数名
    # args:使用元组的方式给指定的任务传参,要按传入参数的顺序
    # kwargs：使用字典方式给指定的任务传参，这个不用，既要指定的参数名字传入字典就可以了
    print('主线程的id：',os.getppid())
    sing_process=Process(target=sing,args=(3,'小明'))  #注意传入为3后面还要带个,
    dance_process=Process(target=dance,kwargs={'name':'小红','num':2})
    sing_process.start()
    dance_process.start()