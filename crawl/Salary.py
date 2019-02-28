import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import re
from nvd3 import pieChart
import  json
import numpy as np
salaryList=[]
from whatJob.config import GlobalVar

curPwdPath=GlobalVar.get_value("curPwdPath")
#处理工资 清洗数据

def processSalary(salaryStr,rate):
    wage=''
    wageStr=re.findall(r"\d+-?\d+",salaryStr)
    if len(wageStr)==0:
        return
    wageRange=wageStr[0].split("-")

    try:
        i=int ( int(wageRange[0])*0.9 + int(wageRange[1])*0.1 )
        if i < 4000:
            rate[0]+=1
        elif i >= 4000 and i <= 6000:
            rate[1] += 1
        elif i > 6000 and i <= 8000:
            rate[2] += 1
        elif i > 8000 and i <= 10000:
            rate[3] += 1
        elif i > 10000 and i <= 15000:
            rate[4] += 1
        elif i > 15000 and i <= 20000:
            rate[5] += 1
        elif i > 20000 and i <= 30000:
            rate[6] += 1
        else:
            rate[7] += 1
    except:
        pass

#主要把具体每个工资段的数量写入json里
def writeNumToJson(job,rate):
    wageNumDict={}
    index=0
    wageRange = ['<4k', "4-6k", '6-8k', '8-10k', '10-15k', '15-20k', '20-30k', '>30k']
    for wage in wageRange:
        wageNumDict[wage]=rate[index]
        index+=1

    result=[]
    result.append(wageNumDict)
    with open(curPwdPath+"result\\"+job+"\\"+job+".json",'w') as f:
        json.dump(result,f)
    f.close()

#利用获取的json工资信息显示图表
def showSalary(job):
    label=[]
    rate=[]
    with open(curPwdPath+"result\\"+job+"\\"+job+".json") as f:
        wageData=json.load(f)
        for wageDict in wageData:
            for k ,v in wageDict.items():
                label.append(k)
                rate.append(v)
    f.close()

    # labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
    # autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
    # shadow，饼是否有阴影
    # startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
    # pctdistance，百分比的text离圆心的距离
    # patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

    # 改变文本的大小
    # 方法是把每一个text遍历。调用set_size方法设置它的属性
    patches, l_text, p_text = plt.pie(rate, labels=label,
                                       labeldistance=1.1, autopct='%2.0f%%', shadow=False,
                                       startangle=90, pctdistance=0.6)
    for t in l_text:
        t.set_size = 30
    for t in p_text:
        t.set_size = 20
    # loc: 表示legend的位置，包括'upper right','upper left','lower right','lower left'等
    # bbox_to_anchor: 表示legend距离图形之间的距离，当出现图形与legend重叠时，可使用bbox_to_anchor进行调整legend的位置
    # 由两个参数决定，第一个参数为legend距离左边的距离，第二个参数为距离下面的距离
    plt.axis('equal')
    plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
    plt.grid()
    plt.savefig(curPwdPath+"result\\"+job+"\\"+job+"SalaryPie",dpi=100)
    '''
    output_file = open('test_pieChart.html', 'w')
    type='pieChart'
    chart=pieChart(name=type,color_category='category20c',height=450,width=450,yaxis='%2.0f%%')

    chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
    chart.callback = '''
                        #function(){
                       # d3.selectAll(".nv-pie .nv-pie .nv-slice").on('click',
                       #     function(d){
                        #    console.log("piechart_callback_test: clicked on slice " + JSON.stringify(d['data']));
                       #     console.log('/app/fruit?type='.concat(d['data']['label']));
                       # }
                    #'''
    '''
    extra_serie={"tooltip":{"y_start":"","y_end":" cal"}}
    chart.add_serie(y=rate,x=label,extra=extra_serie)
    chart.buildhtml()
    output_file.write(chart.htmlcontent)
    output_file.close()
    '''















