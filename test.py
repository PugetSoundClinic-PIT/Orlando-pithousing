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

# Create session 
def setup_driver():
    options = Options()
    chrome_driver_path = '/Users/minhanhtruong/desktop/pit_housing/chromedriver-mac-x64/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_property_features(driver):
    # Click on the "Property Features" tab
    property_features_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'nav-link') and contains(., 'Property Features')]"))
    )
    property_features_tab.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.propertyFeaturesForm"))
    )    
    detail_html = driver.page_source
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    
    # Extract Property Description
    property_description = detail_soup.find("span", text=lambda x: x and "Property Description" in x).find_next_sibling("span").text.strip() if detail_soup.find("span", text=lambda x: x and "Property Description" in x) else "Not Found"
    
    # Extract Total Land Area
    total_land_area = detail_soup.find("h2", text="Total Land Area").find_next("span").text.strip() if detail_soup.find("h2", text="Total Land Area") else "Not Found"
    
    # For simplicity, let's assume we're only interested in the first row of the land data table
    land_data = detail_soup.find("table", {"aria-label": "Land data"})
    if land_data:
        land_use_code = land_data.find("td", {"data-title": "Land Use Code"}).text.strip()
        zoning = land_data.find("td", {"data-title": "Zoning"}).text.strip()
        land_units = land_data.find("td", {"data-title": "Land Units"}).text.strip()
        unit_price = land_data.find("td", {"data-title": "Unit Price"}).text.strip()
        land_value = land_data.find("td", {"data-title": "Land Value"}).text.strip()
        class_unit_price = land_data.find("td", {"data-title": "Class Unit Price"}).text.strip()
        class_value = land_data.find("td", {"data-title": "Class Value"}).text.strip()
    else:
        land_use_code = zoning = land_units = unit_price = land_value = class_unit_price = class_value = "Not Found"

    # Extract first item in Extra Features data for demonstration
    extra_features_data = detail_soup.find("table", {"aria-label": "Extra Features data"})
    if extra_features_data:
        description = extra_features_data.find("td", {"data-title": "Description"}).text.strip()
        date_built = extra_features_data.find("td", {"data-title": "Date Built"}).text.strip()
        units = extra_features_data.find("td", {"data-title": "Units"}).text.strip()
        xfob_value = extra_features_data.find("td", {"data-title": "Xfob Value"}).text.strip()
    else:
        description = date_built = units = xfob_value = "Not Found"
    
    return {
        "property_description": property_description,
        "total_land_area": total_land_area,
        "land_use_code": land_use_code,
        "zoning": zoning,
        "land_units": land_units,
        "unit_price": unit_price,
        "land_value": land_value,
        "class_unit_price": class_unit_price,
        "class_value": class_value,
        "description": description,
        "date_built": date_built,
        "units": units,
        "xfob_value": xfob_value,
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
        try:
            # Adjust the selector to target the clickable element within each row directly
            row_selector = f"table.table-bordered tbody tr:nth-of-type({index})"
            
            # Wait for the specific row to be clickable, then click
            row_to_click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, row_selector))
            )
            driver.execute_script("arguments[0].click();", row_to_click)
            
            # Scrape details from the detail page
            property_features = scrape_property_features(driver)
            
            # Write some details to csv
            writer.writerow([
            property_features["property_description"], property_features["total_land_area"], property_features["land_use_code"],
            property_features["zoning"], property_features["land_units"], property_features["unit_price"],
            property_features["land_value"], property_features["class_unit_price"], property_features["class_value"],
            property_features["description"], property_features["date_built"], property_features["units"], property_features["xfob_value"]
            ])
        
            navigate_back_to_results(driver)
        except Exception as e:
            print(f"Error processing row {index}: {e}")  # print to catch errors
            navigate_back_to_results(driver)
            continue

def main():
    driver = setup_driver()
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
