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

def extract_table_data(driver, writer):
    # Wait for the table body to be present
    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody"))
    )
    # Get the HTML source of the current page
    html_source = driver.page_source
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_source, 'html.parser')
    # Find the table body
    tbody = soup.select_one("table.table-bordered tbody")
    # Iterate over each row in the table body
    for row in tbody.find_all('tr')[1:]:  # Skip the first row 
        # Extract text from each cell
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]

        if len(cells) >= 10:  # Ensure there are enough cells
            address, date_sold, sale_amount, beds, bath, sqft, year, sellers, buyers, parcel_id = cells[:10]
            # Write to CSV
            writer.writerow([address, date_sold, sale_amount, beds, bath, sqft, year, sellers, buyers, parcel_id])


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
        writer.writerow(['Address', 'Date Sold', 'Sale Amount', 'Beds', 'Bath', 'SqFt', 'Year', 'Seller(s)', 'Buyer(s)', 'Parcel ID'])
        page_count = 0        
        while True:
            extract_table_data(driver, writer)
            page_count +=1
            if page_count == 3663:
                break
            try:
                # Try to locate the Next button by its aria-label
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
            except (NoSuchElementException, TimeoutException):
                # Handle cases where the Next button is not found or other exceptions
                print("No Next button found or error clicking Next. Ending pagination.")
                break

    # Click on that row
    # Scarpe all info on property card
    # Come back to the table to click on next row
if __name__ == "__main__":
    main()
