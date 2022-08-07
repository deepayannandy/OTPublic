from flask import Flask, render_template, request
import otsdb

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/employee/<emp>')
def employee(emp):
    print(emp)
    unique=emp.split("(")[0]
    res = otsdb.db.collection("users").where("uniqueid", "==", unique).get()
    if len(res)==0:
        return render_template('DataNotFound.html', key="User data not available")
    else:
        user = res[0].to_dict()
        timecard= otsdb.getEmpTimesheet(user["uid"])
        print(timecard)
        return render_template('employee.html',user=user,card=timecard)
@app.route('/eq/<eqid>')
def eqp(eqid):
    print(eqid)
    res = otsdb.db.collection("equipments").where("eqId", "==", eqid).get()
    if len(res)==0:
        return render_template('DataNotFound.html', key="Equipment data not available")
    else:
        eq = res[0].to_dict()
        return render_template('EQP.html',eq=eq)
@app.route('/con/<conid>')
def con(conid):
    print(conid)
    res = otsdb.db.collection("consumableItems").where("conId", "==", conid).get()
    if len(res)==0:
        return render_template('DataNotFound.html', key="Equipment data not available")
    else:
        con = res[0].to_dict()
        return render_template('CON.html',con=con)
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
@app.route('/invoice/<wonum>')
def invoice(wonum):
    print(wonum)
    wodetails = otsdb.getWoDetils(wonum)
    if wodetails == None:
        return render_template('DataNotFound.html', key=wonum)
    else:
        return render_template('invoice.html', wo=wodetails)

if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=False, host='0.0.0.0', port=80)
    serve(app, host="0.0.0.0", port=8080)