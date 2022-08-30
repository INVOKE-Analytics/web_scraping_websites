from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# activate excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'Leads Info'
sheet.append(['Name','Address','Telephone Number','Mobile Number','Email','Website'])

# header for requests library argument
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
target_link = "https://iks.my/sme-directory/?category=0&zoom=13&is_mile=0&directory_radius=50&view=list&hide_searchbox=0&hide_nav=0&hide_nav_views=1&hide_pager=0&featured_only=0&feature=1&perpage=15"

# open chromedriver
driver = webdriver.Chrome('insert-path-to-chromedriver')
HTML_text = driver.get(target_link)
driver.maximize_window()

# extract data in the first 80 pages    
for k in range(80):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    infos = soup.find('div',{'class':'sabai-directory-listings sabai-directory-listings-list sabai-col-md-12'}).find_all('div', {'class':'sabai-row'})
    
    for info in infos:
        temp_name = info.find('div', {'class':'sabai-directory-title'})
        if temp_name != None:
            name = temp_name.get_text().strip()
        else:
            name = ''

        temp_address = info.find('span', {'class':'sabai-googlemaps-address sabai-googlemaps-address-0'})
        if temp_address != None:
            address = temp_address.get_text().strip()
        else:
            address = ''

        add_info = info.find('div', {'class':'sabai-directory-contact'})

        temp_number = add_info.find('div',{'class':'sabai-directory-contact-tel'})
        if temp_number != None:
            temp_number2 = temp_number.find('span',{'class':'sabai-hidden-xs'})
            if temp_number2 != None:
                number = temp_number2.get_text().strip()
            else:
                number = ''
        else:
            number = ''

        temp_mobile = add_info.find('div',{'class':'sabai-directory-contact-mobile'})
        if temp_mobile != None:
            temp_mobile2 = temp_mobile.find('span',{'class':'sabai-hidden-xs'})
            if temp_mobile2 != None:
                mobile = temp_mobile2.get_text().strip()
            else:
                mobile = ''
        else:
            mobile = ''

        temp_email = add_info.find('div',{'class':'sabai-directory-contact-email'})
        if temp_email != None:
            temp_email2 = temp_email.find('a')
            if temp_email2 != None:
                email = temp_email2.get('href').split(':')[1]
            else:
                email =''
        else:
            email = ''
            
        temp_website = add_info.find('div',{'class':'sabai-directory-contact-website'})
        if temp_website != None:
            temp_website2 = temp_website.find('a')
            if temp_website2 != None:
                website = temp_website2.get('href')
            else:
                website = ''
        else:
            website = ''

        sheet.append([name,address,number,mobile,email,website])
    
    # click next page
    try:
        next = driver.find_element(By.LINK_TEXT, '»')
        time.sleep(3)
        next.click()
        time.sleep(3)
    
    except:
        driver.quit()

# save excel file    
excel.save('IKS_MY.xlsx')