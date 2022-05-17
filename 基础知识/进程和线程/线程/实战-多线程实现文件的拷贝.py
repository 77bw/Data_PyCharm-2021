import os
import threading

def copy_file(file_name,source_dir,dest_dir):
    #1.拼接源文件夹路径和目标文件路径
    source_path=os.path.join(source_dir,file_name)
    dest_path = os.path.join(dest_dir, file_name)
    #2.打开源文件和目标文件
    with open(source_path,"rb") as source_file:
        with open(dest_path,"wb") as dest_file:
            #3.循环读取源文件到目标路径
            while True:
                data=source_file.read(1024)
                if data:
                    dest_file.write(data)
                else:
                    break


if __name__ == '__main__':
    #1.定义源文件目录和目标文件目录
    source_dir="E:\\大数据\\sql---资料、代码\\ppt"
    dest_dir="C:\\Users\\bw\\Desktop\\test"

    #2.创建目标文件夹
    try:
        os.mkdir(dest_dir)
    except:
        print("目标文件已经存在")

    #3.读取源文件夹的的文件列表
    file_list=os.listdir(source_dir)

    #4.遍历文件列表实现拷贝
    for file_name in file_list:
        #copy_file(file_name,source_dir,dest_dir)
        #5.使用多进程实现任务拷贝
        sub_process=threading.Thread(target=copy_file,args=(file_name,source_dir,dest_dir))
        sub_process.start()