import time
from selenium.webdriver.common.by import By
import pandas as pd


def district_URL_scrapper(Const):
    current_district = 1
    districts_URL = []
    URL_base = Const.URL
    districts = Const.electoral_district_number
    while current_district <= districts:
        URL = URL_base + str(current_district)
        districts_URL.append(URL)
        current_district = current_district + 1
    return districts_URL

def region_URL_scrapper(district_list, driver):
    all_regions_url = []
    current_district_number=1
    for single_district_url in district_list:
        a = 0
        driver.get(single_district_url)
        time.sleep(2)
        ul_elements = driver.find_elements(By.CSS_SELECTOR, "ul.list li ul li")
        for one_region in ul_elements:
            a_one_region = one_region.find_elements(By.TAG_NAME, "a")
            for x in a_one_region:
                href_value = x.get_attribute("href")
                single_region = [one_region.text, href_value]
            if (a != 0):
                all_regions_url.append(single_region)
            a = a + 1
        current_district_number = current_district_number + 1
    region_df = pd.DataFrame(all_regions_url, columns=['Powiat','URL'])
    region_df.to_csv('csv/okregi.csv',index=False)

def district_stat_scrapper(csv_file, driver):
    region_df=pd.read_csv(csv_file)
    final_dataset=[]
    for index, row in region_df.iterrows():
        nazwa_powiatu = row['Powiat']
        link = row['URL']
        print(nazwa_powiatu, link)
        driver.get(link)
        time.sleep(2)
        laczna_ilosc_wszystkich_glosow=driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[4]/td[3]').text
        laczna_ilosc_glosow_niewaznych = driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[5]/td[3]').text
        niewazny_poprzez_wieleX = driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[6]/td[3]').text
        niewazny_poprzez_zadnegoX = driver.find_element(By.XPATH,'/html/body/div[4]/div[16]/div[4]/div[3]/table/tbody/tr[7]/td[3]').text
        nazwa_powiatu = driver.find_element(By.XPATH, '//*[@id="root"]/div[16]/div[1]/div[1]/div/h3').text
        print("Nazwa: ", nazwa_powiatu, "Laczna ilosc glosow waznych: ", laczna_ilosc_wszystkich_glosow," Laczna ilosc glosow niewaznych: ", laczna_ilosc_glosow_niewaznych, " Wiecej niz jeden X: ", niewazny_poprzez_wieleX, " Zadnego X: ", niewazny_poprzez_zadnegoX)

        stat_list=[nazwa_powiatu,laczna_ilosc_wszystkich_glosow,laczna_ilosc_glosow_niewaznych,niewazny_poprzez_zadnegoX,niewazny_poprzez_wieleX]
        final_dataset.append(stat_list)
        time.sleep(5)


    time.sleep(5)

    final_dataset_df=pd.DataFrame(final_dataset, columns=['Powiat','Laczna ilosc glosow','Laczna ilosc glosow niewaznych','Poprzez brak głosu','Poprzez zbyt wiele głosów'])
    columns_to_clean = ['Laczna ilosc glosow', 'Laczna ilosc glosow niewaznych', 'Poprzez brak głosu',
                        'Poprzez zbyt wiele głosów']
    for column in columns_to_clean:
        final_dataset_df[column] = final_dataset_df[column].str.replace(' ', '')
    final_dataset_df.to_csv('csv/final_dataset.csv')


    driver.close()