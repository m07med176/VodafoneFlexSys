class VodafoneNumber:
    def __init__(self,id="",number="",area="",main_area="",strip="",dateOfRecord="",version="",best="",reviewer="",deleted=""):
        self.id=id
        self.number = number
        self.area=area
        self.main_area=main_area
        self.strip=strip
        self.dateOfRecord=dateOfRecord
        self.version=version
        self.best=best
        self.reviewer=reviewer
        self.deleted=deleted

    def getId(self):
        return id
    
    def setId(self,id):
        self.id = id
    
    def getNumber(self,):
        return self.number
    
    def setNumber(self,number):
        self.number = number
    
    def  getArea(self):
        return self.area
    

    def setArea(self,area):
        self.area = area
    

    def  getMain_area(self):
        return self.main_area
    

    def setMain_area(self,main_area):
        self.main_area = main_area
    

    def  getStrip(self):
        return self.strip
    

    def setStrip(self,strip):
        self.strip = strip
    

    def  getDateOfRecord(self):
        return self.dateOfRecord
    

    def setDateOfRecord(self,dateOfRecord):
        self.dateOfRecord = dateOfRecord
    

    def getVersion(self):
        return self.version
    

    def setVersion(self,version):
        self.version = version
    

    def getBest(self):
        return self.best
    

    def setBest(self,best):
        self.best = best
    

    def  getReviewer(self):
        return self.reviewer
    

    def setReviewer(self,reviewer):
        self.reviewer = reviewer
    

    def isDeleted(self):
        return self.deleted
    

    def setDeleted(self,deleted):
        self.deleted = deleted
    
    def toJSON(self):
        return {
            "id":self.id,
            "number":self.number,
            "area":self.area,
            "main_area":self.main_area,
            "strip":self.strip,
            "dateOfRecord":self.dateOfRecord,
            "version":self.version,
            "best":self.best,
            "reviewer":self.reviewer,
            "deleted":self.deleted
        }
