from bs4 import BeautifulSoup
import requests, openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests

# activate excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Leads Info'
sheet.append(['Shop Name','Job Opening','Address','Phone Number'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://www.imfan.com.my/index.php?route=product/seller"

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

# function for decoding email data
def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)

    for i in range(2, len(e)-1, 2):
        de += chr(int(e[i:i+2], 16)^k)

    return de

soup = BeautifulSoup(driver.page_source, 'lxml')

# extract all shop links
shop_link = soup.find('div', {'class':'main-products product-grid'}).find_all('a')

# extract data from shop links
for shop in shop_link:
    link = shop.get('href')
    if link == None:
        pass
    else:
        r = requests.get(link)
        soup2 = BeautifulSoup(r.text, 'lxml')
        info = soup2.find('div',{'class':'col-xs-7 col-sm-7 col-md-7 col-lg-7'})
        name = info.find('div', {'class':'upper-detail'}).string
        mobile = info.find('div',{'class':'seller-mobile'}).get_text()
        mobile_no = mobile.replace('&nbsp&nbsp&nbsp','')
        email_text = info.find('a',{'class':'__cf_email__'})
        encoded_email = email_text.get('data-cfemail')
        email = decodeEmail(encoded_email)
        
        sheet.append([name,mobile_no,email])

# save excel file        
excel.save('Meniaga Leads (IMFAN).xlsx')