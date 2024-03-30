import requests
import json

# Load Parcel IDs from a JSON file
with open('parcel_ids.json', 'r') as json_file:
    parcel_ids = json.load(json_file)

# Base URL for the API endpoints
base_url_values = 'https://ocpa-mainsite-afd-standard.azurefd.net/api/PRC/GetPRCPropertyValues?'
base_url_general_info = 'https://ocpa-mainsite-afd-standard.azurefd.net/api/PRC/GetPRCGeneralInfo?'

# Common query parameters for the Property Values endpoint, except PID
query_parameters_values = 'TaxYear=0&ShowAllFlag=1'

# Headers based on HTTPS Requests
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'ocpa-mainsite-afd-standard.azurefd.net',
    'Origin': 'https://ocpaweb.ocpafl.org',
    'Referer': 'https://ocpaweb.ocpafl.org/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15',
    'x-user-key': 'a5250bb5-c321-4926-a966-9e907f560f31',
}

# Dictionary to hold the fetched data
parcel_data = {}

# Loop through each Parcel ID and make the API requests
for pid in parcel_ids:
    parcel_data[pid] = {}

    # Construct the full URLs with the current Parcel ID
    url_values = f'{base_url_values}PID={pid}&{query_parameters_values}'
    url_general_info = f'{base_url_general_info}pid={pid}'

    # Make a GET request to the GetPRCPropertyValues endpoint
    response_values = requests.get(url_values, headers=headers)
    if response_values.status_code == 200:
        parcel_data[pid]['Values'] = response_values.json()
    else:
        parcel_data[pid]['Values'] = f"Failed to retrieve data: HTTP {response_values.status_code}"

    # Make a GET request to the GetPRCGeneralInfo endpoint
    response_general_info = requests.get(url_general_info, headers=headers)
    if response_general_info.status_code == 200:
        parcel_data[pid]['GeneralInfo'] = response_general_info.json()
    else:
        parcel_data[pid]['GeneralInfo'] = f"Failed to retrieve data: HTTP {response_general_info.status_code}"

# Writing the collected data to a JSON file
with open('/Users/minhanhtruong/Desktop/Orlando-pithousing/parcel_data.json', 'w') as file:
    json.dump(parcel_data, file, indent=4)

print("Fetched data written to parcel_data.json.")
