from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd

options = Options()

chrome_driver_path = '/Users/minhanhtruong/desktop/pit_housing/chromedriver-mac-x64/chromedriver'

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://ocpaweb.ocpafl.org/parcelsearch')

# Write instruction for Selenium to navigate to result page
tpp_advanced_searches_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "ngb-nav-1"))
)
tpp_advanced_searches_button.click()

# <td _ngcontent-wsa-c91="" style="white-space: pre-wrap;" data-title="Address" class="ng-star-inserted"><!----><!----> 6306  PLYMOUTH SORRENTO RD  <!----><!----></td>
results_table = driver.find_elements(By.XPATH, '//td[@data-title="Address" and @class="ng-star-inserted"]')
results_list = []
for i in range(len(results_table)):
    results_list.append(results_table[i].text)

print(results_list) # its giving me empty list 

