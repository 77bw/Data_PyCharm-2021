'''
多任务：同一时间执行多个任务   多任务又分为：1.并发：同一时间内交替去执行多个任务 2.并行：在一段时间内真正的同时一起执行多个任务
  （为了能充分利用cpu以提高程序的执行的效率，python提供了两种常见的多任务编程的方式：进程和线程）
1）进程：运行的程序
特点：1.动态性（一次执行的过程，它是动态产生，动态消亡）
      2.并发性（多个进程可并发执行）
      3.独立性（进程是一个能够独立运行的基本单位，同时也是操作系统进行资源分配和调度的基本单位）
      4.异步性（进程之间的相互制约使得进程的执行具有间断性，它们按各自独立的，不可预知的速度向前推进）
进程的创建步骤：
1.导入进程包
from multiprocessing import Process
2.通过进程类创建进程对象
进程对象= Process(target=任务名)  #这里的任务名指的是函数名或者方法名
3.启动进程执行任务
进程对象.start()
'''
from multiprocessing import Process
import  time
def sing():
    for i in range(3):
        print('唱歌中')
        time.sleep(0.5)

def dance():
    for i in range(3):
        print('跳舞中')
        time.sleep(0.5)

if __name__=='__main__':
    sing_process=Process(target=sing)
    dance_process=Process(target=dance)
    sing_process.start()
    dance_process.start()