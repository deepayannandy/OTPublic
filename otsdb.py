import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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