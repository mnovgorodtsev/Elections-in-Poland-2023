import pandas as pd
pd.set_option('display.max_rows', 100)

from scripts.classes import Const
from scripts.functions import district_URL_scrapper, district_stat_scrapper, region_URL_scrapper
from selenium import webdriver
from map import create_map

driver = webdriver.Chrome()

district_list=district_URL_scrapper(Const)
region_URL_scrapper(district_list,driver)
district_stat_scrapper("csv/okregi.csv", driver)

create_map('csv/final_dataset')







