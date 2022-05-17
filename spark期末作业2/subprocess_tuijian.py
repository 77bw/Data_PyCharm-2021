import time
import subprocess
import time
start = time.perf_counter()

subprocess.run("python testml.py ratings_1_1.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_2.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_3.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_4.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_5.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_6.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_7.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_8.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_9.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
subprocess.run("python testml.py ratings_1_10.csv", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,encoding="utf-8")
fo = open("performance.txt", "a+")
end = time.perf_counter()
fo.write("Time used:"+str(end-start))
print("Time used:"+str(end-start))