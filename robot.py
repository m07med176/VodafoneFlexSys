from selenium import webdriver
import os

class Robot:
    def __init__(self):

        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options)

    def test(self):
        self.driver.get("https://www.google.com")
        return self.driver.page_source
        
