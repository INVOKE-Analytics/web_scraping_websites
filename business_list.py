from bs4 import BeautifulSoup
import requests, openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# activate excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Leads Info'
sheet.append(['Name','Address','Phone Number','Website'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://www.businesslist.my/category/general-business"

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

soup = BeautifulSoup(driver.page_source, 'lxml')

shop_link = soup.find('div', {'id':'listings'}).find_all('a')

# extract all links
temp_list = []

for shop in shop_link:
    link = shop.get('href')
    temp_list.append(link)

temp_list2 = list(dict.fromkeys(temp_list))

# extract company links
temp_list3 = []
element = '/company/'

for item in temp_list2:
    if element in item:
        temp_list3.append(item)
    else:
        pass

url_list = []
element2 = 'reviews'

for shop in temp_list3:
    if element2 not in shop:
        url = 'https://www.businesslist.my'
        link = url + shop
        url_list.append(link)
    else:
        pass

# extract data in page 1
for cart in url_list:
    r = requests.get(cart)
    soup2 = BeautifulSoup(r.text, 'lxml')
    info = soup2.find('div',{'class':'cmp_details'})
    name = info.find('b',{'id':'company_name'}).string
    address = info.find('div',{'class':'text location'}).get_text()
    final_address = address.replace('View Map','')
    number = info.find('div',{'class':'text phone'})
    if number != None:
        phone_number = number.get_text()
    else:
        phone_number = ""

    website = info.find('div',{'class':'text weblinks'})
    if website != None:
        temp_wb = website.find('a')
        wb_link = temp_wb.get('href')

    else:
        wb_link = ""

# create page links
page_list = []
element3 = '/category/general-business/'
url = 'https://www.businesslist.my'
number = range(2,3591)

for j in number:
    page_number = str(j)
    page_link = url + element3 + page_number
    page_list.append(page_link)  
    
final_page_list = page_list[:348]

# extract data in page 2 until page 350    
for page in final_page_list:
    r = requests.get(page)
    soup2 = BeautifulSoup(r.text, 'lxml')
    shop_link2 = soup2.find('div', {'id':'listings'}).find_all('a')
    company_list = []

    for shop in shop_link2:
        link = shop.get('href')
        company_list.append(link)

    company_list2 = list(dict.fromkeys(company_list))

    company_list3 = []
    element4 = '/company/'

    for item in company_list2:
        if element4 in item:
            company_list3.append(item)
        else:
            pass

    url_list2 = []
    element5 = 'reviews'

    for shop in company_list3:
        if element5 not in shop:
            url = 'https://www.businesslist.my'
            link = url + shop
            url_list2.append(link)
        else:
            pass
        
    for cart in url_list2:
        r = requests.get(cart)
        soup2 = BeautifulSoup(r.text, 'lxml')
        info = soup2.find('div',{'class':'cmp_details'})
        name = info.find('b',{'id':'company_name'}).string
        address = info.find('div',{'class':'text location'})
        if address != None:
            temp_address = address.get_text()
            final_address = temp_address.replace('View Map','')
        else:
            final_address = ""
        number = info.find('div',{'class':'text phone'})
        if number != None:
            phone_number = number.get_text()
        else:
            phone_number = ""

        website = info.find('div',{'class':'text weblinks'})
        if website != None:
            temp_wb = website.find('a')
            wb_link = temp_wb.get('href')

        else:
            wb_link = ""
        
        sheet.append([name,final_address,phone_number,wb_link])

# save excel file        
excel.save('Business List (adnexio).xlsx')