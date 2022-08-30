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
sheet.append(['Shop Name','Owner Name','Address','State','Telephone Number','Email','Website'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://www.insken.gov.my/direktori-usahawan/"

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'lxml')

# extract data from 106 shops
infos = soup.find_all('div', {'class':'search-filter-result-item'})
final_infos = infos[:106]

for info in final_infos:
    temp_header_info = info.find('h3').get_text().strip() 
    temp_header_info2 = temp_header_info.split('  ')
    
    shop_name = temp_header_info2[0].strip()
    
    if '\n' in temp_header_info2[1]:
        temp_state = temp_header_info2[1].split('\n')
        state = temp_state[1].strip()
    else:
        state = temp_header_info2[1].lstrip()
    
    temp_owner_name = info.find('td').get_text().strip()
    temp_owner_name2 = temp_owner_name.split('Nama')[1]
    owner_name = temp_owner_name2.strip()
    
    url = info.find_all('a')
    temp_email = url[0].get('href')
    email = temp_email.split(':')[1]
    temp_phone = url[1].get('href')
    phone = temp_phone.split(':')[1]
    
    add_info = info.find_all('div', {'class':'search_website'})
    
    address = add_info[0].get_text().strip()
    
    if len(add_info) > 1:
        website = add_info[1].get_text().strip()
    else:
        website = '-'
    
    sheet.append([shop_name,owner_name,address,state,phone,email,website])

# save excel file
excel.save('INSKEN.xlsx')