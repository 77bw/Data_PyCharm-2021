import threading
import time


def task():
    time.sleep(1)
    #current_thread():获取当前线程的线程对象
    thread=threading.current_thread()
    print(thread)

if __name__ == '__main__':
    for i in range(5):
        sub_thread=threading.Thread(target=task)
        sub_thread.start()

#多线程之间的执行是无序的，由cpu调度的