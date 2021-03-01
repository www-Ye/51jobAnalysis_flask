# -*- codeing = utf-8 -*-
# @Time : 2021/3/1 23:40
# @Author : wy
# @File : jobFunction.py
# @Software : PyCharm

import sqlite3

def getJobnum():
    datalist = []
    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()

    sql = "select keyword,count(keyword) from job group by keyword"
    data = cur.execute(sql)
    for item in data:
        #print(item)
        datalist.append(item)
    cur.close()
    con.close()

    return datalist

def isQian(salary):
    flag = False
    for c in salary:
        if c == '千':
            flag = True
            break
    return flag

def numstrTofloat(str):
    floatNum = 0.0
    t = 10.0
    flag = True
    for s in str:
        if s == '.':
            flag = False
            continue
        if flag:
            floatNum = floatNum * 10.0 + float(s)
        else:
            floatNum = floatNum + (float(s) / t)
            t *= 10.0
    return floatNum

def findSalary(salary):
    data = []
    num = ''
    for s in salary:
        if s.isdigit() or s == '.':
            num = num + s
        elif len(num) != 0:
            #print(num)
            data.append(numstrTofloat(num))
            num = ''
    #print(data)
    return data

def getAvgSalary():
    # findSalary = re.compile(r'(\d*)')
    datalist = {}
    numlist = {}
    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()

    sql = "select distinct keyword from job"
    data = cur.execute(sql)
    for item in data:
        datalist[item[0]] = 0.0
        numlist[item[0]] = 0

    sql = "select keyword,salary from job"
    data = cur.execute(sql)

    for item in data:
        if len(item[1]) == 0:
            continue
        s = 0
        #print(item)
        salary = findSalary(item[1])

        #print(salary)

        #print(item[1][-1])
        if item[1][-1] == '年':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) / (2 * 12)
            else:
                s = salary[0] / 12
        elif item[1][-1] == '月':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) / 2
            else:
                s = salary[0]
            if isQian(item[1]) == True:
                s /= 10
        elif item[1][-1] == '天':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) * 30 / 10000
            else:
                s = salary[0] * 30 / 10000
        # print(s,'万/月')
        datalist[item[0]] += s
        numlist[item[0]] += 1
        # if item[0] == 'c++':
        #
        # elif item[0] == 'python':
        #
        # elif item[0] == 'java':
        #
        # elif item[0] == '大数据':
    # print(datalist)
    # print(numlist)
    for key in datalist.keys():
        datalist[key] = round(datalist[key]/numlist[key],2)
    #print(datalist)
    return list(datalist.keys()),list(datalist.values())

def getJob(tag,flag):   #flag==0时按照keyword搜索，flag==1时按照jname搜索
    datalist = []
    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()
    if tag == 'all':
        sql = "select * from job"
    else:
        if flag == 0:
            sql = "select * from job where keyword like %s"%("'%" + tag + "%'")
        elif flag == 1:
            sql = "select * from job where jname like %s" % ("'%" + tag + "%'")
    data = cur.execute(sql)
    for item in data:
        # print(item)
        datalist.append(item)
    cur.close()
    con.close()
    return datalist

def getSalary():
    # findSalary = re.compile(r'(\d*)')
    datalist = {}

    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()

    sql = "select distinct keyword from job"
    data = cur.execute(sql)
    for item in data:
        datalist[item[0]] = [0,0,0,0,0,0,0,0]

    sql = "select keyword,salary from job"
    data = cur.execute(sql)

    for item in data:
        if len(item[1]) == 0:
            continue
        s = 0
        #print(item)
        salary = findSalary(item[1])

        #print(salary)

        #print(item[1][-1])
        if item[1][-1] == '年':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) / (2 * 12)
            else:
                s = salary[0] / 12
        elif item[1][-1] == '月':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) / 2
            else:
                s = salary[0]
            if isQian(item[1]) == True:
                s /= 10
        elif item[1][-1] == '天':
            if len(salary) == 2:
                s = (salary[0] + salary[1]) * 30 / 10000
            else:
                s = salary[0] * 30 / 10000
        # print(s,'万/月')
        if s < 0.5:
            datalist[item[0]][0] += 1
        elif s < 1:
            datalist[item[0]][1] += 1
        elif s < 1.5:
            datalist[item[0]][2] += 1
        elif s < 2:
            datalist[item[0]][3] += 1
        elif s < 3:
            datalist[item[0]][4] += 1
        elif s < 4:
            datalist[item[0]][5] += 1
        elif s < 5:
            datalist[item[0]][6] += 1
        else:
            datalist[item[0]][7] += 1

    # print(datalist)

    #print(datalist)
    return datalist

def getExperience():
    # findSalary = re.compile(r'(\d*)')
    datalist = {}

    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()

    sql = "select distinct keyword from job"
    data = cur.execute(sql)
    for item in data:
        datalist[item[0]] = [0, 0, 0, 0, 0, 0]

    sql = "select keyword,experience from job"
    data = cur.execute(sql)

    for item in data:
        if item[1] == '在校生/应届生':
            datalist[item[0]][0] += 1
        elif item[1] == '无需经验':
            datalist[item[0]][1] += 1
        elif item[1] == '1年经验' or item[1] == '2年经验':
            datalist[item[0]][2] += 1
        elif item[1] == '3-4年经验':
            datalist[item[0]][3] += 1
        elif item[1] == '5-7年经验' or item[1] == '8-9年经验':
            datalist[item[0]][4] += 1
        elif item[1] == '10年以上经验':
            datalist[item[0]][5] += 1

    # print(datalist)

    # print(datalist)
    return datalist

def getEducate():
    datalist = {}

    con = sqlite3.connect("jobSpider/51job.db")
    cur = con.cursor()

    sql = "select distinct keyword from job"
    data = cur.execute(sql)
    for item in data:
        datalist[item[0]] = [0, 0, 0, 0, 0, 0]

    sql = "select keyword,educate from job"
    data = cur.execute(sql)

    for item in data:
        if item[1] == '初中及以下':
            datalist[item[0]][0] += 1
        elif item[1] == '中专' or item[1] == '中技' or item[1] == '高中':
            datalist[item[0]][0] += 1
        elif item[1] == '大专':
            datalist[item[0]][1] += 1
        elif item[1] == '本科':
            datalist[item[0]][2] += 1
        elif item[1] == '硕士':
            datalist[item[0]][3] += 1
        elif item[1] == '博士':
            datalist[item[0]][4] += 1
        else:
            datalist[item[0]][5] += 1

    # print(datalist)

    # print(datalist)
    return datalist