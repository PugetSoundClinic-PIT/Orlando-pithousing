from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


import pandas as pd

options = Options()

chrome_driver_path = '/Users/minhanhtruong/desktop/pit_housing/chromedriver-mac-x64/chromedriver'

service = Service(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://ocpaweb.ocpafl.org/parcelsearch')

# Write instruction for Selenium to navigate to result page
# Click on TPP/advanced search
tpp_advanced_searches_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "ngb-nav-1"))
)
tpp_advanced_searches_button.click()

# In "Search by", select "Residential Sales Search"
dropdown = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "searchType"))
)
select = Select(dropdown)
select.select_by_visible_text("Residential Sales Search")
# In "Category", select "Single-Family Residential"
dropdown2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "saleCategory"))
)
dropdown2.click()
option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Single-Family Residential')]"))
)
option.click()
# In "Property Type", select "Select All"
dropdown3 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".multiselect-dropdown .dropdown-btn"))
)
dropdown3.click()
select_all_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//li[input[@aria-label='multiselect-select-all']]"))
)
select_all_option.click()
# Then click on "Search Sales"
search_sales_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search Sales')]"))
)
search_sales_button.click()

""" # 100 results per page
results_per_page = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "pageSize"))
)

select_100 = Select(results_per_page)
select_100.select_by_visible_text("100")
 """
table = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-bordered'))
)[0]

""" # Extract data from each row
table_rows = table.find_elements(By.TAG_NAME, 'tr')
for row in table_rows[1:]:  # Skip the header row
    cells = row.find_elements(By.TAG_NAME, 'td')
    address = cells[0].text.strip()
    date_sold = cells[1].text.strip()
    sale_amount = cells[2].text.strip()
    beds = cells[3].text.strip()
    bath = cells[4].text.strip()
    sqft = cells[5].text.strip()
    year = cells[6].text.strip()
    sellers = cells[7].text.strip()
    buyers = cells[8].text.strip()
    parcel_id = cells[9].text.strip()
    
    # print
    print("Address:", address)
    print("Date Sold:", date_sold)
    print("Sale Amount:", sale_amount)
    print("Beds:", beds)
    print("Bath:", bath)
    print("SqFt:", sqft)
    print("Year:", year)
    print("Seller(s):", sellers)
    print("Buyer(s):", buyers)
    print("Parcel ID:", parcel_id)
    print()
 """
# Function to extract data from the current page's table
def extract_table_data(driver):
    table_rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in table_rows[1:]:  # Skip the header row
        cells = row.find_elements(By.TAG_NAME, 'td')
        address = cells[0].text.strip()
        date_sold = cells[1].text.strip()
        sale_amount = cells[2].text.strip()
        beds = cells[3].text.strip()
        bath = cells[4].text.strip()
        sqft = cells[5].text.strip()
        year = cells[6].text.strip()
        sellers = cells[7].text.strip()
        buyers = cells[8].text.strip()
        parcel_id = cells[9].text.strip()
        
        # print
        print("Address:", address)
        print("Date Sold:", date_sold)
        print("Sale Amount:", sale_amount)
        print("Beds:", beds)
        print("Bath:", bath)
        print("SqFt:", sqft)
        print("Year:", year)
        print("Seller(s):", sellers)
        print("Buyer(s):", buyers)
        print("Parcel ID:", parcel_id)
        print()
page_count = 0        
while True:
    extract_table_data(driver)
    # Locate the Next button by its aria-label
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loader"))
    )
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']"))
    )
    # Check if the Next button is disabled (indicating the last page)
    if "disabled" in next_button.get_attribute("class"):
        print("Reached the last page.")
        break
    
    # If not disabled, click the Next button
    next_button.click()
    
    # Wait for the next page to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'table-bordered'))
    )
