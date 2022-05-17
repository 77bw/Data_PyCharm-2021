from multiprocessing import Process
import  time
def sing(num,name):
    for i in range(num):
        print(name+'唱歌中')
        time.sleep(0.5)

def dance(num,name):
    for i in range(num):
        print(name+'跳舞中')
        time.sleep(0.5)

if __name__=='__main__':
    # 使用进程类创建线程对象
    # target:指定执行进程的函数名
    # args:使用元组的方式给指定的任务传参,要按传入参数的顺序
    # kwargs：使用字典方式给指定的任务传参，这个不用，既要指定的参数名字传入字典就可以了

    sing_process=Process(target=sing,args=(3,'小明'))  #注意传入为3后面还要带个,
    dance_process=Process(target=dance,kwargs={'name':'小红','num':2})
    sing_process.start()
    dance_process.start()