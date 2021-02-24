# -*- codeing = utf-8 -*-
# @Time : 2021/2/20 13:21
# @Author : wy
# @File : testBS.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import re

html = open("jobList.html","r")
bs = BeautifulSoup(html,"html.parser")

bs = bs.find_all("script",type="text/javascript")
job_list = str(bs[2])
print(bs[2])
findJob = re.compile(r'"is_special_job":(.*?)"adid"')

findJob_link = re.compile(r'"job_href":"(.*?)",')
findJname = re.compile(r'"job_name":"(.*?)",')
findClink = re.compile(r'"company_href":"(.*?)",')
findCname = re.compile(r'"company_name":"(.*?)",')
findSalary = re.compile(r'"providesalary_text":"(.*?)",')
findArea = re.compile(r'"workarea_text":"(.*?)",')
findUpdatedate = re.compile(r'"updatedate":"(.*?)",')
findCtype = re.compile(r'"companytype_text":"(.*?)",')
findCsize = re.compile(r'"companysize_text":"(.*?)",')
findCind = re.compile(r'"companyind_text":"(.*?)",')      #公司所在行业
#         educate text,
#         experience text,
info = re.compile(r'"attribute_text":\[(.*?)],')

count = 0
for j_list in re.findall(findJob,job_list):
    print(j_list)
    job_link = re.findall(findJob_link,j_list)
    #print(job_link[0].replace("\\",""))
    count += 1
print(count)


#resultList = bs.select("#app")
# bs = str(bs)
# res = re.findall(find,bs)
# print(res[0])
# eldiv = bs.select(".er")
# print(eldiv)