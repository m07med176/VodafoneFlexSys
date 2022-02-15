from os import environ, path
environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
import django #@UnresolvedImport
django.setup()
from pymongo import MongoClient
import sqlite3,sys,os,psycopg2,datetime
# ----------- Controller ---------------- #
# from .vars import Vars
# from .vodafoneModel import VodafoneNumber
# from .best_numbers import BestNumber
# ----------- Models ---------------- #
from ropotApp.models import Area,Branch,ROR

client = MongoClient("mongodb+srv://biteam:Mohamed195825735@cluster0.3ccve.mongodb.net/vodafone_number?retryWrites=true&w=majority")
db = client.vodafone_number

# insert one row ----------------------------------------------
# db.items.insert_one({"name":"mohamed"})

# count all row -----------------------------------------------
# count_all = db.items.count_documents({})

# count specific row ------------------------------------------
# count = db.items.count_documents({"branch":"الدقهلية"})

# get one row -------------------------------------------------
def findItem():
    data = db.items.find_one({"number": "01050900289"})
    print(data != None)
    print(data)

# get more than row -------------------------------------------
# data = [i['number'] for i in db.items.find({"best": 8})]


# get distinct rows -------------------------------------------
# best = db.items.find({}).distinct('best')
#best = [i['best'] for i in db.items.find({}).distinct('best')]

# delete one --------------------------------------------------
# db.items.delete_one({ "address": "Mountain 21" }) 
# db.items.delete_many({})

# querry using regex ------------------------------------------
# myquery = { "address": {"$regex": "^S"} }
# best = db.items.find(myquery)

# update ------------------------------------------------------
# myquery = { "number": "01050900289" }
# newvalues = { "$set": { "is_valid":True} }
# db.items.update_one(myquery, newvalues)
# db.items.update_many(myquery, newvalues)

def migrations():
    for no,item in enumerate(db.items.find({"is_valid":None})):

        # condition = False
        # try:
        #     data = item["is_valid"]
        # except KeyError:
        #     condition = True
        # if condition:
        query = { "number": item["number"] }
        documnet = {
        "area":item["branch"],
        "branch":item["area"],
        "area_id":Area.objects.get(area_name=item["branch"]).id,
        "branch_id":Branch.objects.get(branch_name=item["area"]).id,

        "user_number":"",
        "is_reserved":False,
        "is_valid":True,
        "is_deleted":False,
        "is_new":True,
        "is_done":False,
        "is_available":False
        }
        newvalues = { "$set": documnet }
        db.items.update_one(query,newvalues)
        print(str(no)+" ==> "+item["number"] )
            

migrations()
#findItem()
