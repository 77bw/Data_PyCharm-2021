'''
为了保证子进程能够正常运行，主进程会等待所有的子进程执行完成以后在销毁，设置守护进程的目的就是主进程推出子进程销毁，不让主进程等待子进程去执行
设置守护进程的方式：work_process.daemon=True

'''

from multiprocessing import Process
import time

def work():
    #子进程工作2s
    for i in range(10):
        print("工作中...")
        time.sleep(0.2)

if __name__=='__main__':
    work_process=Process(target=work)
    #设置守护进程，主线程结束子进程自动销毁，不在执行子进程代码
    work_process.daemon=True
    work_process.start()

    time.sleep(1.5)
    print("主线程完成...")
