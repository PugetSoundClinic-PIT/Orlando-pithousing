import requests

# Example list of Parcel IDs -> will try to get this list
parcel_ids = [
    "272001000000010",
    "272001000000020",
    "272001000000030"
    # Add Parcel ID
]

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

# Loop through each Parcel ID and make the API requests
for pid in parcel_ids:
    # Construct the full URLs with the current Parcel ID
    url_values = f'{base_url_values}PID={pid}&{query_parameters_values}'
    url_general_info = f'{base_url_general_info}pid={pid}'

    # Make a GET request to the GetPRCPropertyValues endpoint
    response_values = requests.get(url_values, headers=headers)
    if response_values.status_code == 200:
        print(f"Success for PID {pid} at GetPRCPropertyValues! Here's some response data:")
        print(response_values.json())
    else:
        print(f"Failed to retrieve data for PID {pid} at GetPRCPropertyValues: HTTP {response_values.status_code}")

    # Make a GET request to the GetPRCGeneralInfo endpoint
    response_general_info = requests.get(url_general_info, headers=headers)
    if response_general_info.status_code == 200:
        print(f"Success for PID {pid} at GetPRCGeneralInfo! Here's some response data:")
        print(response_general_info.json())
    else:
        print(f"Failed to retrieve data for PID {pid} at GetPRCGeneralInfo: HTTP {response_general_info.status_code}")


""" [{
    "id": "29",
    "category": "Condominiums - Residential"
}, {
    "id": "30",
    "category": "Multi-Family Residential 2 - 9 Units"
}, {
    "id": "31",
    "category": "Residential HOA"
}, {
    "id": "32",
    "category": "Single-Family Residential"
}, {
    "id": "33",
    "category": "Vacant Residential Land"
}] """
