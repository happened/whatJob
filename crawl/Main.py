#coding:utf-8
import requests
import re
import threading
import urllib.parse
import logging
import os
##引入别的处理函数


from bs4 import BeautifulSoup

from whatJob.config import GlobalVar


GlobalVar._init()
baseUrl="https://sou.zhaopin.com/?jl=489&"
curPwdPath="D:\\python\\whatJob\\"


GlobalVar.set_value("baseUrl",baseUrl)
GlobalVar.set_value("curPwdPath",curPwdPath)



from whatJob.config import Brower
from whatJob.config import GenerateHeadList
from whatJob.crawl import Salary,Map,WordCloud


#初始化一些全局变量


leibie = '1'

job_name=[]
#第一个是选择了地点 但第二个url不限制工作地点
#baseUrl="http://sou.zhaopin.com/jobs/searchresult.ashx?"\
        #"in=210500%3B160400%3B160000%3B160500%3B160200%3B300100%3B160100%3B160600&jl=上海%2B杭州%2B北京%2B广州%2B深圳&kw="
#上海%2B杭州%2B北京%2B广州%2B深圳

#baseurl中相应的参数代表不同的意义
#jl 地区编号 p页码 kw关键字 kt不清楚


#这是工资的区间 设置了8个
rate=[0,0,0,0,0,0,0,0]

#确定爬取的url  多线程
#totalNum代表爬取的页数 threadNum表示用的线程数 默认情况一个页面一个线程  页面必须大于线程数  如果2个页面 可以指定一个 也可指定2个
#这里有个问题 当10 4的时候 10/4=2 导致 10-8=2 2不小于2导致少爬两页 最好的配合是totalNUM/threaNum!=10%threadNum

def getJobUrl(job,totalNum,threadNum=1):
    url_job=[]
    if totalNum<threadNum:
        return False

    userAgentFile=open(curPwdPath+"config\\userAgent.txt")
    eachNum=int(totalNum/threadNum)
    curPage=0
    endPage = curPage + eachNum
    allList=[]
    lock=threading.Lock()
    allThread=[]

    for i in range(threadNum):
        userAgent=userAgentFile.readline().strip()

        if totalNum-endPage<eachNum:
            endPage=totalNum

        thread=threading.Thread(target=threadGetList,args=(curPage,endPage,allList,job))
        curPage=endPage
        endPage=curPage+eachNum
        allThread.append(thread)

    for thread in allThread:
        thread.setDaemon(True)
        thread.start()

    for thread in allThread:
        thread.join()


    for list in allList:
            if list not in url_job:
                url_job.append(list)
    return url_job

#爬取搜索结果展示页面 获得相应的job具体信息页面url

def threadGetList(curPage,endPage,allList,job,):
    for page in range(curPage,endPage):
        x = str(page)  # 爬取的页码
        p = str(page + 1)
        logging.info("正在抓取第" + p + "页...\n")  # 提示
        #url = baseUrl + job + "&p=" + x + "&isadv=0"  # url地址，此处为示例，可更据实际情况更改

        #这里BUG有点多 需要好好考虑
        jobmap={}
        jobmap["kw"]=job
        url = baseUrl+urllib.parse.urlencode(jobmap)+"&kt=3"+"&p="+p
        #url=baseUrl+"kw="+job+"&kt=3"+"&p="+p

        jobshtml=Brower.BrowerGetHTML(url)

        jobshtml=BeautifulSoup(jobshtml,'lxml')

        #这里貌似有个bug 网站改版了
        #jobDescribe = jobshtml.find_all(id="list-content-pile")
        try:
            jobDescribe=jobshtml.find('div',class_="contentpile__content")

            if jobDescribe==None:
                logging.warning("Failed to find the class content the href\n")
                exit(1)

            list = jobDescribe.find_all('a')

            if len(list)>=0:
                for index in list:
                    href=index['href']
                    if "jobs" in href:
                        allList.append(href)
            else:
                raise IndexError
        except  ValueError as e:
            logging.error(e)


        # 这里多线程要加锁

#这里对具体工作的html页面进行分析 是获得信息的主要途径

def getJobinfo(job,jobUrls,companyPos):
    logging.info("开始分析")
    file=open(curPwdPath+"result\\"+job+"\\"+job+".txt",'w',encoding='utf-8')

    indexOfUrl=1.00

    Content=''
    for url in jobUrls:
        ##生成随机Agent
        userAgent=GenerateHeadList.randomUserAgent()


        print("%.3f"%(indexOfUrl/len(jobUrls)),"%")

        head={
            'User-Agent':userAgent
        }
        htmlStr=requests.get(url,headers=head)

        html=BeautifulSoup(htmlStr.text,'lxml')
        # 数据清洗
        html=html.find('div',class_='app')



        #职位名
        jobNameTag = html.find('h3', class_="summary-plane__title")
        jobNameStr= jobNameTag.get_text().strip()
        jobNameStrs=jobNameStr.split('\n')

        #月薪
        jobMoneyTag=html.find('span',class_='summary-plane__salary')
        jobMoneyStr=jobMoneyTag.get_text().strip()
        jobMoneyStrs=jobMoneyStr.split('\n')
        Salary.processSalary(jobMoneyStrs[0],rate)

        fileContent = ''
        requireContent = ''

        if len(jobMoneyStrs) != 0:
            Salary.processSalary(jobMoneyStrs[0], rate)
            fileContent += jobNameStrs[0] + ": \n" + "薪资:" + jobMoneyStrs[0] + "\n"
        else:
            fileContent += jobNameStrs[0] + ": \n" + "薪资:" + "\n"

        # 工作地点
        pos = html.find('div', class_='job-address__content')
        if pos != None:
            addressTag = pos.find('span', class_='job-address__content-text')
            if addressTag != None:
                addressStr = addressTag.get_text().strip()

        companyPos.append(addressStr)
        fileContent+="公司地址: "+addressStr+ "\n"

        # 工作要求
        requireTag = html.find('div', class_='describtion__detail-content')
        requireStrs = []

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


        requireContent="任职条件:"+'\n'

        for require in requireStrs:
            requireContent+=require+"\n\n"

        indexOfUrl+=1
        Content+=fileContent+requireContent+"\n"

    file.write(Content)

    file.close()
    #显示数据信息

##获取文本信息的多线程实现  最好读写锁


if __name__=='__main__':

    job="芯片"
    #通过创建文件夹将所有的结果包括json文件 html文件以及txt文档集合在result下的job目录
    isExists=os.path.exists(curPwdPath+"result\\"+job)

    if not  isExists:
        os.makedirs(curPwdPath+"result\\"+job)
    # 公司地址
    companyPos = []

    urls=getJobUrl(job,10,5)

    if len(urls)!=0:
        hrefTxt=open("D:\\python\\whatJob\\tempUrl\\urlTxt.txt",'wt')
        for url in urls:
            hrefTxt.write(url+'\n')

        urls=list(set(urls))


        ##这里添加多线程的处理
        getJobinfo(job,urls,companyPos)


        #处理工资表 rate 全局变量
        Salary.writeNumToJson(job,rate)
        Salary.showSalary(job)

        #处理公司经纬度 写入到jingwei.json里
        Map.getJinWei(job,companyPos)
        Map.generateHtml(job)

        WordCloud.GenerateCloud(job)

    else:
        logging.error("未得到职业信息")


























