from flask import Flask, render_template, request
import otsdb
from datetime import date
import random



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
        stc=95
        otc=142.5
        wodet=otsdb.getWoDetils(wonum)
        proj=otsdb.getPoDetils(wodet["po"])
        today = date.today()
        d1 = today.strftime("%m/%d/%Y")
        listOfEmp=wodet["assignedEmployee"]
        print(listOfEmp)
        empdata=[]
        for emp in listOfEmp:
            res = otsdb.db.collection("users").where("uniqueid", "==", emp.split("(")[0]).get()
            if len(res) != 0:
                empdata.append(res[0].to_dict())
            else:
                pass
        timecardData=[]
        total = 0
        tcInvoice = []
        for emp in empdata:
            res = otsdb.db.collection(emp["uid"]+"-timecards").where("wo", "==", wodet["po"]+"~"+wonum).get()
            for x in range(0, len(res)):
                tc=res[x].to_dict()
                if tc['st'] > 0:
                    tcInvoice.append({"date": tc['date'], "item": proj['jobDescriptions'], "desc":emp["fullname"]+" (ST)","qnt":tc['st'],'rate':stc,"total":stc*tc['st']})
                    total+=stc*tc['st']
                if tc['ot'] > 0:
                    tcInvoice.append({"date": tc['date'], "item": proj['jobDescriptions'], "desc":emp["fullname"]+" (OT)","qnt":tc['ot'],'rate':otc,"total":otc*tc['ot']})
                    total+=otc*tc['ot']
        print(tcInvoice,"\n",total)



        return render_template('invoice.html', wo=wodet["wo"], po=wodet["po"],proj=proj,date=d1,inv=random.randint(0, 99),invoice=tcInvoice,total=total)

if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=False, host='0.0.0.0', port=80)
    serve(app, host="0.0.0.0", port=8080)