import time
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from classes import Const
from functions import district_URL_scrapper
from selenium import webdriver

district_list=district_URL_scrapper(Const)
#print(district_list)

driver = webdriver.Chrome()
#single_url=district_list[0]
#driver.get(single_url)
#print(single_url)
#time.sleep(3)
i=1
numer_okregu=1
cala_lista_okregow=[]
for single_district_url in district_list:
    a=0
    okrag=[]
    driver.get(single_district_url)
    time.sleep(2)
    ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul.list li ul li")
    for one_region in ul_elements:
        a_one_region = one_region.find_elements(By.TAG_NAME, "a")
        for x in a_one_region:
            href_value = x.get_attribute("href")
            powiat = [one_region.text, href_value]

        if(a!=0):
            okrag.append(powiat)
        #print(okrag)
        a=a+1
    print("Numer okregu: ",numer_okregu, " liczba powiatów: ",len(okrag))
    i=i+1
    numer_okregu=numer_okregu+1
    cala_lista_okregow.append(okrag)

import csv

print(cala_lista_okregow)

okregi_dataframe=pd.DataFrame(cala_lista_okregow)
okregi_dataframe.to_csv('okregi.csv')

time.sleep(1000)



jeden_powiat=driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[1]/div[1]/div/ul/li/ul/li/ul/li[5]/a')
driver.execute_script("arguments[0].click();", jeden_powiat)
time.sleep(1)
laczna_ilosc_glosow_niewaznych=driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[5]/td[3]').text
niewazny_poprzez_wieleX=driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[6]/td[3]').text
niewazny_poprzez_zadnegoX=driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[7]/td[3]').text
nazwa_powiatu=driver.find_element(By.XPATH,'//*[@id="root"]/div[16]/div[1]/div[1]/div/h3').text
print("Nazwa: ",nazwa_powiatu)
print("Laczna ilosc glosow niewaznych: ", laczna_ilosc_glosow_niewaznych)
print("Wiecej niz jeden X: ",niewazny_poprzez_wieleX)
print("Zadnego X: ",niewazny_poprzez_zadnegoX)
time.sleep(5)
driver.close()


