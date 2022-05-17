import time
from threading import Thread

def work():
    for i in range(10):
        print("工作...")
        time.sleep(0.2)


if __name__ == '__main__':
    # sub_thread=Thread(target=work)  前台线程
    # sub_thread.start()
    #后台线程：主线程结束不想在等待子线程结束在结束，可以设置子线程守护主线程
    # 1.Thread(target=work,daemon=True)
    # 2.线程对象.setDaemon(True)
    # sub_thread = Thread(target=work,daemon=True)
    sub_thread = Thread(target=work)
    sub_thread.setDaemon(True)
    sub_thread.start()
    #主线程等待1s，执行结束
    time.sleep(1)
    print("主线程结束了...")

#结论：主线程会等待所有子线程执行结束在结束