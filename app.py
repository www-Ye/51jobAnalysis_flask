from flask import Flask,render_template,request
import sqlite3



app = Flask(__name__)

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

@app.route('/')
def index():
    jobnums = getJobnum()
    # print(jobnums)
    avgkeys,avgvalues = getAvgSalary()
    # print(avgkeys)
    # print(avgvalues)
    return render_template('index.html',jobnums=jobnums,avgkeys=avgkeys,avgvalues=avgvalues)

# @app.route('/test')
# def test():
#     return render_template('test.html')

@app.route('/index.html')
def home():
    return index()

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

@app.route('/tables.html')
def table():
    datalist = getJob('all',0)
    return render_template('tables.html', jobs=datalist)

@app.route('/search.html',methods=['POST','GET'])
def search_tag():
    if request.method == 'POST':
        result = request.form.to_dict()
        datalist = getJob(result['tag'],1)
    else:
        datalist = getJob('all')
    return render_template('tagSearch.html',jobs=datalist,tag=result['tag'])

@app.route('/python.html')
def tag_python():
    datalist = getJob('python',0)
    dSalary = getSalary()['python']
    dExperience = getExperience()['python']
    dEducate = getEducate()['python']
    return render_template('tag.html', jobs=datalist,tag='Python',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/c++.html')
def tag_cplus():
    datalist = getJob('c++',0)
    dSalary = getSalary()['c++']
    dExperience = getExperience()['c++']
    dEducate = getEducate()['c++']
    return render_template('tag.html', jobs=datalist,tag='C++',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/java.html')
def tag_java():
    datalist = getJob('java',0)
    dSalary = getSalary()['java']
    dExperience = getExperience()['java']
    dEducate = getEducate()['java']
    return render_template('tag.html', jobs=datalist,tag='Java',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/bigdata.html')
def tag_bigdata():
    datalist = getJob('大数据',0)
    dSalary = getSalary()['大数据']
    dExperience = getExperience()['大数据']
    dEducate = getEducate()['大数据']
    return render_template('tag.html', jobs=datalist,tag='大数据',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

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

@app.route('/salaryCharts.html')
def salaryCharts():
    datalist = getSalary()
    pythonS = datalist['python']
    cplusS = datalist['c++']
    javaS = datalist['java']
    bigdataS = datalist['大数据']
    return render_template('salaryCharts.html',
                           pythonS=pythonS,cplusS=cplusS,
                           javaS=javaS,bigdataS=bigdataS)

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


@app.route('/experienceCharts.html')
def experienceCharts():
    datalist = getExperience()
    pythonE = datalist['python']
    cplusE = datalist['c++']
    javaE = datalist['java']
    bigdataE = datalist['大数据']
    return render_template('experienceCharts.html',
                           pythonE=pythonE, cplusE=cplusE,
                           javaE=javaE, bigdataE=bigdataE
                           )

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

@app.route('/educateCharts.html')
def educateCharts():
    datalist = getEducate()
    pythonE = datalist['python']
    cplusE = datalist['c++']
    javaE = datalist['java']
    bigdataE = datalist['大数据']
    return render_template('educateCharts.html',
                           pythonE=pythonE, cplusE=cplusE,
                           javaE=javaE, bigdataE=bigdataE
                           )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
