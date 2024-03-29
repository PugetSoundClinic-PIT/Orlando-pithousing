import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def setup_driver():
    options = Options()
    chrome_driver_path = '/Users/minhanhtruong/desktop/pit_housing/chromedriver-mac-x64/chromedriver'
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://ocpaweb.ocpafl.org/parcelsearch')
    return driver

def navigate_and_select_options(driver):
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
    time.sleep(2)  # Wait for the results to load

def get_total_rows(driver):
    tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody")))
    return len(tbody.find_elements(By.TAG_NAME, 'tr'))

def scrape_and_append_data(driver, index, csv_writer):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody")))
    detail_links = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr td a.a-link")
    detail_links[index - 1].click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ngb-nav-6"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.propertyFeaturesForm")))
    detail_html = driver.page_source
    soup = BeautifulSoup(detail_html, 'html.parser')
    # Data extraction:
    # Extract Property Description 
    property_description = soup.find('span', attrs={"_ngcontent-wtk-c92": True}, class_="col-sm-12")

    # Extract Total Land Area 
    land_area = soup.find('span', attrs={"_ngcontent-wtk-c92": True}, class_="row")

    # Other data is from table
    land_units = extract_value_from_table(soup, "Land Units")
    unit_price = extract_value_from_table(soup, "Unit Price")
    land_value = extract_value_from_table(soup, "Land Value")
    class_unit_price = extract_value_from_table(soup, "Class Unit Price")
    class_value = extract_value_from_table(soup, "Class Value")

    # Write the extracted data to CSV
    csv_writer.writerow([property_description, land_area, land_units, unit_price, land_value, class_unit_price, class_value])

def extract_value_from_table(soup, data_title):
    element = soup.find("td", attrs={"data-title": data_title})
    return element.text.strip() if element else "Not Available"

def main():
    driver = setup_driver()
    navigate_and_select_options(driver)
    total_rows = get_total_rows(driver)

    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Property Description', 'Land Area', 'Land Unit', 'Unit Price', 'Land Value', 'Class Unit Price', 'Class Value'])

        for index in range(1, total_rows + 1):
            scrape_and_append_data(driver, index, csv_writer)
            driver.get('https://ocpaweb.ocpafl.org/parcelsearch')  # Navigate directly instead of using driver.back()
            navigate_and_select_options(driver)  # Reapply filters for search

    driver.quit()

if __name__ == "__main__":
    main()
