import sqlite3,sys,os,psycopg2,datetime,json
# ----------- Controller ---------------- #
from .vars import Vars
from .vodafoneModel import VodafoneNumber
from .best_numbers import BestNumber
# ----------- Models ---------------- #
from ropotApp.models import Area,Branch,ROR
from .notification import Notification

from pymongo import MongoClient
from bson.objectid import ObjectId

class DatabaseManager:
    def __init__(self):
        self.conf = Vars()
        self.best = BestNumber()
        client = MongoClient("mongodb+srv://biteam:Mohamed195825735@cluster0.3ccve.mongodb.net/vodafone_number?retryWrites=true&w=majority")
        self.modb = client.vodafone_number
                            ## vars ##

    # region MONGO Database
    def getCountArea(self,area):
       return self.modb.items.count_documents({"area":area,"is_deleted":False})

    def getCountBranch(self,branch):
       return self.modb.items.count_documents({"branch":branch,"is_deleted":False})

    def updateValidation(self,phoneNumber,is_valid):
        query = { "number": phoneNumber }
        if is_valid:
            newvalues = { "$set": { "is_valid": is_valid } }
        else:
            newvalues = { "$set": { "is_valid": False,"is_reserved": False,"is_available":False,"is_new":False,"is_deleted":True} }

        self.modb.items.update_one(query,newvalues)

    
    def updateCheckDone(self,phoneNumber,is_checked=True):
        query = { "number": phoneNumber }
        newvalues = { "$set": { "is_checked": is_checked } }
        self.modb.items.update_one(query,newvalues)
    
    def updateDone(self,phoneNumber,is_done):
        query = { "number": phoneNumber }
        newvalues = { "$set": { "is_done":is_done} }
        self.modb.items.update_one(query,newvalues)
        if is_done: return {"message":"تم شراء الرقم ","status":True}
        else:  return {"message":"شراء فاشل","status":True}

    def deleteNumber(self,number):
        self.modb.items.delete_one({ "number": number })
        # Notification().sendNotification("حذف",f"تم حذف رقم  {number} ")
        
    def updateReservation(self,phoneNumber,userNumber):
        query = { "number": phoneNumber }
        newvalues = { "$set": { "is_reserved": True,"user_number":userNumber} }

        self.modb.items.update_one(query,newvalues)
        return  {"message":"تم حجز الرقم وجارى التحقق من صلاحيتها والتواصل معك","status":True}
        
    def showNumbers(self,querry):
        # to delete page if apear
        _ = querry.pop("page") if "page" in querry.keys() else 0
        order = querry.pop("order") if "order" in querry.keys() else "best"
        if "number" in querry.keys():
            querry["number"]  = querry["number"].replace('"','').replace("'","")

        if "user_number" in querry.keys(): 
            querry["user_number"]  = querry["user_number"].replace('"','').replace("'","")

        if "number_regex" in querry.keys():
            querry["number"] = {"$regex": querry["number_regex"]}
            querry.pop("number_regex")

        array = []
        for i in self.modb.items.find(querry).sort(order, -1):
            i.update({"_id":""})
            array.append(i)
        return array

    def insertInDatabase(self,number,area,branch):
        if len(number) > 30: return 
        dateNow = datetime.datetime.now().date()

        querry = self.modb.items.find_one({"number": number})
        if querry == None :# querry number 
            degree = 0
            try: degree = self.best.getDublicates(number)
            except Exception as e:print("insert numbers in Database Error: " + str(e))

            documnet = {
                "number":number,
                "best":degree,

                "area":area,
                "branch":branch,
                "area_id":Area.objects.get(area_name=area).id,
                "branch_id":Branch.objects.get(branch_name=branch).id,

                "user_number":"",
                "is_reserved":False,
                "is_valid":True,
                "is_deleted":False,
                "is_new":True,
                "is_done":False,
                "is_available":False,

                "dateRecord":str(dateNow),
                "version":str(dateNow)
            }
            self.modb.items.insert_one(documnet)

        else: # if is old just update
            query = { "number": number }
            documnet = { "is_new":False,"version":str(dateNow) }
            newvalues = { "$set": documnet }
            self.modb.items.update_one(query,newvalues)
            
     
    def getDegrees(self,number):
        try: 
            return  self.best.getDublicates(number)
        except Exception as e:
            print("insert numbers in Database Error: " + str(e))
            return 0
        
    def insertInDatabaseAdapter(self,webNumbers,area,branch):
        dateNow = datetime.datetime.now().date()

        databaseNumbers = [item['number'] for item in self.modb.items.find({"area":area,"branch":branch})]
        
        oldNumbers = list(set(webNumbers).intersection(databaseNumbers))
        newNumbers = list(set(webNumbers).difference(databaseNumbers))
        deleteNumbers = list(set(databaseNumbers).difference(webNumbers))

        if len(newNumbers) != 0:
            try:
                bulkInsert = []
                for new in newNumbers:
                    documnet = {
                            "number":new,
                            "best":self.getDegrees(new),

                            "area":area,
                            "branch":branch,
                            "area_id":Area.objects.get(area_name=area).id,
                            "branch_id":Branch.objects.get(branch_name=branch).id,

                            "user_number":"",
                            "is_reserved":False,
                            "is_valid":True,
                            "is_deleted":False,
                            "is_new":True,
                            "is_done":False,
                            "is_available":False,

                            "dateRecord":str(dateNow),
                            "version":str(dateNow)
                        }
                    bulkInsert.append(documnet)
                
                self.modb.items.insert_many(bulkInsert)
                print("data inseterted")
            except Exception as e: print("inseterted error"+str(e) )

        if len(oldNumbers) != 0:
            try:
                query = {'number': {"$in": oldNumbers}}
                documnet = { "is_new":False,"version":str(dateNow) }
                newvalues = { "$set": documnet }
                self.modb.items.update_many(query,newvalues)
                print("data is updated")
            except Exception as e: print("updated error"+str(e) )

        if len(deleteNumbers) != 0:
            try:
                query = {'number': {"$in": deleteNumbers}}
                self.modb.items.delete_many(query)
                print("data is deleted")
            except Exception as e: print("deleted error"+str(e) )

    # endregion MONGO Database

    # region Django Database
    def recordOfDatabase(self):
        date_record = datetime.datetime.now().date()
        ROR.objects.update_or_create(
            date_record=date_record, 
            defaults={ 'date_record' :date_record } 
            )
   
    def setAreas(self, areas):
        for area in areas:
            Area.objects.update_or_create(
                area_name=area,
                defaults={ 'area_name' :area } 
                )

    def setBranches(self, branches, area):
        for branch in branches:
            area_id = Area.objects.get(area_name=area).id
            Branch.objects.update_or_create(
                branch_name=branch,
                defaults={ 'branch_name' :branch,'area_id':area_id }
                )
  
    def getSelectedAreas(self):
        data = Area.objects.filter(selected=True).values('area_name')
        return [i['area_name'] for i in data]
 
    def getSelectedBranches(self,area):
        area_id = Area.objects.get(area_name=area).id
        data = Branch.objects.filter(selected=True,area_id=area_id).values('branch_name')
        return [i['branch_name'] for i in data]
    # endregion Django Database

    # region Postgree Database
    def deleteAllNumbersInServer(self,table = "VodafoneNumberShow"):
            try:
                connection = psycopg2.connect(
                    host="ec2-34-254-69-72.eu-west-1.compute.amazonaws.com",
                    database="d84lv9hqj4cvad",
                    user="pkekjaplofajah",
                    password="5f23b729fd13ec1e966727ead1da9717e48c44bd830a6753ee23f54e14d3b099")
                cursor = connection.cursor()
                
                password = 'm195825735'
                password2 = input("please put password to continue: ").strip()

                if password != password2:
                        print("sorry we can not delete.")
                        return

                sql = f'DELETE FROM public."{table}";'

                cursor.execute(sql)
                connection.commit()
                print(f"{table} was deleted successfully.")
                return 

            except (Exception, psycopg2.Error) as error:
                print( "Error while fetching data from PostgreSQL", error)

            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
        
    def getCustomerRest(self,id):
            try:
                connection = psycopg2.connect(
                    host="ec2-34-254-69-72.eu-west-1.compute.amazonaws.com",
                    database="d84lv9hqj4cvad",
                    user="pkekjaplofajah",
                    password="5f23b729fd13ec1e966727ead1da9717e48c44bd830a6753ee23f54e14d3b099")
                cursor = connection.cursor()
                
                
                sql = f"""SELECT COALESCE(
                    (SELECT COALESCE(SUM(transactions_record.value),0) FROM transactions_record WHERE transactions_record."isDown" = false AND transactions_record."isDone" = false AND transactions_record."customerData_id" = {id} )
                    -
                    (SELECT COALESCE(SUM(transactions_record.value),0) FROM transactions_record WHERE transactions_record."isDown" = true AND transactions_record."isDone" = false AND transactions_record."customerData_id" = {id} )
                    ,0) AS rest """
                
                cursor.execute(sql)
                date = str(datetime.datetime.now().date())
                time = str(datetime.datetime.now().time()).split(".")[0]
                value =cursor.fetchone()[0]
                
                sql = f"""
                INSERT INTO transactions_rest (value,customer_id,date,time) VALUES(
                {value},{id},'{date}','{time}') 
                ON CONFLICT (customer_id) 
                DO UPDATE SET VALUE = {value},date = '{date}',time ='{time}';
                """
                cursor.execute(sql)
                connection.commit()
                return value

            except (Exception, psycopg2.Error) as error:
                print( "Error while fetching data from PostgreSQL", error)

            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()

    def uploadVodafoneNumberFromGovern(self):
            try:
                connection = psycopg2.connect(
                    host="ec2-34-254-69-72.eu-west-1.compute.amazonaws.com",
                    database="d84lv9hqj4cvad",
                    user="pkekjaplofajah",
                    password="5f23b729fd13ec1e966727ead1da9717e48c44bd830a6753ee23f54e14d3b099")
                cursor = connection.cursor()
                data = self.selectNumberFromGovern()
                for i in data:

                    insert = f"""
                    insert into public."VodafoneNumberShow" (
                        "number",
                        area,
                        branch,
                        self.best ,
                        reviewer ,
                        "version" ,
                        date_record ,
                        deleted ) values (
                            '{i.getNumber()}',
                            '{i.getMain_area()}',
                            '{i.getArea()}',
                            '{i.getBest()}',
                            '{i.getReviewer()}',
                            '{i.getVersion()}',
                            '{i.getDateOfRecord()}',
                            '{i.isDeleted()}'
                            );
                        """
                    cursor.execute(insert)
                    connection.commit()            
                return 

            except (Exception, psycopg2.Error) as error:
                return "Error while fetching data from PostgreSQL"+ error

            finally:
                # closing database connection.
                if connection:
                    cursor.close()
                    connection.close()
    # endregion ostgree Database





