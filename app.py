from flask import Flask,render_template,request

import jobFunction as jf

app = Flask(__name__)

@app.route('/')
def index():
    jobnums = jf.getJobnum()
    # print(jobnums)
    avgkeys,avgvalues = jf.getAvgSalary()
    # print(avgkeys)
    # print(avgvalues)
    return render_template('index.html',jobnums=jobnums,avgkeys=avgkeys,avgvalues=avgvalues)

# @app.route('/test')
# def test():
#     return render_template('test.html')

@app.route('/index.html')
def home():
    return index()

@app.route('/tables.html')
def table():
    datalist = jf.getJob('all',0)
    return render_template('tables.html', jobs=datalist)

@app.route('/search.html',methods=['POST','GET'])
def search_tag():
    if request.method == 'POST':
        result = request.form.to_dict()
        datalist = jf.getJob(result['tag'],1)
    else:
        datalist = jf.getJob('all')
    return render_template('tagSearch.html',jobs=datalist,tag=result['tag'])

@app.route('/python.html')
def tag_python():
    datalist = jf.getJob('python',0)
    dSalary = jf.getSalary()['python']
    dExperience = jf.getExperience()['python']
    dEducate = jf.getEducate()['python']
    return render_template('tag.html', jobs=datalist,tag='Python',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/c++.html')
def tag_cplus():
    datalist = jf.getJob('c++',0)
    dSalary = jf.getSalary()['c++']
    dExperience = jf.getExperience()['c++']
    dEducate = jf.getEducate()['c++']
    return render_template('tag.html', jobs=datalist,tag='C++',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/java.html')
def tag_java():
    datalist = jf.getJob('java',0)
    dSalary = jf.getSalary()['java']
    dExperience = jf.getExperience()['java']
    dEducate = jf.getEducate()['java']
    return render_template('tag.html', jobs=datalist,tag='Java',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/bigdata.html')
def tag_bigdata():
    datalist = jf.getJob('大数据',0)
    dSalary = jf.getSalary()['大数据']
    dExperience = jf.getExperience()['大数据']
    dEducate = jf.getEducate()['大数据']
    return render_template('tag.html', jobs=datalist,tag='大数据',
                           dSalary=dSalary,dExperience=dExperience,dEducate=dEducate)

@app.route('/salaryCharts.html')
def salaryCharts():
    datalist = jf.getSalary()
    pythonS = datalist['python']
    cplusS = datalist['c++']
    javaS = datalist['java']
    bigdataS = datalist['大数据']
    return render_template('salaryCharts.html',
                           pythonS=pythonS,cplusS=cplusS,
                           javaS=javaS,bigdataS=bigdataS)


@app.route('/experienceCharts.html')
def experienceCharts():
    datalist = jf.getExperience()
    pythonE = datalist['python']
    cplusE = datalist['c++']
    javaE = datalist['java']
    bigdataE = datalist['大数据']
    return render_template('experienceCharts.html',
                           pythonE=pythonE, cplusE=cplusE,
                           javaE=javaE, bigdataE=bigdataE
                           )


@app.route('/educateCharts.html')
def educateCharts():
    datalist = jf.getEducate()
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
