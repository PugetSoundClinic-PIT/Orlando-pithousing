import csv
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
from bs4 import BeautifulSoup

def scrape_detail_page(driver):
    # Modify later
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".propertyFeaturesForm .p-2")))    
    detail_html = driver.page_source
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    # Extract
    property_features = detail_soup.find("div", {"id": "property-features"}).text if detail_soup.find("div", {"id": "property-features"}) else "Not Found"
    # Extract other tabs
    
    return {
        "property_features": property_features,
        # Other details here
    }

def navigate_back_to_results(driver):
    # Click on the "Results" tab to return to the table
    results_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "ngb-nav-2"))
    )
    results_tab.click()

def extract_table_data(driver, writer):
    # Wait for the table body to be present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody"))
    )
    # Get the HTML source of the current page
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    tbody = soup.select_one("table.table-bordered tbody")
    
    # Get the total number of rows in the table for iteration
    total_rows = len(tbody.find_all('tr')) - 1 
    
    for index in range(1, total_rows + 1):
        # Find the row by index and click on it to view details
        row_to_click = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"table.table-bordered tbody tr:nth-of-type({index})"))
        )
        row_to_click.click()
        
        # Scrape details from the detail page
        details = scrape_detail_page(driver)
        
        # Test: Write some details to CSV (expand as needed)
        writer.writerow([details["property_features"]])  # Adjust later
        
        # Navigate back to the results table
        navigate_back_to_results(driver)

def main():
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
        EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Vacant Residential Land')]"))
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

    # 100 results per page
    results_per_page = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "pageSize"))
    )
    select = Select(results_per_page)
    select.select_by_visible_text("100")

    csv_file_path = '/Users/minhanhtruong/Desktop/Orlando-pithousing/test.csv'
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
    
        writer.writerow(['Property Features'])  #Header?
        
        extract_table_data(driver, writer)

    # driver.quit()

if __name__ == "__main__":
    main()
