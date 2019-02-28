# _*_ coding= utf-8 _*_

import pandas as pd
import json
import requests
import csv
import traceback
import os
import time

from whatJob.config import GlobalVar

curPwdPath=GlobalVar.get_value("curPwdPath")

def getJinWei(job,positions):

    result=[]
    for pos in positions:
        try:
            url='http://api.map.baidu.com/geocoder/v2/?address='+pos+'&output=json&ak=gStVcApQyfVj1zvOwmA1lZtTIi43uIxX'
            response=requests.get(url)
            s=requests.Session
            s.keep_alive=False

            answer=response.json()

            if answer['result']!=None:
                lng = float(answer['result']['location']['lng'])
                lat = float(answer['result']['location']['lat'])
                jinweiDict={"lng":lng,"lat":lat,"count":1}
                result.append(jinweiDict)
        except:
            time.sleep(5)
            continue

    file=open(curPwdPath+"result\\"+job+"\\"+job+"jinwei.json",'w')
    json.dump(result,file)
    file.close()


def generateHtml(job):
    file1 = open(curPwdPath + "result\\"+job+"\\"+job+"jinwei.json", encoding='utf-8')
    jsonStr = file1.read()

    file1.close()
    # 打开旧文件
    file2 = open(curPwdPath + "config\\mapTemplate.html", encoding='utf-8')

    # 打开新文件
    f_new = open(curPwdPath + "result\\"+job+"\\"+job+"Map.html", 'w', encoding='utf-8')

    # 循环读取旧文件
    for line in file2:
        # 进行判断
        if "var points =" in line:
            line = line.replace('var points =[];', 'var points =' + jsonStr + ";")
        # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
        f_new.write(line)

    file2.close()
    f_new.close()

