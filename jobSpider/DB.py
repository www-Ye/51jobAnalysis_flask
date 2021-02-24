# -*- codeing = utf-8 -*-
# @Time : 2021/2/20 12:53
# @Author : wy
# @File : DB.py
# @Software : PyCharm

import sqlite3
import os

dbpath = "./51job.db"

def init_db(dbpath):
    if os.path.exists(dbpath):
        print("数据库已存在")
    else:
        sql = '''
            create table job
            (
            id integer primary key autoincrement,
            keyword text,
            job_link text,
            jname varchar ,
            c_link text,
            cname varchar,
            salary text,
            area text,
            updatedate text,
            ctype text,
            csize text,
            cind text,
            experience text,
            educate text,
            need text
            )
        '''    #创建数据表
        conn = sqlite3.connect(dbpath)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
        print("数据库创建成功")

#init_db(dbpath)

def saveData(datalist,dbpath):
    #init_db(dbpath)
    print("开始存入数据。。。")

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    index = 1
    for data in datalist:
        # sql = "insert into job (id) values (%d)"%index
        # cur.execute(sql)
        for key in data.keys():
            data[key] = '"' + data[key] + '"'
        #     #print(key,data[key])
        #     sql = '''
        #         update job set %s=%s
        #         where id=%d
        #     '''%(key,'"' + data[key] + '"',index)
        #     print(sql)
        #     cur.execute(sql)
        print("存入第%d条数据"%index)
        index += 1
        sql = '''
            insert into job
            (keyword, job_link, jname, c_link, cname, salary, area, 
            updatedate, ctype, csize, cind,
            experience, educate ,need)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''%(data["keyword"],data["job_link"],data["jname"],data["c_link"],data["cname"],
             data["salary"],data["area"],data["updatedate"],data["ctype"],
             data["csize"],data["cind"],data["experience"],data["educate"],
             data["need"])
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("数据已存入数据库")