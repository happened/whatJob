import requests
import urllib.request
from bs4 import BeautifulSoup
from whatJob.crawl import Salary
rate=[0,0,0,0,0,0,0,0]


import time
from selenium import webdriver

url="https://jobs.zhaopin.com/000404489250630.htm"

htmlStr = requests.get(url)

html = BeautifulSoup(htmlStr.text, 'lxml')

requireTag = html.find('div', class_='pos-ul')
requireStrs=[]
if requireTag != None:
    requireStr = requireTag.find_all('p')
    if requireStr != None:
            index = 0
            length = len(requireStr)
            flag = True

            while index < length and flag == True:
                txt = requireStr[index].get_text().strip()
                if txt == "":
                    index += 2
                    while index < length:
                        txt = requireStr[index].get_text().strip()
                        if txt != "":
                            requireStrs.append(txt)
                            index += 1
                        else:
                            flag = False
                            break
                index += 1

print(requireStrs)
