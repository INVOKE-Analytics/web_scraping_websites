from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# create a panda dataframe
df = pd.DataFrame(columns=['Name','Address','Telephone Number','Website','Email'])

# create an excel sheet for dataframe object
writer = pd.ExcelWriter('New Pages.xlsx')

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://m.newpages.com.my/en/free-listing/index.html"

# open chromedriver
driver = webdriver.Chrome("insert-path-to-chromedriver")
HTML_text = driver.get(target_link)
driver.maximize_window()

url_link = []
domain = 'https://m.newpages.com.my/'

name_list = []
address_list = []
number_list = []
website_list = []
email_list = []

# extract all data besides email in the first 500 pages    
for k in range(500):
    soup = BeautifulSoup(driver.page_source, 'lxml')

    infos = soup.find('div',{'class':'company_list'}).find_all('li')

    for info in infos:
        temp_name = info.find('div',{'class':'company_list_detail'})
        if temp_name != None:
            temp_name2 = temp_name.get_text()
            if temp_name2 != None:
                name = temp_name2.split('  ')[0].strip()
            else:
                name = ''
        else:
            name = ''

        add_info = info.find_all('p')

        address = add_info[0].get_text().strip()

        if len(add_info) > 2:
            number = add_info[1].get_text().strip()
        else:
            number = ''

        if len(add_info) > 3:
            temp_website = add_info[2].find('a')
            website = temp_website.get('href')
        else:
            website = ''    

        temp_link = info.find('a')
        link = temp_link.get('href')
        url = domain + link
        url_link.append(url)

        name_list.append(name)
        address_list.append(address)
        number_list.append(number)
        website_list.append(website)
        
    next = driver.find_element(By.XPATH,'/html/body/div[1]/div[22]/section/div[3]/a[3]')
    time.sleep(3)
    next.click()
    time.sleep(3)

# extract email data using requests    
for link in url_link:
    r = requests.get(link)
    soup2 = BeautifulSoup(r.text,'lxml')
    temp_email = soup2.find('div',{'class':'company_topdetail_box'})
    if temp_email != None:
        temp_email2 = temp_email.get_text().split('\n')
        email = temp_email2[1].strip()
        email_list.append(email)
    else:
        temp_email2 = soup2.find('div',{'class':'freelisting'}).find_all('p')
        temp_email3 = temp_email2[2].find('a')
        if temp_email3 != None:
            temp_email4 = temp_email3.find('img')
            if temp_email4 != None:
                email = temp_email4.get('src')
                email_list.append(email)
            else:
                email = ''
                email_list.append(email)
        else:
            email = ''
            email_list.append(email)

# push the data into pandas dataframe    
df['Name'] = name_list
df['Address'] = address_list
df['Telephone Number'] = number_list
df['Website'] = website_list
df['Email'] = email_list

# push pandas dataframe into excel
df.to_excel(writer,sheet_name = 'Leads Info',index=False)

# save excel file
writer.save()