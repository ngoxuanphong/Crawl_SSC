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
    def login(self, symbol, year, type_time):
        self.driver.get(self.link)
        # self.getlink(self.link)
        time.sleep(0.5)
        try:
            self.driver.maximize_window()
        except: return self.login(symbol, year, type_time)
        check_element = self.sendelenmet(symbol, year, type_time)
        if check_element == 'Loi':
            return pd.DataFrame({'Nothing':[]})
        time.sleep(2)
        data = self.read_table()
        if type(data) == str: 
            return pd.DataFrame({'Nothing':[]})
        for type_finan in range(2, 5):
            try:
                self.driver.find_element_by_id(f'pt2:tab{type_finan}::disAcr').click()
                time.sleep(2)
                data_new = self.read_table()
                time.sleep(1)
                data = pd.concat([data, data_new])
            except: return self.login(symbol, year, type_time)
        return data


    def sendelenmet(self, symbol, year, type_time):
        self.driver.find_element_by_id('pt9:it8112::content').send_keys(symbol)
        time.sleep(0.5)
        self.driver.find_element_by_id('pt9:it8112::content').send_keys(Keys.ENTER)
        self.driver.find_element_by_id('pt9:smc2::content').click()
        time.sleep(0.5)
        if type_time == 'NAM':
            xpath_bctc = '//*[@id="pt9:smc2::pop"]/li[2]/ul/li[11]/label/input'
        else: 
            xpath_bctc = '//*[@id="pt9:smc2::pop"]/li[2]/ul/li[12]/label'
        self.driver.find_element_by_xpath(xpath_bctc).click()
        time.sleep(0.5) 
        self.driver.find_element_by_xpath(xpath_bctc).send_keys(Keys.ENTER)
        self.driver.find_element_by_id('pt9:b1').click()
        time.sleep(7)
        id = self.ChooseLink_table(year, type_time)
        # print(id)
        if id == None:
            return 'Loi'
        self.driver.find_element_by_id(id).click()
        time.sleep(3)
        action = webdriver.ActionChains(self.driver)
        element = self.driver.find_element_by_id('pt2:tab1::disAcr') # or your another selector here
        action.move_to_element(element)
        action.perform()
        try:
            self.driver.find_element_by_id('pt2:tab1::disAcr').click()
        except:
            print('Dont click')
        time.sleep(6)
        
    def Choose_id(self, year, type_time):
        driver_page_source = self.driver.page_source
        page = BeautifulSoup(driver_page_source, "html.parser")
        check = page.find('table', {'role':'presentation',"class":"x14q x15f"})
        # span_page = check.find_all('a', {'class':'xgl'})
        for tr in check.find_all('tr'):
            list_td = tr.find_all('td')
            # print(list_td[1]['id'], list_td[3].text)
            text_tin = str([list_td[3].text.upper(),list_td[1].text.upper()])
            if type_time == 'NAM':
                    if 'KIỂM TOÁN' in text_tin and year in text_tin:
                        if  'RIÊNG' not in text_tin and 'MẸ' not in text_tin:
                            if '6 THÁNG ĐẦU NĂM' not in text_tin and 'BÁN NIÊN' not in text_tin:
                                id = list_td[1]['id']
                                return id
            else:
                quy = year[:5]
                nam = year[-4:]
                if 'RIÊNG' not in text_tin and 'MẸ' not in text_tin:
                        # print(nam, quy)
                        if nam in text_tin or nam in text_tin:
                            if '1' in quy:
                                if quy in text_tin or quy.replace('1', 'I') in text_tin:
                                    if 'II'not in text_tin and 'III' not in text_tin and 'IV' not in text_tin:
                                        return list_td[1]['id']
                            if '2' in quy:
                                if quy in text_tin or quy.replace('2', 'II') in text_tin:
                                    if 'III'not in text_tin:
                                        return list_td[1]['id']
                            if '3' in quy:
                                if quy in text_tin or quy.replace('3', 'III') in text_tin:
                                    return list_td[1]['id']
                            if '4' in quy:
                                if quy in text_tin or quy.replace('4', 'IV') in text_tin:
                                    return list_td[1]['id']
                        

    def ChooseLink_table(self, year, type_time):
        for i in range(6):
            time.sleep(2)
            id = self.Choose_id(year, type_time)
            if id != None:
                return id
            try:
                self.driver.find_element_by_id('pt9:t1::nb_nx').click()
                time.sleep(2)
            except: break
        

    def read_table(self):
        try:
            driver_page_source = self.driver.page_source
        except: 
            print('Loi roi ngu ngu')
            return 'Loi'
        if 'java.lang.NullPointerException' in driver_page_source:
            return 'Loi'
        page = BeautifulSoup(driver_page_source, "html.parser")
        table = page.find('table', {'role':'presentation',"class":"x14q x15f"})
        data = pd.read_html(str(table))[0]
        return data
