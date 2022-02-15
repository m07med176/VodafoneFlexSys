import requests
import json
class Notification:
    def __init__(self):
        self.BASE = "https://fcm.googleapis.com/fcm/send"
        
        key = "AAAAxsHIIUg:APA91bH_S-BoeQ5Jg0egog3EDA7Xanm9yeyvgoQLS7PdfIbgrPtsaF6CqAgD_D9aYHIVHVIsQxK_IvUPh8v2Nvtm7bc_D4wh1N8mUX2UkRn0zpCbcTUSOOU8NXRg3SC302dpydOZQEka"
        
        self.headers={"Content-Type":"application/json","Authorization":f"key={key}"}
        
     
    def sendNotification(self,title,message):
        data ={
            "data":{
                "title":title,
                "message":message
            },
            "to":"/topics/myTopic2"
        }
        response = requests.post(self.BASE,headers=self.headers, data=json.dumps(data))
        return response.content

if __name__ == "__main__":
    n = Notification()
    data = n.sendNotification("mohamed","this is message")
    print(data)