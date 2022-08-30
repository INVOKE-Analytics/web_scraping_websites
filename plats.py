from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# activate excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Leads Info'
sheet.append(['Name','Address','Whatsapp Link'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://platselangor.com/senarai-penjaja-listing/?sf-s=&sf-listdom-category=&sf-listdom-label=&sf-listdom-location=&sf-att-168-eq="

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

# load the page 499 times to get data worth of 500 pages
for i in range(499):
    next = driver.find_element(By.CLASS_NAME, "lsd-load-more")
    next.click()
    time.sleep(3)

# extract all data
soup = BeautifulSoup(driver.page_source, 'lxml')

infos = soup.find_all('div', {'class':'lsd-listing-body'})

for info in infos:
    temp_name = info.find('h3', {'class':'lsd-listing-title'})
    if temp_name != None:
        name = temp_name.get_text().strip()
    else:
        name = ''
    temp_address = info.find('div', {'class':'lsd-listing-address'})
    if temp_address != None:
        address = temp_address.get_text().strip()
    else:
        address = ''
    temp_ws = info.find('div', {'class':'lsd-contact-info'})
    if temp_ws != None:
        temp_ws2 = temp_ws.find('a')
        if temp_ws2 != None:
            ws = temp_ws2.get('href')
        else:
            ws = ''
    else:
        ws = ''
        
    sheet.append([name,address,ws])

# save excel file
excel.save('Platform Selangor (meniaga).xlsx')