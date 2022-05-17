#主进程会等待所有的子进程执行结束再结束，除非设置子进程守护主进程
from multiprocessing import Process
import time

def work():
    #子进程工作2s
    for i in range(10):
        print("工作中...")
        time.sleep(0.2)

if __name__=='__main__':
    work_process=Process(target=work)
    work_process.start()

    time.sleep(1.5)
    print("主线程完成...")
    #总结：主线程会等待所有子进程执行完成以后程序在退出完成