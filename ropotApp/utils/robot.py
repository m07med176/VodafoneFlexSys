# python utils
import numbers
from time import sleep
import sqlite3,json,os,datetime
from pathlib import Path
# main selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# firefox selenium
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
# custom classes
from .vars import Vars
from .databaseManager import DatabaseManager
from .notification import Notification
# ------ Django ---------#
from ropotApp.models import Config,ScrappingLogs
import random
class Robot:
    def __init__(self):
        self.user = Config.objects.get(name='user').content
        self.password = Config.objects.get(name='password').content
        
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.db = DatabaseManager()
        self.conf = Vars()

    # region Utils
    def startAppException(self):
        try: self.startApp()
        except Exception as e: self.insertMessage(msg = str(e))

    def insertMessage(self,title="سحب",msg="",notify = False,type = 0):
        print(msg)
        if notify: Notification().sendNotification(title,msg)
        message         = ScrappingLogs()
        message.name    = title
        message.content = msg
        message.type    = type
        message.save()
    # endregion Utils

    # region Custom Main Scrapping
    def navigateToFlex(self, driver,id_key='id'):
        driver.get(self.conf.target_flex)
        self.insertMessage(msg = "تم الدخول لصفحه حجز الخطوط")
        # ----------------------------------------- #
        id = Config.objects.get(name=id_key).content
        driver.find_elements(By.CSS_SELECTOR, self.conf.idInput)[0].clear()
        driver.find_elements(By.CSS_SELECTOR, self.conf.idInput)[0].send_keys(id)
        driver.find_elements(By.CSS_SELECTOR, self.conf.nextBtn)[0].click()

        try:
            msg = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.alert)))
            if len(msg) !=0:
                if "alert-danger" in msg[0].get_attribute("class"):
                    model  = Config.objects.get(name=id_key)
                    model.content = id[:-4]+ str(random.randrange(1000, 9000, 4))
                    model.save()
                    self.navigateToFlex(driver,id_key)
        except Exception as e: print(e)
        self.insertMessage(msg = "تم كتابه كتابه الرقم القومى والدخول على صفحه الخطوط")
        driver.implicitly_wait(1)
        # ----------------------------------------- #

    def preparePage(self,id_key='id'):
        self.db.recordOfDatabase()
        self.insertMessage(msg = "البرنامج بدأ..")
        # ----------------------------------------- #
        driver = self.web_driver() # firefox_driver # web_driver firefox_driver_wind
        self.insertMessage(msg = "جارى تهيئة البرنامج ..")
        # ----------------------------------------- #
        # login to your account
        is_login = self.load_cookies(driver,self.conf.target_flex,self.conf.loginBtn)
        if is_login == False: self.login(driver)

        self.insertMessage(msg = "تم تسجيل الدخول")
        # ----------------------------------------- #
        self.navigateToFlex(driver,id_key)
        return driver

    def goBack(self,driver):
        backBtn = driver.find_elements(By.CSS_SELECTOR,self.conf.backbtn)[0]# backBtn.click()
        driver.execute_script("arguments[0].click();", backBtn)
        driver.implicitly_wait(5)

    def goNext(self,driver):
        nextBtn = driver.find_elements(By.CSS_SELECTOR,self.conf.nextBtn)[0]# backBtn.click()
        driver.execute_script("arguments[0].click();", nextBtn)
        driver.implicitly_wait(5)
        

        # Areas and Branches Scrapping
    def login(self,driver):
        # load page
        driver.get(self.conf.target_login)
        driver.implicitly_wait(2)

        # login
        userInput = driver.find_elements(By.CSS_SELECTOR,self.conf.userInput)
        if len(userInput) != 0:
            userInput[0].send_keys(self.user)
            driver.find_elements(By.CSS_SELECTOR,self.conf.passInput)[0].send_keys(self.password)
            driver.find_elements(By.CSS_SELECTOR,self.conf.pinInput)[0].send_keys(self.user)
            driver.find_elements(By.CSS_SELECTOR,self.conf.loginBtn)[0].click()
            driver.implicitly_wait(5)
            # save cookies
            self.save_cookies(driver)
        else:
            self.login(driver)
    # endregion Custom Main Scrapping
       
    # region General Main Scrapping
    def web_driver(self):
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)

    def firefox_driver_linux(self,gecko_driver='driver/driver_linux/geckodriver',  load_images= True, gui = False):

        options=Options()
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference("media.volume_scale", "0.0")
        options.set_preference("dom.webnotifications.enabled", False)
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0'

        if user_agent != '':
            options.set_preference("general.useragent.override", user_agent)
        if not load_images:
            options.set_preference('permissions.default.image', 2)
        
        options.headless = gui

        # set webdriver
        #  Driver : 
        driver_path = f'{self.current_path}/{gecko_driver}'
        service = Service(driver_path)

        return webdriver.Firefox(executable_path=driver_path, options=options)

    def firefox_driver_wind(self,gecko_driver='driver/driver_wind/geckodriver',  load_images= True, gui = False):

        options=Options()
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference("media.volume_scale", "0.0")
        options.set_preference("dom.webnotifications.enabled", False)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        if user_agent != '':
            options.set_preference("general.useragent.override", user_agent)
        if not load_images:
            options.set_preference('permissions.default.image', 2)
        
        options.headless = gui

        # set webdriver
        #  Driver : 
        driver_path = f'{self.current_path}/{gecko_driver}'
        service = Service(driver_path)

        return webdriver.Firefox(executable_path=driver_path, options=options)

    def save_cookies(self,driver):
        cookies_list = driver.get_cookies()
        db = Config.objects.get(name='cookies')
        db.content= json.dumps( cookies_list ) 
        db.save()

    def load_cookies(self,driver,url,checkElement):
        driver.get(url)
        db = Config.objects.get(name='cookies')
        cookies = db.content
        if cookies != '':
            cookies = json.loads(cookies)

            if len(cookies) > 0:
                for cookie in cookies:
                    driver.add_cookie(cookie)

            driver.implicitly_wait(3)

            driver.get(url)
            # if cookies cant login
            if len(driver.find_elements(By.CSS_SELECTOR,checkElement)) > 0:
                db.content = ''
                db.save()
                return False
            # if cookies login
            else:
                return True
        return False
    # endregion General Main Scrapping
     
    # region Scanning
    def startApp(self,allArea=False,allBranch=True):
        dateNow = datetime.datetime.now().date()
        self.insertMessage(msg ="بدأ تشغيل السحب",type = 0)
        self.insertMessage(msg =f"بدأ تشغيل السحب بتاريخ {dateNow}",type = 3)
        driver = self.preparePage()

        areas = [i.text for i in driver.find_elements(By.CSS_SELECTOR,self.conf.listOfAreas) ]   # extract text of area
        self.db.setAreas(areas)           # save areas or update to database
        self.insertMessage(msg = f"تم تحديث كل المحافظات عددها الأن: {str(len(areas))}")


        selectedAreas = self.db.getSelectedAreas()   # to get selected areas from database
        index_area = 0
        governments = driver.find_elements(By.CSS_SELECTOR,self.conf.listOfAreas)
        for _ in governments:
            try:
                if index_area != 0:
                    driver.refresh()
                    self.navigateToFlex(driver)

                d = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfAreas)))[index_area]
                index_area += 1
                area = d.text.strip()

                if allArea: condition = allArea
                else: condition = area in selectedAreas
                # ----------------------------------------- #

                if condition:
                    driver.execute_script("arguments[0].click();",d)
                    driver.implicitly_wait(10)
                    self.insertMessage(msg=f"جارى فحص محافظة   {area}",notify=True)
                    self.insertMessage(msg =f"بدأ تشغيل سحب محافظة {area} بتاريخ {dateNow}",type = 3)
                    # -------------------------------------------------------#

                    listA2 = driver.find_elements(By.CSS_SELECTOR,self.conf.listOfAreas)

                    self.insertMessage(msg = "تم سحب قائمة الفروع")
                    self.insertMessage(msg = f"عدد أفرع المنطقة {str(len(listA2))}")
                    # -------------------------------------------------------#
                    branches = [e.text.replace('"','') for e in listA2]  # extract text of branches
                    self.db.setBranches(branches, area)
                    self.insertMessage(msg = f"تم تحديث كل الفروع عددها: {str(len(branches))}")
                    # -------------------------------------------------------#

                    branchesSelected = self.db.getSelectedBranches(area)
                    index = 0
                    for _ in listA2:
                        try:
                            #d = driver.find_elements(By.CSS_SELECTOR,self.conf.listOfBranches)
                            d = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfBranches)))

                            if len(d) >= index+1:
                                d = d[index]
                                index += 1
                            else: break

                            branch = d.text
                            if not allBranch:
                                if len(branchesSelected) == 0: 
                                    self.insertMessage(msg = "تم الإنتهاء من الفحص")


                            if allBranch: condition = allBranch
                            else: condition = branch in branchesSelected
                            
                            if condition:
                                numbers = self.getScrappedNumbers(driver,d,branch)
                                try:
                                    self.numbersLabDatabaseAdapter(numbers,area,branch)
                                except Exception as e: self.insertMessage(msg = f"Number extractions Error: {str(e)}")

                                if not allBranch:branchesSelected.remove(branch)
                                self.goBack(driver) 
                                self.insertMessage(msg = f"تم فحص فرع رقم {str(index)}")


                        except Exception as e: self.insertMessage(msg = f"Branches extractions Error: {str(e)}")

                    self.insertMessage(msg=f"تم فحص محافظة   {area}",notify=True)
                    self.insertMessage(msg =f"تم الإنتهاء من الفحص بمحافظة {area} بتاريخ {dateNow}",type = 3)

                    if not allArea: selectedAreas.remove(area)

            except Exception as e:  self.insertMessage(msg = f"Area Extractions: {str(e)}")
    
    def getScrappedNumbers(self,driver,d,branch):
        # Insert to Branch
        driver.execute_script("arguments[0].click();", d) # d.click()
        driver.implicitly_wait(3)
        self.insertMessage(msg = f"جارى فحص الأرقام الموجوده فى فرع {branch}")
        # -------------------------------------------------------#
        numbers = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.numbers)))
        self.insertMessage(msg = f"عدد الأرقام المتوفرة فى منطقة {branch} \n هى {str(len(numbers))}")
        # -------------------------------------------------------#
        return numbers
    
    def numbersLabDatabaseAdapter(self,numbers,area,branch):
        numbers = [number.text[1:] for number in numbers]
        self.db.insertInDatabaseAdapter(numbers, area,branch)

    def numbersLabLoob(self,numbers,area,branch):
        for m in numbers:
            try:
                number = m.text[1:]
                if branch is None: branch = "غير محدد"
                self.db.insertInDatabase(number, area,branch)

            except Exception as e: self.insertMessage(title = "problem",msg = f"number extractions Error: {str(e)}")
    # endregion Scanning 

        
    def checkNumber(self,phoneNumber,branchSelect,areaSelect):
        try:
            dateNow = datetime.datetime.now().date()
            driver = self.preparePage(id_key = "id_check")
            self.insertMessage(msg =f"بدأ فحص الرقم {phoneNumber} بتاريخ {dateNow}",type = 4)
            self.insertMessage(title= "فحص",msg=f"جارى فحص رقم {phoneNumber} ",notify=True,type=1)

            # Areas
            # driver.find_elements(By.CSS_SELECTOR,self.conf.listOfAreas)
            #governments = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfAreas)))
            areas = { area.text.strip():area for area in WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfAreas))) }
            driver.execute_script("arguments[0].click();",areas[areaSelect])
            driver.implicitly_wait(1)
            self.insertMessage(msg="area has been selected",notify=False)

            # Branches
            # driver.find_elements(By.CSS_SELECTOR,self.conf.listOfBranches)
            branches = { branch.text.strip():branch for branch in WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfBranches))) }
            driver.execute_script("arguments[0].click();", branches[branchSelect])
            driver.implicitly_wait(1)
            self.insertMessage(msg="branch has been selected",notify=False)

            # Branches
            # driver.find_elements(By.CSS_SELECTOR,self.conf.numbers)
            numbers = [ number.text[1:] for number in WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.numbers))) ]
            if phoneNumber in numbers:
                ul = driver.find_elements(By.CSS_SELECTOR,self.conf.selectNumber+f'[value="2{phoneNumber}"]')[0]
                driver.execute_script("arguments[0].click();", ul)
                self.goNext(driver)
                msg = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.alert)))
                if len(msg) !=0:
                    message = msg[0].text.strip()
                    classes = msg[0].get_attribute("class")
                    is_valid = "alert-danger" not in classes
                    self.db.updateCheckDone(phoneNumber)
                    self.db.updateValidation(phoneNumber,is_valid)
                    self.insertMessage(msg=message,notify=True,type=1)
                    self.insertMessage(msg=message,notify=False,type=4)
                else:
                    self.insertMessage(title= "فحص",msg=f"يوجد مشكلة فى إستخراج رساله الحجز لرقم {phoneNumber}",notify=True,type=1)
            else:
                self.db.updateCheckDone(phoneNumber)
                self.db.updateValidation(phoneNumber,False)
                self.insertMessage(title= "فحص",msg=f"هذا الرقم {phoneNumber} لم يعد موجود",notify=False,type=1)
        except Exception as e: self.insertMessage(msg =f"يوجد مشكلة فى حجز الرقم: {str(e)}",notify=False,type=1)


    def checkNumberOld(self,phoneNumber,branchSelect,areaSelect):
        driver = self.preparePage(id_key = "id_check")
        self.insertMessage(title= "فحص",msg=f"جارى فحص رقم {phoneNumber} ",notify=True,type=1)

        #governments = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfAreas)))
        #isEnterArea = False
        for area in driver.find_elements(By.CSS_SELECTOR,self.conf.listOfAreas):
            self.insertMessage(msg="index 1",notify=False)
            try:
                if area.text.strip() == areaSelect:
                    self.insertMessage(msg="index 2",notify=False,type=1)
                    driver.execute_script("arguments[0].click();",area)
                    driver.implicitly_wait(5)
                    #branches = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.listOfBranches)))
                    # -------------------------------------------------------#
                    #isEnterBranch = False
                    for branch in driver.find_elements(By.CSS_SELECTOR,self.conf.listOfBranches):
                        self.insertMessage(msg="index 3",notify=False,type=1)
                        try:
                            if branch.text.strip() == branchSelect:
                                self.insertMessage(msg="index 4",notify=False,type=1)
                                driver.execute_script("arguments[0].click();", branch)
                                driver.implicitly_wait(5)
                                # -------------------------------------------------------#
                                #numbers = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.numbers)))
                                # -------------------------------------------------------#
                                #isEnterNumber = False
                                for number in driver.find_elements(By.CSS_SELECTOR,self.conf.numbers):
                                    self.insertMessage(msg="index 5",notify=False,type=1)
                                    try:
                                        if number.text[1:] == phoneNumber:
                                            self.insertMessage(msg="index 6",notify=False,type=1)
                                            ul = driver.find_elements(By.CSS_SELECTOR,self.conf.selectNumber+f'[value="2{phoneNumber}"]')[0]
                                            driver.execute_script("arguments[0].click();", ul)
                                            self.goNext(driver)
                                            
                                            msg = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,self.conf.alert)))
                                            if len(msg) !=0:
                                                self.insertMessage(msg="index 7",notify=False,type=1)
                                                message = msg[0].text.strip()
                                                self.insertMessage(msg=message,notify=True,type=1)
                                                classes = msg[0].get_attribute("class")
                                                is_valid = "alert-danger" not in classes
                                                self.db.updateCheckDone(phoneNumber)
                                                self.db.updateValidation(phoneNumber,is_valid)
                                                return

                                    except Exception as e: 
                                        self.insertMessage(msg =f"number extractions Error: {str(e)}",notify=False,type=1)
                                
                                self.insertMessage(msg=f"هذا الرقم {phoneNumber} لم يعد موجود",notify=False,type=1)
                                self.db.updateCheckDone(phoneNumber)
                                self.db.updateValidation(phoneNumber,False)
                                self.insertMessage(msg="index 8",notify=False,type=1)
                                return
                        except Exception as e: self.insertMessage(msg =f"Branches extractions Error: {str(e)}",notify=False,type=1)

            except Exception as e: self.insertMessage(msg = f"Area Extractions: {str(e)}",notify=False,type=1)


## driver.execute_script("arguments[0].scrollIntoView()", listA3)
##select = driver.find_elements(By.CSS_SELECTOR,"td.entryID")[0]
##select.find_elements(By.CSS_SELECTOR,"a")[0].click()
##sleep(15)
##ul = select.find_elements(By.CSS_SELECTOR,"div#table-uniprot_annotation")[0]
##ul = WebDriverWait(select, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#table-uniprot_annotation")))
##li = ul.find_elements(By.CSS_SELECTOR,"a")
