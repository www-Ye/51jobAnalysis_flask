# -*- codeing = utf-8 -*-
# @Time : 2021/2/20 12:49
# @Author : wy
# @File : spider.py
# @Software : PyCharm

'''
制作流程
1 爬取数据      spider.py
爬取列表
爬取详情
2 数据保存      51job.db
保存列表
保存详情
3 搭建框架      app.py 路由   templates 页面    static 素材（图片、css、js）
前端页面
列表展示
4 制作图表      echarts.js  
Echarts
- 柱形图
- 饼形图
'''

import DB
from bs4 import  BeautifulSoup
import re
import urllib.request, urllib.error
from urllib import parse


# kw = input("请输入你要搜索的网页关键字:")
# keyword = parse.quote(parse.quote(kw))
# pageNum = 1
#https://search.51job.com/list/020000,000000,0000,00,9,99,python,2,1.html

dbpath = "./51job.db"

#主流程
def main():
    kw = input("请输入你要搜索的网页关键字:")

    baseurl = "https://search.51job.com/list/020000,000000,0000,00,9,99,"

    DB.init_db(dbpath)  #数据库初始化
    #url = "https://search.51job.com/list/020000,000000,0000,00,9,99," + keyword +",2,"+ str(pageNum) +".html"
    #html = askURL(url)

    datalist = []
    datalist = getData(baseurl,kw)

    DB.saveData(datalist,dbpath)

findJob = re.compile(r'"is_special_job":(.*?)"adid"')
findJob_link = re.compile(r'"job_href":"(.*?)",')
findJname = re.compile(r'"job_name":"(.*?)",')
findC_link = re.compile(r'"company_href":"(.*?)",')
findCname = re.compile(r'"company_name":"(.*?)",')
findSalary = re.compile(r'"providesalary_text":"(.*?)",')
findArea = re.compile(r'"workarea_text":"(.*?)",')
findUpdatedate = re.compile(r'"updatedate":"(.*?)",')
findCtype = re.compile(r'"companytype_text":"(.*?)",')
findCsize = re.compile(r'"companysize_text":"(.*?)",')
findCind = re.compile(r'"companyind_text":"(.*?)",')      #公司所在行业
#         educate text,
#         experience text,
findInfo = re.compile(r'"attribute_text":\[(.*?)],')
findExperience = re.compile(r'"(.*?)年经验",')
findEducate = re.compile(r'"(.*?)科",')
finde = re.compile(r'","(.*?)","(.*?)","')
finde2 = re.compile(r'","(.*?)","')
findNeed = re.compile(r'"招(.*?)人"')


#爬取网页
def getData(baseurl,kw):

    print("开始爬取。。。")
    keyword = parse.quote(parse.quote(kw))
    datalist = []
    pageNum = 1
    while(True):
        url = baseurl + keyword + ",2,"+ str(pageNum) +".html"
        print("page:%d:"%pageNum)
        pageNum += 1
        html = askURL(url)      #保存获取到的网页源码
        #print(html)
        # if pageNum == 3:
        #     break
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        soup = soup.find_all("script",type="text/javascript")
        job_lists = str(soup[2])
        count = 0
        for j_list in re.findall(findJob, job_lists):
            dict = {}
            dict["keyword"] = kw

            #存入工作链接
            job_link = re.findall(findJob_link,j_list)
            job_link = job_link[0].replace("\\","")
            dict["job_link"] = job_link

            jname = re.findall(findJname,j_list)
            dict["jname"] = jname[0].replace("\\","")

            c_link = re.findall(findC_link,j_list)
            c_link = c_link[0].replace("\\", "")
            dict["c_link"] = c_link

            cname = re.findall(findCname,j_list)
            dict["cname"] = cname[0].replace("\\", "")

            salary = re.findall(findSalary,j_list)
            dict["salary"] = salary[0].replace("\\","")

            area = re.findall(findArea,j_list)
            dict["area"] = area[0]

            updatedate = re.findall(findUpdatedate,j_list)
            dict["updatedate"] = updatedate[0]

            ctype = re.findall(findCtype,j_list)
            dict["ctype"] = ctype[0]

            csize = re.findall(findCsize,j_list)
            dict["csize"] = csize[0]

            cind = re.findall(findCind,j_list)
            dict["cind"] = cind[0].replace("\\","")     # 公司所在行业

            info = re.findall(findInfo,j_list)[0]
            #tempInfo = info[0].replace('"','').split(",")
            #print(info)

            temp = re.findall(finde, info)
            #经验和学历可能两者皆有也可能只有一个还有可能都没有
            if len(temp) == 1:
                temp = temp[0]
                dict["experience"] = temp[0].replace("\\", "")
                dict["educate"] = temp[1]
            else:
                temp = re.findall(finde2,info)
                if len(temp) == 1:
                    temp = temp[0]
                    if temp != "大专" and temp != "本科" and temp != "硕士" and temp != "博士":
                        dict["experience"] = temp.replace("\\", "")
                        dict["educate"] = ""
                    else:
                        dict["experience"] = ""
                        dict["educate"] = temp
                else:
                    dict["experience"] = ""
                    dict["educate"] = ""


            #print(temp[0],temp[1])
            # if len(temp) == 2:
            #     dict["experience"] = temp[0].replace("\\","")
            #     dict["educate"] = temp[1]
            # elif len(temp) == 1:
            #     dict["experience"] = temp[0].replace("\\", "")
            #     dict["educate"] = ""
            dict["need"] = "招" + re.findall(findNeed, info)[0] + "人"
            #dict["need"] = tempInfo[3]

            # dict["experience"] = re.findall(findExperience,info)
            # dict["educate"] = re.findall(findEducate,info)
            # dict["need"] = re.findall(findNeed,info)
            #print("经验：",dict["experience"],"学历：",dict["educate"],"招人数：",dict["need"])
            #print(info[0].replace('"','').split(","))

            count += 1
            print(dict)
            datalist.append(dict)


        print(count)
        if count == 0:
            break
        #print(count)

    print("一共%d条%s数据"%(len(datalist),keyword))
    #print(datalist)
    return datalist

#获取所有工作岗位的链接
# def getLink():
#     return []

#得到指定一个URL的网页内容
def askURL(url):
    head = {    #模拟浏览器头部信息，向51job服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3"
    }

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gbk")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html

if __name__ == "__main__":
    main()
    print("爬取结束")