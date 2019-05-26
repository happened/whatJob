#coding:utf-8
import requests
import re
import operator
import random
import sys

from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator

import codecs
import jieba
import jieba.analyse
import os
import matplotlib.pyplot as plt
from PIL import  Image,ImageDraw,ImageFont,ImageSequence
from bs4 import BeautifulSoup
import numpy as np

#job = "机器学习" #以爬取xxx职业为例

from whatJob.config import GlobalVar
curPwdPath=GlobalVar.get_value("curPwdPath")

def judge_pure_english(tag):
    return all(ord(c) < 128 for c in tag)

def ignore(stopwords):
    tags=['1','2,','3','4','5']
    for i in tags:
        stopwords.add(i)
#生成词云

def GenerateCloud(job):
    comment_text=open(curPwdPath+"result\\"+job+"\\"+job+".txt",'r',encoding='utf-8').read()
    #cut_text=" ".join(jieba.cut(comment_text))
    #找到频率最高的分词
    #词性allow_pos=('n','r')
    tags=jieba.analyse.extract_tags(comment_text,topK=1500,withWeight=True)
    #处理英文 让其权值加大0.01  比较粗放
    tagstring=""
    dict={}
    for tag,weight in tags:
        if judge_pure_english(tag):
            dict[tag]=weight+0.01
            continue
        dict[tag]=weight
    #排序key
    sortDict=sorted(dict.items(),key=operator.itemgetter(1))
    num=1
    #选取前300个作词云
    for i in sortDict:
        if num<=300:
            tagstring=tagstring+sortDict[len(sortDict)-num][0]+" "
            num=num+1
        else:
            break

    #随机选取背景图图片
    index=str(random.randint(1,5))
    print(index)
    color_mask=np.array(Image.open(curPwdPath+"config\\back"+index+".png"))

    stopwords=set(STOPWORDS)
    ignore(stopwords)
    cloud=WordCloud(
        # 设置字体，不指定就会出现乱码
        font_path="C:\\Users\\Bored\\Downloads\\test.ttf",
        # font_path=path.join(d,'simsun.ttc'),
        # 设置背景色
        background_color='white',
        # 词云形状
        mask=color_mask,
        # 允许最大词汇
        max_words=2000,
        # 最大号字体
        max_font_size=40,
        stopwords=stopwords
    )
    word_cloud=cloud.generate(tagstring)


    #if os.path.exists(curPwdPath+"result\\"+job+"\\"+job+"KeyWord.jpg")==False:
    word_cloud.to_file(curPwdPath+"result\\"+job+"\\"+job+"KeyWord.jpg")
    #plt.savefig(job,dpi=600)



