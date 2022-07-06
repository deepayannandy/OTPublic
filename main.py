from flask import Flask, render_template, request
import otsdb

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/employee/<emp>')
def employee(emp):
    print(emp)
    podetails = otsdb.getPoDetils(emp)
    if podetails == None:
        return render_template('DataNotFound.html', key="Page under Construction")
    else:
        return render_template('employee.html')
@app.route('/po/<ponum>')
def po(ponum):
    print(ponum)
    podetails=otsdb.getPoDetils(ponum)
    if podetails==None:
        return render_template('DataNotFound.html', key=ponum)
    else:
        return render_template('po.html',po=podetails)
@app.route('/wo/<wonum>')
def wo(wonum):
    print(wonum)
    wodetails = otsdb.getWoDetils(wonum)
    if wodetails == None:
        return render_template('DataNotFound.html', key=wonum)
    else:
        return render_template('wo.html', wo=wodetails)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)