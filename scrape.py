import mysql.connector

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import os
from time import sleep
from datetime import datetime

try:
    mydb = mysql.connector.connect(
        host="45.33.77.249",
        port = 3306,
        user="alluser",
        password="QWERqwer!@#$4321"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS alljobs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    mydb = mysql.connector.connect(
        host="45.33.77.249",
        port = 3306,
        user="alluser",
        password="QWERqwer!@#$4321",
        database="alljobs"
    )
    mycursor = mydb.cursor()
    table1_create = """CREATE TABLE IF NOT EXISTS ads (
            id int(11) NOT NULL AUTO_INCREMENT,
            category varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            source varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            date varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            parentPosition varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            parentCategoryName varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            categoryName varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            position varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            job_id varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            job_url varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            job_title varchar(500) COLLATE utf8_unicode_ci NOT NULL,
            client varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            client_url varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            client_image varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            location varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            type varchar(255) COLLATE utf8_unicode_ci NOT NULL,
            description varchar(5000) COLLATE utf8_unicode_ci NOT NULL,
            requirement varchar(3000) COLLATE utf8_unicode_ci NOT NULL,
            run_number int(11) NOT NULL,
            created_on datetime NOT NULL,
            PRIMARY KEY (id),
            KEY all_jobs_run_number (run_number)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
    mycursor.execute(table1_create)
except mysql.connector.Error as err:
    print("Mysql Database connect error")
    exit()
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_BIN)
driver.get('https://www.alljobs.co.il/')
sleep(5)
# driver.implicitly_wait(20)
# iframes = driver.find_elements_by_tag_name('iframe')
# wait = WebDriverWait(driver,300)
# wait.until(EC.frame_to_be_available_and_switch_to_it(iframes[0]))
page_num = 0
change_flag=0
while True:
    page_num += 1
    loop_flag1 = 0
    loop_flag2 = 0
    _str1 = 'https://www.alljobs.co.il/SearchResultsGuest.aspx?page='
    _str2 = '&position=&type=&freetxt=&city=&region='
    _url = str("%s%d%s" %(_str1, page_num, _str2))    
    driver.get(_url) 
    try:
        element=driver.find_element_by_xpath("//*[@id='divOpenBoardContainer']")
        job_num = 0
        loop_in_page_flag = True
        while True:
            job_num += 1
            category = "none"
            source = "none"
            date = "none"
            parentPosition = "none"
            parentCategoryName = "none"
            categoryName = "none"
            position = "none"
            job_id = "none"
            job_url = "none"
            job_title = "none"
            client = "none"
            client_url = "none"
            client_image = "none"
            location = "none"
            _type = "none"
            description = "none"
            requirement = "none"
            run_number = 0
            created_on = datetime.now()
            try:
                _str_element = str("//*[@id='divOpenBoardContainer']/div[1]/div[2]/div[%s]" %(job_num))
                _div_id = driver.find_element_by_xpath(_str_element).get_attribute('id')
            except NoSuchElementException:
                loop_in_page_flag = False                
                pass
            if loop_in_page_flag == False:
                break
            _str_element = str("//*[@id='divOpenBoardContainer']/div[1]/div[2]/div[%s]" %(job_num))
            _div_id = driver.find_element_by_xpath(_str_element).get_attribute('id')
            if "job-box-container" in _div_id:
                job_id = int(_div_id[17:30])
                job_url = str("https://www.alljobs.co.il/Search/UploadSingle.aspx?JobID=%d" %(job_id))
                element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[2]/div[2]")
                date=element.text
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]")
                    source=element.text
                except NoSuchElementException:
                    pass
                element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[4]/div[1]")
                job_title=element.text
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[4]/div[2]")
                    client=element.text                      
                except NoSuchElementException:
                    pass
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a")
                    client_url = element.get_attribute('href')                        
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a/img")
                    client_image = element.get_attribute('src')
                except NoSuchElementException:
                    try:
                        element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a/img")
                        client_image = element.get_attribute('src')
                    except NoSuchElementException:
                        pass
                    pass
                div1_num = 5
                while div1_num<7:
                    div1_num +=1
                    div1_str = _str_element + "/div[1]/div[1]/div[5]/div[" + str(div1_num) +"]"
                    if "job-body-content" in driver.find_element_by_xpath(div1_str).get_attribute('id') :
                        element=driver.find_element_by_xpath(div1_str+"/div[2]")
                        location=element.text
                        element=driver.find_element_by_xpath(div1_str+"/div[3]")
                        _type=element.text
                        description_num = 3
                        while description_num< 7 :
                            description_num += 1
                            description_str = div1_str + "/div[" +str(description_num) +"]"
                            if "job-content-top-acord" in driver.find_element_by_xpath(description_str).get_attribute('id') :
                                element=driver.find_element_by_xpath(description_str+"/div[1]/div[1]/div[1]")
                                description=element.text
                                element=driver.find_element_by_xpath(description_str+"/div[1]/div[1]/div[1]/div[1]")
                                requirement=element.text
                                description = description[0:len(description)-len(requirement)]
                                break
                        break
                _sql = "INSERT INTO `alljobs`.`ads` (`category`, `source`, `date`, `parentPosition`, `parentCategoryName`, `categoryName`, `position`, `job_id`, `job_url`, `job_title`, `client`, `client_url`, `client_image`, `location`, `type`, `description`, `requirement`, `run_number`, `created_on`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                _val = (category, source, date, parentPosition, parentCategoryName, categoryName, position, str(job_id), job_url, job_title, client, client_url, client_image, location, _type, description, requirement, run_number, created_on.strftime("%Y-%m-%d %H:%M:%S"))
                try:
                    mycursor.execute(_sql,_val)
                    mydb.commit()
                except mysql.connector.Error as err:
                    print("mysql_insert_error_Ad is page_num %d, AD_num %d"%(page_num,job_num))
                    print(err)
                    pass  
        
        print(job_num,",",page_num,",1-",change_flag)          
        if job_num<14:
            loop_flag1=1
    except NoSuchElementException:        
        loop_flag1=1
        change_flag+=1
        pass    
    try:
        element=driver.find_element_by_xpath("//*[@id='divOrganicContainer']")
        job_num = 0
        loop_in_page_flag = True
        while True:            
            job_num += 1
            category = "none"
            source = "none"
            date = "none"
            parentPosition = "none"
            parentCategoryName = "none"
            categoryName = "none"
            position = "none"
            job_id = "none"
            job_url = "none"
            job_title = "none"
            client = "none"
            client_url = "none"
            client_image = "none"
            location = "none"
            _type = "none"
            description = "none"
            requirement = "none"
            run_number = 0
            created_on = datetime.now()
            _str_=""
            if loop_flag1==1 and change_flag>0:
                _str_="//*[@id='divOrganicContainer']/div[2]/div[2]/div["
            else:
                _str_="//*[@id='divOrganicContainer']/div[1]/div[2]/div["
            try:
                _str_element = _str_ + str(job_num) + ']'                
                _div_id = driver.find_element_by_xpath(_str_element).get_attribute('id')
            except NoSuchElementException:
                loop_in_page_flag = False                
                pass
            if loop_in_page_flag == False:
                break
            _str_element = _str_ + str(job_num) + ']'
            _div_id = driver.find_element_by_xpath(_str_element).get_attribute('id')
            if "job-box-container" in _div_id:
                job_id = int(_div_id[17:30])
                job_url = str("https://www.alljobs.co.il/Search/UploadSingle.aspx?JobID=%d" %(job_id))
                element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[2]/div[2]")
                date=element.text
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[2]/div[1]/div[1]")
                    source=element.text
                except NoSuchElementException:
                    pass
                element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[4]/div[1]")
                job_title=element.text
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[4]/div[2]")
                    client=element.text                      
                except NoSuchElementException:
                    pass
                try:
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a")
                    client_url = element.get_attribute('href')                        
                    element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a/img")
                    client_image = element.get_attribute('src')
                except NoSuchElementException:
                    try:
                        element = driver.find_element_by_xpath(_str_element+"/div[1]/div[1]/div[5]/div[5]/a/img")
                        client_image = element.get_attribute('src')
                    except NoSuchElementException:
                        pass
                    pass
                div1_num = 5
                while div1_num<7:
                    div1_num +=1
                    div1_str = _str_element + "/div[1]/div[1]/div[5]/div[" + str(div1_num) +"]"
                    if "job-body-content" in driver.find_element_by_xpath(div1_str).get_attribute('id') :
                        element=driver.find_element_by_xpath(div1_str+"/div[2]")
                        location=element.text
                        element=driver.find_element_by_xpath(div1_str+"/div[3]")
                        _type=element.text
                        description_num = 3
                        while description_num< 7 :
                            description_num += 1
                            description_str = div1_str + "/div[" +str(description_num) +"]"
                            if "job-content-top-acord" in driver.find_element_by_xpath(description_str).get_attribute('id') :
                                element=driver.find_element_by_xpath(description_str+"/div[1]/div[1]/div[1]")
                                description=element.text
                                try:
                                    element=driver.find_element_by_xpath(description_str+"/div[1]/div[1]/div[1]/div[1]")
                                    requirement=element.text
                                    description = description[0:len(description)-len(requirement)]
                                except NoSuchElementException:
                                    pass
                                break
                        break
                _sql = "INSERT INTO `alljobs`.`ads` (`category`, `source`, `date`, `parentPosition`, `parentCategoryName`, `categoryName`, `position`, `job_id`, `job_url`, `job_title`, `client`, `client_url`, `client_image`, `location`, `type`, `description`, `requirement`, `run_number`, `created_on`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                _val = (category, source, date, parentPosition, parentCategoryName, categoryName, position, str(job_id), job_url, job_title, client, client_url, client_image, location, _type, description, requirement, run_number, created_on.strftime("%Y-%m-%d %H:%M:%S"))
                try:
                    mycursor.execute(_sql,_val)
                    mydb.commit()
                except mysql.connector.Error as err:
                    print("mysql_insert_error_Ad is page_num %d, AD_num %d"%(page_num,job_num))
                    print(err)
                    pass            
        print(job_num,",",page_num,",2-",change_flag)
        if job_num<14:
            loop_flag2=1
            
    except NoSuchElementException:
        loop_flag2=1
        pass
    
    print(page_num,",",loop_flag1,",",loop_flag2,",",change_flag)
    if (loop_flag1==1) and (loop_flag2==1) and change_flag>0:
        break

driver.close()
mycursor.close()
mydb.close()