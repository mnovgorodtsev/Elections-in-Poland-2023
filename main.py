import time
from selenium.webdriver.common.by import By
import pandas as pd
pd.set_option('display.max_rows', 100)

from classes import Const
from functions import district_URL_scrapper, district_stat_scrapper, region_URL_scrapper
from selenium import webdriver
from map import create_map

driver = webdriver.Chrome()

district_list=district_URL_scrapper(Const)
region_URL_scrapper(district_list,driver)
district_stat_scrapper("okregi.csv", driver)

create_map('final_dataset')







