# -*- codeing = utf-8 -*-
# @Time : 2021/2/20 13:27
# @Author : wy
# @File : testKeyword.py
# @Software : PyCharm

from urllib import parse

keyword = parse.quote("大数据")
newKW = parse.quote(keyword)
print(newKW)