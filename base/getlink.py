from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class setup():
    def __init__(self):
        self.link = 'https://congbothongtin.ssc.gov.vn/faces/NewsSearch'
        self.reset_driver('C:\webdrive\Driver\chromedriver.exe')
        # self.reset_driver('C:\webdrive\Driver\msedgedriver.exe')
        # self.login()
    def reset_colab(self):
        from selenium import webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    def reset_driver(self, path = 'C:\webdrive\Driver\chromedriver.exe'):
        self.driver = webdriver.Chrome(executable_path=path)
        # self.driver = webdriver.ChromiumEdge(executable_path=path)


class get(setup):
    def login(self, symbol, year, finan):
        self.driver.get(self.link)
        # self.getlink(self.link)
        time.sleep(0.5)
        self.driver.maximize_window()
        check_element = self.sendelenmet(symbol, year, finan)
        if check_element == 'Loi':
            return pd.DataFrame({'Nothing':[]})
        time.sleep(5)
        # self.driver.close()
        data = self.read_table()
        return data

    def getlink(self, link):
        try:
            self.driver.set_page_load_timeout(10)
            self.driver.get(link)
        except:
            print('hi')
            # self.driver.refresh()
            self.getlink(link)

    def sendelenmet(self, symbol, year, finan):
        self.driver.find_element_by_id('pt9:it8112::content').send_keys(symbol)
        time.sleep(0.5)
        self.driver.find_element_by_id('pt9:it8112::content').send_keys(Keys.ENTER)
        self.driver.find_element_by_id('pt9:smc2::content').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="pt9:smc2::pop"]/li[2]/ul/li[11]/label/input').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="pt9:smc2::pop"]/li[2]/ul/li[11]/label/input').send_keys(Keys.ENTER)
        self.driver.find_element_by_id('pt9:b1').click()
        time.sleep(7)
        id = self.ChooseLink_table(year)
        print(id)
        if id == None:
            return 'Loi'
        self.driver.find_element_by_id(id).click()
        time.sleep(1)
        if finan == 'IS':
            self.driver.find_element_by_id('pt2:tab2::disAcr').click()
        
    def Choose_id(self, year):
        driver_page_source = self.driver.page_source
        page = BeautifulSoup(driver_page_source, "html.parser")
        check = page.find('table', {'role':'presentation',"class":"x14q x15f"})
        span_page = check.find_all('a', {'class':'xgl'})
        for i in span_page:
            if 'năm' in i.text and year in i.text and 'Riêng' not in i.text:  
                id = i['id']
                return id
    def ChooseLink_table(self, year):
        id = self.Choose_id(year)
        if id != None:
            return id
        else:
            try:
                self.driver.find_element_by_id('pt9:t1::nb_nx').click()
                time.sleep(2)
                return self.Choose_id(year)
            except: pass
        

    def read_table(self):
        driver_page_source = self.driver.page_source
        page = BeautifulSoup(driver_page_source, "html.parser")
        table = page.find('table', {'role':'presentation',"class":"x14q x15f"})
        data = pd.read_html(str(table))[0]
        return data

