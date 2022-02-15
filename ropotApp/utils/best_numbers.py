import sqlite3
from pathlib import Path
# ----------- Controller ---------------- #
from .vars import Vars

class BestNumber:
    def __init__(self):
        self.conf = Vars()

    # def getDublicatedNumbers(number):
    #     #Counts each character present in the string
    #     degree = 0
    #     for i in range(0, len(number)):
    #         count = 1
    #         for j in range(i+1, len(number)):
    #             if(number[i] == number[j] and number[i] != ' '):
    #                 count = count + 1
    #                 #Set string[j] to 0 to avoid printing visited character
    #                 number = number[:j] + '.' + number[j+1:]
    #
    #         #A character is considered as duplicate if count is greater than 1
    #         if(count > 1 and number[i] != '.'):
    #             degree = degree + count
    #             #print(number[i]+ " ==> " +str(count))
    #     return degree


    # def getNextDublicatedNo(number):
    #     count = 0
    #     for i in range(0, len(number)):
    #         try:
    #             if number[i] == number[i+1]:
    #                 count=+1
    #         except IndexError:
    #             a= 1
    #         #print(i)
    #     print(count)

    # -------------- regex ------------- #
    def get010n0(self,number):
        import re
        pattern = r"010[0-9]{1}0[0-9]{1}0[0-9]{4}"
        if re.match(pattern, number):

            print(number+"  ("+selectRegion(number)+")")

    def get01010(self,number):
        import re
        pattern = r"01010[0-9]{6}"
        if re.match(pattern, number):
            print(number+"  ("+selectRegion(number)+")")
    # ------------ sim regex -------------#
    def getDublicatedBlok3Numbers(self,number):
        # Counts each character present in the string
        for i in range(0, len(number)):
            try:
                # print(number[i: i + 3],number[i+3 : i+7])

                if number[i:i + 3] == number[i+3 : i+6] :

                    print(number)
                    break
            except IndexError:
                pass

    def getDublicatedBlok2Numbers(self,number):
        # Counts each character present in the string
        for i in range(0, len(number)):
            try:

                if number[i: i + 2]==number[i+2 : i+4] :
                    print(number + "  (" + selectRegion(number) + ")")
                    break
            except IndexError:
                pass

    # -------------- fillter ------------- #
    def getDublicatedNumbers(self,number):
        #Counts each character present in the string
        degree = 0
        for i in range(0, len(number)):
            count = 1

            for j in range(i+1, len(number)):
                if(number[i] == number[j] and number[i] != ' '):
                    count = count + 1
                    #Set string[j] to 0 to avoid printing visited character
                    number = number[:j] + '.' + number[j+1:]
                    # print(number)

            #A character is considered as duplicate if count is greater than 1
            if(count > 1 and number[i] != '.'):
                degree += count - 1
                # print(number[i]+ " ==> " +str(count - 1))
        return degree

    def getDublicatedNeigbNumbers(self,number):
        #Counts each character present in the string
        degree = 0
        for i in range(0, len(number)):
            try:
                if number[i] == number[i+1]:
                    degree+=1
            except IndexError:
                degree = 0
        return degree

    def getDublicatedSubNumbers(self,number):
        #Counts each character present in the string
        degree = 0
        for i in range(0, len(number)):
            try:
                if int(number[i]) - int(number[i+1]) == 1:
                    degree+=1
            except IndexError:
                degree = 0
        return degree

    def getDublicatedZerossNumbers(self,number):
        # Counts each character present in the string
        for i in range(0, len(number)):
            try:
                if int(number[i]) == 0 and number[i] == number[i + 1] :
                    print(number+"  ("+self.selectRegion(number)+")")
            except IndexError:
                pass

    def getDublicates(self,number):
        return  self.getDublicatedNumbers(number)+\
                self.getDublicatedNeigbNumbers(number)+\
                self.getDublicatedSubNumbers(number)

    # ----------------------------------- #