import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import  dateCalculator as dc

cred = credentials.Certificate("ots-pocket-firebase-adminsdk-5q0jt-fceeeffe12.json")
firebase_admin.initialize_app(cred)

db=firestore.client()

def getPoDetils(ponumber):
    res = db.collection("userProjects").where("po", "==", ponumber).get()
    if len(res)!=0:
        return res[0].to_dict()
    else:
        return None

def getWoDetils(wonumber):
    res = db.collection("Workorders").where("wo", "==", wonumber).get()
    if len(res) != 0:
        return res[0].to_dict()
    else:
        return None
def getEmpTimesheet(empid):
    days,week=dc.getDaysinWeek()
    dates=[]
    weekdays=[]
    card=[]
    for day in days:
        res = db.collection(empid+"-timecards").where("date", "==", day.strftime("%Y-%m-%d")).get()
        if len(res)==0:
            card.append(["NA","NA","NA","NA"])
        else:
            usercard=res[0].to_dict()
            if usercard["shift"]:
                card.append([str(usercard["st"]),str(usercard["ot"]),"0","0"])
            else:
                card.append([ "0", "0",str(usercard["st"]), str(usercard["ot"])])
        dates.append(day.strftime("%d/%m/%Y"))
        weekdays.append(dc.getWeekDayStr(day))

    finalCard=[weekdays,dates,card,week]
    print(finalCard)
    return finalCard

# getEmpTimesheet("QfCV0Snm1dc23Dfm1ycMnN0s4ZG2")