import os
import random


curPwdPath="D:\\python\\whatJob\\"

def randomUserAgent():
    userAgentFile = open(curPwdPath+"config\\userAgent.txt")
    List=[]
    while 1:
        line=userAgentFile.readline()
        if not line:
            break
        List.append(line.strip())



    return random.choice(List)
