from nvd3 import lineWithFocusChart
import random
import datetime
import time

from whatJob.config import GlobalVar
curPwdPath=GlobalVar.get_value("curPwdPath")

file1=open(curPwdPath+"result\\Golangjinwei.json",encoding='utf-8')

jsonStr=file1.read()

file1.close()
# 打开旧文件
file2=open(curPwdPath+"result\\mapResult.html",encoding='utf-8')


# 打开新文件
f_new = open(curPwdPath+"result\\mapResult2.html",'w',encoding='utf-8')


# 循环读取旧文件
for line in file2:
    # 进行判断
    if "var points =" in line:
        line = line.replace('var points =[];','var points ='+jsonStr+";")
    # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
    f_new.write(line)

file2.close()

f_new.close()

