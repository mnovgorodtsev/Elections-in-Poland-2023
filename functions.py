import time
from selenium.webdriver.common.by import By
import pandas as pd
pd.set_option('display.max_columns', 100)
import requests
from classes import Const
from selenium import webdriver
def district_URL_scrapper(Const):
    i = 1
    districts_URL = []
    URL_base = Const.URL
    districts = Const.electoral_district_number
    while i < districts:
        URL = URL_base + str(i)
        districts_URL.append(URL)
        i = i + 1
    return districts_URL

def region_URL_scrapper(district_list, driver):
    cala_lista_okregow = []
    i=1
    numer_okregu=1
    for single_district_url in district_list:
        a = 0
        okrag = []
        driver.get(single_district_url)
        time.sleep(2)
        ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul.list li ul li")
        for one_region in ul_elements:
            a_one_region = one_region.find_elements(By.TAG_NAME, "a")
            for x in a_one_region:
                href_value = x.get_attribute("href")
                powiat = [one_region.text, href_value]

            if (a != 0):
                okrag.append(powiat)
            # print(okrag)
            a = a + 1
        i = i + 1
        numer_okregu = numer_okregu + 1
        cala_lista_okregow.append(okrag)

    import csv

    print(cala_lista_okregow)
    okregi_dataframe = pd.DataFrame(cala_lista_okregow)
    okregi_dataframe.to_csv('okregi.csv')

    #okregi_dataframe = pd.DataFrame(okrag)
    #okregi_dataframe.to_csv('okregi.csv')


def district_stat_scrapper(csv_file, driver):
    region_df=pd.read_csv(csv_file)
    region_df = region_df.iloc[:, 1:]
    for row_index, row in region_df.iterrows():
        for col_index, value in row.items():
            if str(value).lower() != "nan":
                print(value)
            else:
                break
    time.sleep(1000)


    jeden_powiat = driver.find_element(By.XPATH, '/html/body/div[4]/div[16]/div[1]/div[1]/div/ul/li/ul/li/ul/li[5]/a')
    driver.execute_script("arguments[0].click();", jeden_powiat)
    time.sleep(1)
    laczna_ilosc_glosow_niewaznych = driver.find_element(By.XPATH,
                                                         '/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[5]/td[3]').text
    niewazny_poprzez_wieleX = driver.find_element(By.XPATH,
                                                  '/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[6]/td[3]').text
    niewazny_poprzez_zadnegoX = driver.find_element(By.XPATH,
                                                    '/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[7]/td[3]').text
    nazwa_powiatu = driver.find_element(By.XPATH, '//*[@id="root"]/div[16]/div[1]/div[1]/div/h3').text
    print("Nazwa: ", nazwa_powiatu)
    print("Laczna ilosc glosow niewaznych: ", laczna_ilosc_glosow_niewaznych)
    print("Wiecej niz jeden X: ", niewazny_poprzez_wieleX)
    print("Zadnego X: ", niewazny_poprzez_zadnegoX)
    time.sleep(5)
    driver.close()