from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# activate excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Leads Info'
sheet.append(['Name','Business Type','Address','Telephone Number','Fax Number'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://pekema.org.my/senarai-ahli-pekema/"

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

# extract all data in the page
soup = BeautifulSoup(driver.page_source, 'lxml')

infos = soup.find('tbody').find_all('tr', {'role':'row'})

for info in infos:
    name = info.find('td', {'class':'column-namasyarikat sorting_1'}).get_text().strip()
    business_type = info.find('td', {'class':'column-jenisperniagaan'}).get_text().strip()
    address = info.find('td', {'class':'column-alamat'}).get_text().strip()
    phone_number = info.find('td', {'class':'column-notelefon'}).get_text().strip()
    fax_number = info.find('td', {'class':'column-nofaks'}).get_text().strip()
    
    sheet.append([name,business_type,address,phone_number,fax_number])

# save excel file
excel.save('PEKEMA.xlsx')